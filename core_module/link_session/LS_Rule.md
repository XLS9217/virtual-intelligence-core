# LinkSession - WebSocket Session Protocol

## Overview

LinkSession is a lightweight WebSocket-based session manager for two types of clients:

- **Controller**: Sends control messages intended for broadcast to all **Displayers**.
- **Displayer**: Receives control messages 

## Roles

| Role        | Purpose                                | Behavior                                      |
|-------------|----------------------------------------|-----------------------------------------------|
| controller  | Sends **control** messages             | These are broadcast to all displayer clients. |
| displayer   | Receives control messages              | Can process payloads to perform specific actions. |

## Message Format

All WebSocket messages must be JSON-encoded with the following structure:

{
  "type": "control",
  "payload": ... // your data here
}

### Supported Types

| type      | Description                            | Target                             |
|-----------|----------------------------------------|------------------------------------|
| control   | Sent by controller clients             | Broadcast to all displayers        |

## Payload Control

Displayers can interpret the `payload` field of incoming control messages to perform specific actions. Example:

{
  "type": "control",
  "payload": {
    "action": "speak",
    "content": "Hello"
  }
}

In this example, the displayer should handle the `"speak"` action as appropriate for its implementation.



## Protocol Flow

1. **Connection**
   - Client connects to: `/link_session`
   - Must immediately send:
     {
       "role": "controller" | "displayer"
     }

2. **Data Transfer**
   - Controllers send:
     {
       "type": "control",
       "payload": ...
     }
   - Displayers receive control broadcasts and handle payload instructions such as `{ "action": "speak" }`.
