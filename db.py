import os
from typing import Optional, List, Dict, Any

from neo4j import GraphDatabase, Driver
from neo4j.exceptions import Neo4jError

_driver: Optional[Driver] = None


def get_driver() -> Driver:
    global _driver
    if _driver is None:
        uri = os.getenv("NEO4J_CONNECTION_URI")
        if not uri:
            raise RuntimeError("NEO4J_CONNECTION_URI not set")

        user = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")

        if user and password:
            _driver = GraphDatabase.driver(uri, auth=(user, password))
        else:
            raise RuntimeError("NEO4J_USERNAME and NEO4J_PASSWORD not set")
    return _driver


class QuerySyntaxError(Exception):
    """Raised when a Cypher syntax error occurs """
    pass


def _run_query(cypher: str, **params):
    """
    Execute a Cypher query and convert Neo4j syntax errors to QuerySyntaxError.

    Returns a list of neo4j.Record objects. Records are materialized while the
    session is open to avoid accessing results after the session closes.
    """
    driver = get_driver()
    try:
        with driver.session() as session:
            result = session.run(cypher, **params)
            return list(result)
    except Neo4jError as e:
        _error_handling(cypher, e)


def _run_query_single(cypher: str, **params):
    """Like _run_query but returns a single record or None."""
    driver = get_driver()
    try:
        with driver.session() as session:
            result = session.run(cypher, **params)
            return result.single()
    except Neo4jError as e:
        _error_handling(cypher, e)


def _error_handling(cypher: str, e: Neo4jError):
    code = getattr(e, "code", "") or ""
    msg = str(e)
    if "SyntaxError" in code or "syntax" in msg.lower():
        raise QuerySyntaxError(f"Cypher syntax error: {msg}\nQuery:\n{cypher}") from e
    raise


# ==== Workshop TODOs: Fill in the Cypher queries below ====


def create_user(username: str, password_hash: str) -> Dict[str, Any]:
    """
    TODO: Create a new user node if it doesn't exist. The app expects a user object called user.

    Suggested shape:
    - Label: User
    - Properties:
        - username: $username
        - passwordHash: $password_hash
        - createdAt: datetime()
    """
    cypher = """
    // TODO: Cypher query to create a User node 
    """
    record = _run_query_single(cypher, username=username, password_hash=password_hash)
    return record["user"] if record else {}


def fetch_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """
    TODO: Fetch a user node by username; the app expects a user object called user. The app expects a user object called user.
    """
    cypher = """
    // TODO: Cypher query to fetch a User node by username
    """
    record = _run_query_single(cypher, username=username)
    return record["user"] if record else None


def create_chat_and_first_message(username: str, message: str) -> Dict[str, Any]:
    """
        TODO: Create a new Chat node linked to the User and store the first user message. The app expects a chat object called chat.

        Suggested shape:
        - Label: Chat
        - Properties:
            - id: randomUUID()
            - createdAt: datetime()
            - updatedAt: datetime()
        - Relationship: (user)-[:STARTED]->(chat)
        """
    cypher = """
    // TODO: Cypher query to create chat
    """
    chat_record = _run_query_single(cypher, username=username, message=message)
    create_message(chat_record["chat"]["id"], role="user", content=message, previous_ai_chat_id=None)
    return chat_record["chat"] if chat_record else {}


def create_message(chat_id: str, role: str, content: str, previous_ai_chat_id: Optional[str]) -> Dict[str, Any]:
    """
    TODO: Create a Message node and link it to an existing Chat. The app expects a message object called message.

    Suggested shape:
    - Label: Message
    - Properties:
        - id: randomUUID()
        - role: $role
        - content: $message
        - createdAt: datetime()
        - previousAIChatId: $previous_ai_chat_id // Note: this comes from the AI and is used for OpenAI to keep track of the conversation
    - Relationship: (chat)-[:HAS_MESSAGE]->(message)
    """
    cypher = """
    // TODO: Cypher query to create a message for a chat
    """
    record = _run_query_single(cypher, chat_id=chat_id, role=role, content=content,
                               previous_ai_chat_id=previous_ai_chat_id)
    return record["message"] if record else {}


def list_user_chats(username: str) -> List[Dict[str, Any]]:
    """
    TODO: Return all chats for the logged-in user. The app expects a stream of chat objects called chat.

    Suggested shape:
    - Label: Chat
    - Properties:
        - id
        - createdAt
        - updatedAt
    - Relationship: (user)-[:STARTED]->(chat)
    """
    cypher = """
    // TODO: cypher query to list user chats
    """
    records = _run_query(cypher, username=username)
    return [r["chat"] for r in records]


def fetch_chat(chat_id: str) -> Optional[Dict[str, Any]]:
    """
    TODO: Fetch a full chat with all messages in a list. The app expects a chat object called chat and a list of messages called messages.

    Hint: Use collect()

    suggested shape:
    - Label: Chat
    - Properties:
        - id
        - createdAt
        - updatedAt
    - Relationship: (chat)-[:HAS_MESSAGE]->(message)
    """
    cypher = """
    // TODO: Cypher query to fetch a chat by id and its messages
    """
    record = _run_query_single(cypher, chat_id=chat_id)
    return record if record else None


def get_ai_response(chat_id: str, previous_chat_id: Optional[str], message: str) -> Optional[Dict[str, Any]]:
    """
    TODO: Send the message to our GenAI plugin; using the ai.text.chat function. The app expects a Cypher Map called aiResponse.

    See the docs for more: https://neo4j.com/docs/genai/plugin/current/generate-text/#chat-new

    - Using the ai.text.chat function, send the message and the config to OpenAI

    Recommended AI config:
    {
        token: $openaiToken,
        model: 'gpt-5-nano'
    }
    """
    cypher = """
    // TODO: Cypher query to send message to AI plugin
    """
    record = _run_query_single(cypher, chat_id=chat_id, previous_chat_id=previous_chat_id, message=message,
                               openaiToken=os.getenv("OPENAI_API_KEY"))
    return record["aiResponse"] if record else None


def get_previous_ai_chat_id(chat_id: str) -> Optional[str]:
    """
    TODO: Using the chat id, find the most recent AI ChatID (returned by openAI), in order to continue the conversation
    if there is none, then the AI chat will be the first chat in this conversation. The app expects a string called chatId.

    Hint: Use an ORDER BY and LIMIT and only search for AI messages

    """
    cypher = """
    // TODO: Cypher query to find the most recent AI ChatID
    """
    record = _run_query_single(cypher, chat_id=chat_id)
    return record["chatId"] if record else None
