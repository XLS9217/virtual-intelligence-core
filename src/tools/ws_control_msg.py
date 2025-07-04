import asyncio
import websockets
import json

MESSAGES = [
    {
        "type": "control",
        "payload": {
            "action": "thinking",
            "content": False
        }
    },
        {
        "type": "control",
        "payload": {
            "action": "thinking",
            "content": True
        }
    },

    {
        "type": "control",
        "payload": {
            "action": "speak",
            "content": "Hello there, welcome to the facility.",
            "body_language": "TalkN"
        }
    },
    {
        "type": "control",
        "payload": {
            "action": "speak",
            "content": "Listen closely. I won’t say this twice.",
            "body_language": "TalkA"
        }
    },
    {
        "type": "control",
        "payload": {
            "action": "speak",
            "content": "Did you know the ancient texts described this very moment?",
            "body_language": "TalkN"
        }
    },
    {
        "type": "control",
        "payload": {
            "action": "speak",
            "content": "Get out of here! Now!",
            "body_language": "TalkA"
        }
    },
    {
        "type": "control",
        "payload": {
            "action": "speak",
            "content": "For Unreal lambdas working with class members, using [this] is recommended for clarity.",
            "body_language": "TalkN"
        }
    },
    {
        "type": "information",
        "payload": {
            "68341adf853baf0882320786": "Default",
            "68341af0853baf0882320788": "Booked",
            "68341b05853baf0882320790": "Focused",
            "68341b15853baf0882320792": "Default"
        }
    },
    {
        "type": "information",
        "payload": {
            "68341adf853baf0882320786": "Focused",
            "68341af0853baf0882320788": "Default",
            "68341b05853baf0882320790": "Default",
            "68341b15853baf0882320792": "Default"
        }
    },
    {
        "type": "information",
        "payload": {
            "68341adf853baf0882320786": "Booked",
            "68341af0853baf0882320788": "Focused",
            "68341b05853baf0882320790": "Booked",
            "68341b15853baf0882320792": "Booked"
        }
    }
]


async def get_input(prompt):
    return await asyncio.to_thread(input, prompt)

async def control_client(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"role": "controller"}))
        print("Registered as controller")

        print("Available messages:")
        for idx, msg in enumerate(MESSAGES):
            print(f"[{idx}] {msg}")

        while True:
            try:
                choice = await get_input("Enter message index to send (or -1 to quit): ")
                choice = int(choice)
                if choice == -1:
                    break
                if 0 <= choice < len(MESSAGES):
                    await websocket.send(json.dumps(MESSAGES[choice]))
                    print(f"Sent: {MESSAGES[choice]}")
                else:
                    print("Invalid index.")
            except ValueError:
                print("Please enter a valid number.")

if __name__ == "__main__":
    asyncio.run(control_client("ws://localhost:8192/link_session"))
