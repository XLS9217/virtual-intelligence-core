# LinkSession - WebSocket Session Protocol

## Overview

LinkSession is a lightweight WebSocket-based session manager for two types of clients:

## Roles

| Role        | Purpose                                | Behavior                                      |
|-------------|----------------------------------------|-----------------------------------------------|
| controller  | Sends **control** messages             | These are broadcast to all displayer clients. |
| displayer   | Receives control messages              | Can process payloads to perform specific actions. |

## Message Format

All WebSocket messages must be JSON-encoded with the following structure:

{
  "type": "",
  "payload": {}
}

### Supported Types

| type      | Description                            | Target                             |
|-----------|----------------------------------------|------------------------------------|
| control   | Sent by controller clients             | Broadcast to all displayers        |
| user_chat | the input setence from user            | Send to agent for further process  |

### Payload Description

**control**
e.g.



control types
* speak: send to tts to generate speech
  <pre>
  {
    "type": "control",
    "payload": {
      "action": "speak",
      "content": "Hello" (a string of what to speak)
      "body_language": "" (from display_info, if any of the display can be use as a body language, should stop when speak end)
    }
  }
  </pre>
* play: A series of what will happen in the display side
  <pre>
  {
    "type": "control",
    "payload": {
      "action": "play",
      "content":[
        {
          "name":"play1"
        }
      ]
    }
  }
  </pre>

**user_chat**

<pre>
{
  "type": "user_chat",
  "payload": {
    "recognized": true,
    "content": "Hello"
  }
}
</pre>


**display_info**

<pre>
{
  "type": "display_info",
  "payload": {
    "action" : "add" | "set"
    "content": [
      "display_name": "",
      "display_description" : "",
    ]
  }
}
</pre>
action types
* "add" : append to list
* "set" : reset the list

## Protocol Flow

1. **Connection**
   - Client connects to: `/link_session`
   - Must immediately send:
     {
       "role": "controller" | "displayer" **Must have**
       "platform": "unreal" | "live2d" | "web"
     }

2. **Data Transfer**
   - Controllers send:
     {
       "type": "type_string",
       "payload": ...
     }
   - Displayers receive control broadcasts and handle payload instructions such as `{ "action": "speak" }`.

3. **Special Display**
   - Displayers send:
     {
       "type": "display_info",
       "payload": ...
     }
   - Displayers receive control broadcasts and handle payload instructions such as `{ "action": "speak" }`.
