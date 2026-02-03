# Async7 Controller

The controller service is responsible for the ingress of messages into the Async7 system.

## Process

1.  Receive incoming message
2.  Get message group ID
    -   This should be a unique patient index, or something of the like
3.  Add message to the database for processing by a worker
4.  Acknowledge receipt of message to sender
