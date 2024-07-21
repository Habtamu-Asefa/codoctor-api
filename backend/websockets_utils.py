# websocket_utils.py
from fastapi import WebSocket
from sqlalchemy.orm import Session
from backend.models.schema import Message as DBMessage
from datetime import datetime
from utility import logger
from fastapi import WebSocket, WebSocketDisconnect, Depends
from pydantic import BaseModel, ValidationError
from sqlalchemy.exc import SQLAlchemyError
from AI.codoctor_ai import CoDoctor
from AI.agent import Oncology


onco = Oncology()

doctor = CoDoctor()
session_id = "abc1"



# Define Pydantic models
class Message(BaseModel):
    message: str

class ConversationCreate(BaseModel):
    title: str
    id: int = None


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
                db_message = DBMessage(conversation_id=conversation_id, data=data.data, timestamp=datetime.now(), is_ai=False)

                db.add(db_message)
                db.commit()
                db.refresh(db_message)

                # ai_response = doctor.invoke(data.data, session_id)
                ai_response = onco.create_rag_chain().invoke(data.data)
                db_ai_message = DBMessage(conversation_id=conversation_id, data=str(ai_response), is_ai=True, timestamp=datetime.now())
                db.add(db_ai_message)
                db.commit()
                db.refresh(db_ai_message)
                chat_history = db.query(DBMessage).filter(DBMessage.conversation_id == conversation_id).all()
                response = WebSocketMessage(conversation_id=str(conversation_id), data=f"Message text was: {ai_response}")
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