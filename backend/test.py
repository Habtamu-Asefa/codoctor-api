import requests
import asyncio
import websockets
import json

session_id = "abc1"

# Step 1: Login and get the JWT token
def login():
    url = "http://localhost:8000/auth/token"
    data = {
        "username": "default_user",
        "password": "password"
    }
    # Send the data as JSON
    response = requests.post(url, json=data)
    response_data = response.json()
    if response.status_code == 200:
        return response_data["access_token"]
    else:
        print("Login failed:", response_data)
        return None

# Step 2: Create a new conversation
def create_conversation():
    url = "http://localhost:8000/conversations/"
    data = {"title": "My New Conversation"}
    headers = {"Authorization": f"Bearer"}
    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()
    if response.status_code == 200:
        conversation_id = response_data["id"]  # Extract just the ID
        return conversation_id
    else:
        print("Failed to create conversation:", response_data)
        return None
    

# Step 3: Send a message using WebSocket
async def send_message(conversation_id, message):
    uri = f"ws://localhost:8000/ws/{conversation_id}"
    async with websockets.connect(uri, extra_headers={"Authorization": f"Bearer "}) as websocket:
        json_message = json.dumps({
            "conversation_id": str(conversation_id),
            "data": message
        })
        await websocket.send(json_message)
        response = await websocket.recv()
        print(f"Response from server: {response}")

def main():
    # token = login()
    # if token:
    #     print(f"Obtained JWT token: {token}")
    conversation_id = create_conversation()
    if conversation_id:
        print(f"Created conversation with ID: {conversation_id}")
        message = "What does an oncologist do ."
        asyncio.run(send_message(conversation_id, message))
    else:
        print("Failed to create conversation")


if __name__ == "__main__":
    main()