from async7_controller import Async7Controller
import uvicorn


class A7Implement(Async7Controller):
    async def get_group_id_from_message(self, message: str) -> str:
        """
        Extracts and returns the group ID from the given message.

        The idea behind this is to group messages for batch processing, so messages
        from the same patient should return the same group ID.

        Args:
            message (str): The input message containing group information.
        """

        return "42"


a7_controller = A7Implement(
    pg_host="localhost",
    pg_user="joe",
    pg_password="thisismypassword",  # nosec B106 (for demo's sake)
    pg_database="async7",
    pg_schema="public",
    pg_port=5432,
)
app = a7_controller.get_fastapi_app()

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)  # nosec B104 (for demo's sake)
