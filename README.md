Pink Programming Chatbot (Flask + Neo4j)

Overview
- Flask web app scaffold for a chatbot that stores users, chats, and messages in Neo4j.
- Participants complete the Cypher TODOs in `db.py` to enable user auth, chat creation, and viewing history.
- OpenAI is used to generate assistant replies; reads config from environment variables.

Quick Start with Codespaces
- Create an account on https://console-preview.neo4j.io/ and create a free Aura instance (make sure to save the password).
- In the GitHub repository click the green "Use this template" button and open the project in a codespace.
- Copy `.env.example` to `.env` and set values.
  - `NEO4J_CONNECTION_URI`: Inspect your Aura instance and copy the connection URI.
  - `NEO4J_PASSWORD`: (paste password that you got during the instance creation).
- Open the Run and Debug menu and start the "Flask: run app.py" configuration.
- It opens a terminal and starts the Flask development server, click on the link to open the app in a new browser tab.
- Try registering a new user, you should see Cypher Error page which means you're ready to start the exercises!

Workshop Tasks (Cypher TODOs in `db.py`)
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
