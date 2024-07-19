# websocket_utils.py
from fastapi import WebSocket
from sqlalchemy.orm import Session
from database import Message as DBMessage
from datetime import datetime
from utility import logger
from fastapi import WebSocket, WebSocketDisconnect, Depends
from pydantic import BaseModel, ValidationError
from sqlalchemy.exc import SQLAlchemyError


# Define Pydantic models
class Message(BaseModel):
    message: str

class WebSocketMessage(BaseModel):
    conversation_id: str
    data: str


async def process_websocket_message(websocket: WebSocket, conversation_id: int, db: Session):
    try:
        while True:
            try:
                json_data = await websocket.receive_text()
                logger.debug(f"Received message in conversation {conversation_id}: {json_data}")
                data = WebSocketMessage.model_validate_json(json_data)
                db_message = DBMessage(conversation_id=conversation_id, data=data.data, timestamp=datetime.now())
                db.add(db_message)
                db.commit()
                db.refresh(db_message)
                response = WebSocketMessage(conversation_id=str(conversation_id), data=f"Message text was: {data.data}")
                await websocket.send_text(response.model_dump_json())
                logger.debug(f"Message processed and response sent in conversation {conversation_id}")
            except ValidationError as ve:
                logger.error(f"Validation error for message data in conversation {conversation_id}: {ve.json()}")
                await websocket.send_text(f"Error: Invalid message data - {ve.json()}")
            except SQLAlchemyError as sqle:
                logger.error(f"Database error in conversation {conversation_id}: {sqle}")
                db.rollback()
                await websocket.send_text("Error: Could not save message to database.")
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for conversation {conversation_id}")
    except Exception as e:
        logger.error(f"Unexpected error in conversation {conversation_id}: {e}")
        await websocket.close(code=1011)