from fastapi import WebSocket, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from setup import logger, app, database
from database_utils import init_db
from utility import timing_decorator
from websockets_utils import process_websocket_message, Message


# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    logger.info(f"WebSocket connection established for conversation {conversation_id}")
    await websocket.accept()
    await process_websocket_message(websocket, conversation_id, db)


@app.get("/")
async def get():
    return {"message": "Hello World"}