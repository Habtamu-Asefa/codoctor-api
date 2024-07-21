import requests
import asyncio
import websockets
import json

session_id = "abc1"

# Step 1: Login and get the JWT token
def login():
<<<<<<< HEAD
    url = "http://localhost:8000/auth/token"
=======
    url = "http://localhost:8000/token"
>>>>>>> 67cbfa0fd8fedd4810ab474eab6715f0627df220
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
def create_conversation(token):
    url = "http://localhost:8000/conversations/"
    data = {"title": "My New Conversation"}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()
    if response.status_code == 200:
        conversation_id = response_data["id"]  # Extract just the ID
        return conversation_id
    else:
        print("Failed to create conversation:", response_data)
        return None

# Step 3: Send a message using WebSocket
async def send_message(conversation_id, message, token):
    uri = f"ws://localhost:8000/ws/{conversation_id}"
    async with websockets.connect(uri, extra_headers={"Authorization": f"Bearer {token}"}) as websocket:
        json_message = json.dumps({
            "conversation_id": str(conversation_id),
            "data": message
        })
        await websocket.send(json_message)
        response = await websocket.recv()
        print(f"Response from server: {response}")

def main():
    token = login()
    if token:
        print(f"Obtained JWT token: {token}")
        conversation_id = create_conversation(token)
        if conversation_id:
            print(f"Created conversation with ID: {conversation_id}")
<<<<<<< HEAD
            message = "What does an oncologist do ."
=======
            message = "Hello, tell me about common cold."
>>>>>>> 67cbfa0fd8fedd4810ab474eab6715f0627df220
            asyncio.run(send_message(conversation_id, message, token))
        else:
            print("Failed to create conversation")
    else:
        print("Failed to obtain JWT token")

if __name__ == "__main__":
    main()
