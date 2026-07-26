import json
import os

MEMORY_FILE = "memory/memory.json"


def load_memory():

    if not os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "w") as f:
            json.dump({}, f)

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(data):

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


def remember(key, value):

    data = load_memory()

    data[key] = value

    save_memory(data)

    return f"✅ I will remember that your {key} is {value}."


def recall(key):

    data = load_memory()

    if key in data:
        return data[key]

    return None


def everything():

    data = load_memory()

    if len(data) == 0:
        return "I don't remember anything yet."

    result = ""

    for k, v in data.items():

        result += f"• {k}: {v}\n"

    return result