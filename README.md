# async7

The idea behind this is to allow for asynchronous HL7v2 message processing, that supports in-order message handling, retries, and dead-letter queues.

HL7 feeds from systems like LIMS and EPRs send messages in the order they need to be processed. If messages are processed out of order, it may cause data integrity issues. This library allows for asynchronous processing while maintaining the order of messages.

If we can group messages by a unique patient index, we can process messages for different patients in parallel, while ensuring that messages for the same patient are processed in order. This will improve throughput while maintaining data integrity.

## Features

-   Asynchronous message processing to increase general throughput
-   In-order processing of messages for the same patient
-   Parallel processing of messages for different patients
-   Retry mechanism for failed message processing
-   Dead-letter queue for messages that fail after maximum retries
-   Fully horizontally scalable, by adding more worker instances

## Notes

TBD
