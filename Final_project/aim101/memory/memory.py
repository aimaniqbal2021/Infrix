import json
import os

MEMORY_FILE = "memory/data.json"


def save_memory(key, value):

    data = {}

    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)

    data[key] = value

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f)


def get_memory(key):

    if not os.path.exists(MEMORY_FILE):
        return None

    with open(MEMORY_FILE, "r") as f:
        data = json.load(f)

    return data.get(key)