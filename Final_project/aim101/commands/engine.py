from commands.browser import browser_commands
from commands.system import system_commands
from ai.gemini import ask_gemini

# from memory.memory import save_memory, get_memory

# if "my name is" in command:
#     name = command.replace("my name is", "").strip()
#     save_memory("name", name)
#     return f"Got it, {name}!"

# elif "what is my name" in command:
#     name = get_memory("name")
#     return name if name else "I don't know your name yet."


def process_command(command: str):

    command = command.lower()

    # 1. Browser commands
    result = browser_commands(command)
    if result:
        return result

    # 2. System commands
    result = system_commands(command)
    if result:
        return result

    # 3. AI fallback
    return ask_gemini(command)