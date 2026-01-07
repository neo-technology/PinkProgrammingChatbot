import os
from typing import Optional

from openai import OpenAI, APIConnectionError, OpenAIError


def get_openai_client() -> Optional[OpenAI]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url.rstrip("/"))
    return OpenAI(api_key=api_key)


def generate_ai_response(prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Generates an assistant message for the given prompt using OpenAI.

    You can change the default model to any available to your account.
    """
    client = get_openai_client()
    if client is None:
        return "[AI unavailable: missing OPENAI_API_KEY]"

    # Using Chat Completions API for broad compatibility
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        return resp.choices[0].message.content or ""
    except APIConnectionError:
        return "[AI unavailable: connection error to OpenAI API]"
    except OpenAIError as e:
        # Generic safety net for other OpenAI errors (auth, rate limit, etc.)
        return f"[AI error: {e.__class__.__name__}]"
