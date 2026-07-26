import os
import json
import uuid

HISTORY_DIR = "history"
CURRENT_CHAT_FILE = os.path.join(HISTORY_DIR, "current_chat.txt")

os.makedirs(HISTORY_DIR, exist_ok=True)


def create_new_chat():
    chat_id = str(uuid.uuid4())
    save_current_chat(chat_id)

    file_path = os.path.join(HISTORY_DIR, f"{chat_id}.json")
    with open(file_path, "w") as f:
        json.dump([], f)

    return chat_id


def save_current_chat(chat_id):
    with open(CURRENT_CHAT_FILE, "w") as f:
        f.write(chat_id)


def get_current_chat():
    if not os.path.exists(CURRENT_CHAT_FILE):
        return create_new_chat()

    with open(CURRENT_CHAT_FILE, "r") as f:
        return f.read().strip()


def save_chat(chat_id, messages):
    file_path = os.path.join(HISTORY_DIR, f"{chat_id}.json")
    with open(file_path, "w") as f:
        json.dump(messages, f)


def load_chat(chat_id):
    file_path = os.path.join(HISTORY_DIR, f"{chat_id}.json")

    if not os.path.exists(file_path):
        return []

    with open(file_path, "r") as f:
        return json.load(f)


def get_all_chats():
    return [f for f in os.listdir(HISTORY_DIR) if f.endswith(".json")]