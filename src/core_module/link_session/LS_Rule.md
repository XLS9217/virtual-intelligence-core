# LinkSession - WebSocket Session Protocol

## Overview

LinkSession is a lightweight WebSocket-based session manager for two types of clients:

## Roles

| Role        | Purpose                                | Behavior                                      |
|-------------|----------------------------------------|-----------------------------------------------|
| controller  | Sends **control** messages             | These are broadcast to all displayer clients. |
| displayer   | Receives control messages              | Can process payloads to perform specific actions. |
| monitor     | Receives all messages                  | Listens all control message and display message|

## Message Format

All WebSocket messages must be JSON-encoded with the following structure:

{
  "type": "",
  "payload": {}
}


### Payload Description

**control**
Sent by controller clients 
Broadcast to all {displayer , monitor}

e.g.

control types

* speak: send to tts to generate speech
  <pre>
  {
    "type": "control",
    "payload": {
      "action": "speak",
      "content": "Hello" (a string of what to speak)
    }
  }
  </pre>

  * motion: perform a motion based on motion dict
  <pre>
  {
    "type": "control",
    "payload": {
      "action": "motion",
      "content": "Idle_1" (a string of what to perform)
    }
  }
  </pre>

* inform: just use this for updating status and error reporting, front end should define their own behaviour 
  <pre>
  {
    "type": "control",
    "payload": {
      "action": "inform",
      "content": "e.g. I'm extracting the mcp logic" 
    }，
  }
  </pre>


* thinking
  <pre>
  {
    "type": "control",
    "payload": {
      "action": "thinking",
      "content": true | false
    }
  }
  </pre>


**information**
  use a list to return a client defined specific information representation

  <pre>
  {
    "type": "information",
    "payload": {
      [] <--- a list
    }
  }
  </pre>


**user_chat**
user input

<pre>
{
  "type": "user_chat",
  "payload": {
    "recognized": true,
    "content": "Hello"
  }
}
</pre>

I'm current using this to transition to strategy group
<pre>
{
  "type": "execute_strategy",
  "payload": {
    "recognized": true,
    "content": "Hello"
  }
}
</pre>


**motion_dict**
From displayer send to Link session
description of what to do while responding
<pre>
{
  "type": "motion_dict",
  "payload": {
    "action" : "add" | "set"
    "content": [
      "motion_name": "",
      "motion_description" : "",
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
       "session_id": "id string"  if not send will fall into the base session
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
