from .model import generate_text
from .prompt_builder import build_messages


def generate_answer(query, intent, entities, documents, api_token):
    messages = build_messages(query, intent, entities, documents)
    return generate_text(messages, token=api_token).strip()
