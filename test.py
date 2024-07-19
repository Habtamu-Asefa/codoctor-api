import requests
import asyncio
import websockets
import json  # Import the json module to format the message as JSON

# Step 1: Create a new conversation
def create_conversation():
    url = "http://localhost:8000/conversations/"
    data = {"title": "My New Conversation"}
    response = requests.post(url, json=data)
    conversation_id = response.json().get('id')  # Extract just the ID
    return conversation_id  # Return only the conversation ID

# Step 2: Send a message using WebSocket
async def send_message(conversation_id, message):
    uri = f"ws://localhost:8000/ws/{conversation_id}"
    async with websockets.connect(uri) as websocket:
        # Adjust the JSON payload to include conversation_id and wrap message inside data
        json_message = json.dumps({
            "conversation_id": str(conversation_id),
            "data": message
        })
        await websocket.send(json_message)
        response = await websocket.recv()
        print(f"Response from server: {response}")

def main():
    conversation_id = create_conversation()
    if conversation_id:
        print(f"Created conversation with ID: {conversation_id}")
        message = "Hello, this is a message."
        asyncio.run(send_message(conversation_id, message))
    else:
        print("Failed to create conversation")

if __name__ == "__main__":
    main()