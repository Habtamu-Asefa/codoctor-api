API for CoDoctor

Welcome to the backend of the Co-Doctor API. This API is built using FastAPI and is used to provide the backend services for the Co-Doctor application.

Structure
The API is structured as follows:

Backend
- The main entry point is run.py which contains code to start the FastAPI server.
- The API routes are defined in the main.py file.
- The main websockets helper codes are defined in the websocket_utils.py file.
    - The Co-Doctor AI responses are processed in this file and sent to the front end.
- The database models are defined in models module.
    - The schema for the database models are defined in the schemas file
    - The database connection and some helper functions is defined in the database file
    - The database setup are defined in setup.py file
- The authentication and authorization are defined in the auth module.
    - The authentication and authorization functions are defined in the auth.py file.
    - The token generation and verification functions are defined in the auth_utils file.
    - The authentication routes are defined in the auth_routes file.



AI
- Run test_ai.py to test the ai on terminal
