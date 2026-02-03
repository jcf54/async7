from fastapi import FastAPI, APIRouter, Request, Response
from dataclasses import dataclass
import asyncpg
from contextlib import asynccontextmanager


@dataclass
class PostgresConfig:
    host: str
    user: str
    password: str
    database: str = "postgres"
    schema: str = "public"
    port: int = 5432

    def get_dsn(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


def ingress_route_handler(a7_controller: "Async7Controller") -> APIRouter:
    router = APIRouter()

    @router.post("/hl7v2/")
    async def hl7v2_ingress_handler(request: Request) -> Response:
        data = await request.body()

        message_data = data.decode()

        if not message_data:
            return Response(status_code=200, content="Empty message received.")

        try:
            msg_group_id = await a7_controller.get_group_id_from_message(message_data)
        except Exception as e:
            # TODO: add dead-letter queue handling here
            raise e

        async with a7_controller.pg_pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO hl7v2 (message, group_id)
                VALUES ($1, $2)
                """,
                message_data,
                str(msg_group_id),
            )

        return Response(status_code=204)

    return router


class Async7Controller:
    fastapi_app: FastAPI
    postgres_config: PostgresConfig
    dead_letter_threshold: int = 5

    def __init__(
        self,
        pg_host: str,
        pg_user: str,
        pg_password: str,
        pg_database: str = "postgres",
        pg_schema: str = "public",
        pg_port: int = 5432,
        dead_letter_threshold: int = 5,
    ) -> None:
        """
        Initializes the Async7Controller with PostgreSQL configuration and FastAPI app.

        Args:
            pg_host (str): PostgreSQL host.
            pg_user (str): PostgreSQL user.
            pg_password (str): PostgreSQL password.
            pg_database (str, optional): PostgreSQL database name. Defaults to
                "postgres".
            pg_schema (str, optional): PostgreSQL schema name. Defaults to "public".
            pg_port (int, optional): PostgreSQL port. Defaults to 5432.
            dead_letter_threshold (int, optional): Threshold for dead-letter queue
                handling. Defaults to 5.
        """
        self.postgres_config = PostgresConfig(
            host=pg_host,
            user=pg_user,
            password=pg_password,
            database=pg_database,
            schema=pg_schema,
            port=pg_port,
        )

        self.dead_letter_threshold = dead_letter_threshold

        self.fastapi_app = FastAPI(
            title="Async7 Controller",
            lifespan=self.lifespan,
        )

        self.fastapi_app.include_router(
            ingress_route_handler(self),
        )

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        # Create Postgres connection pool
        self.pg_pool = await asyncpg.create_pool(
            dsn=self.postgres_config.get_dsn(),
        )
        # Store the pool in the app state for access in endpoints
        app.state.pg_pool = self.pg_pool

        try:
            yield
        finally:
            await self.pg_pool.close()

    def get_fastapi_app(self) -> FastAPI:
        """
        Returns the FastAPI application instance to be called by an ASGI server.

        Returns:
            FastAPI: The controller's FastAPI application instance.
        """
        return self.fastapi_app

    async def get_group_id_from_message(self, message: str) -> str:
        """
        Extracts and returns the group ID from the given message.

        The idea behind this is to group messages for batch processing, so messages
        from the same patient should return the same group ID.

        Args:
            message (str): The input message containing group information.
        """

        raise NotImplementedError(
            "This method should be implemented to extract group ID from message."
        )
