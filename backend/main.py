<<<<<<< HEAD
from fastapi import HTTPException, WebSocket, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.auth.auth import  get_current_user
from backend.models.schema import Conversation, User
from setup import logger, app
from backend.models.setup import database
from backend.models.database import init_db, get_db
=======
from datetime import timedelta
from fastapi import HTTPException, Request, WebSocket, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.auth_utils import verify_password
from backend.auth import create_access_token, get_current_user, get_user_by_username
from models import SessionLocal, Conversation, User
from setup import logger, app, database
from backend.database import init_db, get_db
>>>>>>> 67cbfa0fd8fedd4810ab474eab6715f0627df220
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
<<<<<<< HEAD
=======


# @app.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(SessionLocal)):
#     user = get_user_by_username(db, form_data.username)
#     if user is None or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


@app.post("/token", response_model=Token)
async def login_for_access_token(request: Request, db: Session = Depends(get_db)):
    print("Login for access token")
    try:
        json_data = await request.json()
        username = json_data["username"]
        password = json_data["password"]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid input data",
        )

    user = get_user_by_username(db, username)
    if user is None or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
>>>>>>> 67cbfa0fd8fedd4810ab474eab6715f0627df220
