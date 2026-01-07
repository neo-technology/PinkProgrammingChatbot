Pink Programming Chatbot (Flask + Neo4j)

Overview
- Flask web app scaffold for a chatbot that stores users, chats, and messages in Neo4j.
- Participants complete the Cypher TODOs in `db.py` to enable user auth, chat creation, and viewing history.
- OpenAI is used to generate assistant replies; reads config from environment variables.

Quick Start
- Python 3.9+
- Install dependencies:
  - uv: `uv sync` 
- Copy `.env.example` to `.env` and set values.
- Run: `python app.py`

Environment Variables
- `NEO4J_CONNECTION_URI`: Neo4j Connection URI (copy from your Aura instance).
- `NEO4J_USERNAME` / `NEO4J_PASSWORD`: (default username: neo4j, paste password that you get during the instance creation).
- `OPENAI_API_KEY`: API key for OpenAI 
- `OPENAI_BASE_URL`: https://api.openai.com/v1 (no need to change)

Workshop Tasks (Cypher TODOs in `db.py`)
- Create an account on https://console-preview.neo4j.io/ and create a free Aura instance.
- Create/Login User
  - `create_user(username, password_hash)`: create a `:User` with properties and return it.
  - `fetch_user_by_username(username)`: find a `:User` by username and return it.
- Chat With Chatbot
  - `create_chat_and_first_message(user_id, message)`: create a `:Chat` and the first user `:Message`.
  - `create_message(chat_id, role, content)`: append messages (both user and assistant) to a chat.
- See Previous Chats
  - `list_user_chats(user_id)`: gat all chats for the user, return summary list.
  - `fetch_chat(chat_id)`: return full chat with messages ordered by time.

Pages
- `/register` and `/login`: basic authentication using Flask sessions.
- `/chat/new`: start a new chat by sending the first message.
- `/chats`: list previous chats.
- `/chats/<chat_id>`: view and continue a chat.

Safety and Dev Tips
- Do not commit secrets. Use `.env` locally.
- Hash passwords; never store plain text. We use `werkzeug.security`.
- For production, set a strong `FLASK_SECRET_KEY` and configure HTTPS.
