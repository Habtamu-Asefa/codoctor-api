API for CoDoctor
Welcome to the backend of the Co-Doctor API. This API is built using FastAPI and is used to provide the backend services for the Co-Doctor application.

Structure
The API is structured as follows:

Backend
- The main entry point is run.py which contains code to start the FastAPI server.
- The API routes are defined in the main.py file.
- The main websockets helper codes are defined in the websocket_utils.py file.
    - The Co-Doctor AI reponses are process in this file and sent to the frontend.
- The database models are defined in models.py.
- The database connection and session management is defined in the database.py file.
(For now the run.py in the main directory should be used to run the server, the run.py in the backend directory is not used)

AI
