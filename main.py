from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Lifespan
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, database, Message as DBMessage
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define Pydantic models
class Message(BaseModel):
    message: str

class WebSocketMessage(BaseModel):
    conversation_id: str
    data: str

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def startup():
    await database.connect()

async def shutdown():
    await database.disconnect()

@app.websocket("/ws/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: int, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            json_data = await websocket.receive_text()
            data = WebSocketMessage.model_validate_json(json_data)
            db_message = DBMessage(conversation_id=conversation_id, data=data.data, timestamp=datetime.now())
            db.add(db_message)
            db.commit()
            db.refresh(db_message)
            response = WebSocketMessage(conversation_id=str(conversation_id), data=f"Message text was: {data.data}")
            await websocket.send_text(response.model_dump_json())
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for conversation {conversation_id}")

@app.get("/", response_model=Message)
async def get():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)