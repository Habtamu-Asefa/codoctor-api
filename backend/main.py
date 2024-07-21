from fastapi import HTTPException, WebSocket, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.auth.auth import  get_current_user
from backend.models.schema import Conversation, User
from setup import logger, app
from backend.models.setup import database
from backend.models.database import init_db, get_db
from utility import timing_decorator
from websockets_utils import process_websocket_message, ConversationCreate
from backend.auth_utils import Token
from sqlalchemy.exc import SQLAlchemyError


async def startup():
    init_db()
    await database.connect()


async def shutdown():
    await database.disconnect()


app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)


@app.websocket("/ws/{conversation_id}")
@timing_decorator
async def websocket_endpoint(websocket: WebSocket, conversation_id: int, db: Session = Depends(get_db)):
    """
    WebSocket endpoint for a conversation.
    """
    logger.info(f"WebSocket connection established for conversation {conversation_id}")
    await websocket.accept()
    await process_websocket_message(websocket, conversation_id, db)

    
@app.post("/conversations/", response_model=ConversationCreate)
async def create_conversation(conversation_data: ConversationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Create a new conversation.

    - **title**: each conversation must have a title
    """
    new_conversation = Conversation(title=conversation_data.title, owner_id=current_user.id)
    db.add(new_conversation)
    try:
        db.commit()
        db.refresh(new_conversation)
        return new_conversation
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating conversation: {e}")
        raise HTTPException(status_code=500, detail="Error creating conversation")


@app.get("/")
async def get():
    return {"message": "Hello World"}

