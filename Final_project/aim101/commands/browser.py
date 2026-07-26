from ai.gemini import ask_gemini
from ai.memory import *

from commands.apps import *
from commands.system import *
from commands.web import *


def process_command(prompt: str):

    text = prompt.lower().strip()

    # ==========================
    # Desktop Apps
    # ==========================

    if "open chrome" in text:
        return open_chrome()

    elif "open vscode" in text or "open visual studio code" in text:
        return open_vscode()

    elif "open notepad" in text:
        return open_notepad()

    elif "calculator" in text:
        return open_calculator()

    elif "open cmd" in text:
        return open_cmd()

    elif "command prompt" in text:
        return open_cmd()

    elif "open explorer" in text or "file explorer" in text:
        return open_explorer()

    elif "open powershell" in text:
        return open_powershell()

    elif "open paint" in text:
        return open_paint()

    elif "open task manager" in text:
        return open_task_manager()

    elif "open settings" in text:
        return open_settings()

    elif "open control panel" in text:
        return open_control_panel()

    elif "open camera" in text:
        return open_camera()

    elif "open snipping tool" in text:
        return open_snipping_tool()

    elif "open word" in text:
        return open_word()

    elif "open excel" in text:
        return open_excel()

    elif "open powerpoint" in text:
        return open_powerpoint()

    # ==========================
    # Websites
    # ==========================

    elif "open google" in text:
        return open_google()

    elif "open youtube" in text:
        return open_youtube()

    elif "open github" in text:
        return open_github()

    elif "open gmail" in text:
        return open_gmail()

    elif "open facebook" in text:
        return open_facebook()

    elif "open chatgpt" in text:
        return open_chatgpt()

    # ==========================
    # Search
    # ==========================

    elif text.startswith("search google "):
        return search_google(prompt[14:])

    elif text.startswith("search youtube "):
        return search_youtube(prompt[15:])

    

    # ==========================
    # System
    # ==========================

    elif text == "time" or "what time" in text:
        return f"🕒 Current Time: {get_time()}"

    elif text == "date" or "today" in text:
        return f"📅 Today's Date: {get_date()}"

    elif "battery" in text:
        return get_battery()

    elif "ram" in text:
        return get_ram()

    elif "cpu" in text:
        return get_cpu()

    elif "computer name" in text:
        return get_pc_name()

    elif "windows version" in text:
        return get_windows()

    elif "screenshot" in text:
        return take_screenshot()

    elif "lock pc" in text:
        return lock_pc()

    elif "restart pc" in text:
        return restart_pc()

    elif "shutdown pc" in text:
        return shutdown_pc()

    elif "sleep pc" in text:
        return sleep_pc()

    # ==========================
    # Memory
    # ==========================

    elif text.startswith("remember "):

        sentence = prompt[9:]

        if " is " in sentence:

            key, value = sentence.split(" is ", 1)

            return remember(key.strip(), value.strip())

        else:

            return "Example:\nRemember my name is Aiman"

    elif "what do you remember" in text:

        return everything()

    elif "what is my" in text:

        key = text.replace("what is my", "").strip()

        value = recall(key)

        if value:

            return f"Your {key} is {value}"

        return f"I don't know your {key} yet."

    # ==========================
    # AI
    # ==========================

    return ask_gemini(prompt)











# from commands.apps import *

# from ai.memory import *

# from commands.system import *

# from ai.gemini import ask_gemini

# from commands.apps import (
#     open_chrome,
#     open_vscode,
#     open_notepad,
#     open_calculator,
#     open_cmd,
#     open_explorer,
# )

# from commands.system import (
#     get_time,
#     get_date,
# )

# from commands.web import (
#     open_google,
#     open_youtube,
#     open_github,
#     open_gmail,
#     open_facebook,
#     open_chatgpt,
#     search_google,
#     search_youtube,
# )


# def process_command(prompt: str):

#     text = prompt.lower().strip()

#     # ==========================
#     # Desktop Apps
#     # ==========================

#     if "open chrome" in text:
#         return open_chrome()

#     elif "open vscode" in text or "open visual studio code" in text:
#         return open_vscode()

#     elif "open notepad" in text:
#         return open_notepad()

#     elif "calculator" in text:
#         return open_calculator()

#     elif "open cmd" in text:
#         return open_cmd()

#     elif "command prompt" in text:
#         return open_cmd()

#     elif "open explorer" in text:
#         return open_explorer()

#     elif "file explorer" in text:
#         return open_explorer()
#     elif "open powershell" in text:
#         return open_powershell()

#     elif "open paint" in text:
#         return open_paint()

#     elif "open task manager" in text:
#         return open_task_manager()

#     elif "open settings" in text:
#         return open_settings()

#     elif "open control panel" in text:
#         return open_control_panel()

#     elif "open camera" in text:
#         return open_camera()

#     elif "open snipping tool" in text:
#         return open_snipping_tool()

#     elif "open word" in text:
#         return open_word()

#     elif "open excel" in text:
#         return open_excel()

#     elif "open powerpoint" in text:
#         return open_powerpoint()
      

#     # ==========================
#     # Websites
#     # ==========================

#     elif "open google" in text:
#         return open_google()

#     elif "open youtube" in text:
#         return open_youtube()

#     elif "open github" in text:
#         return open_github()

#     elif "open gmail" in text:
#         return open_gmail()

#     elif "open facebook" in text:
#         return open_facebook()

#     elif "open chatgpt" in text:
#         return open_chatgpt()

#     # ==========================
#     # Search
#     # ==========================

#     elif text.startswith("search google "):
#         query = prompt[14:]
#         return search_google(query)

#     elif text.startswith("search youtube "):
#         query = prompt[15:]
#         return search_youtube(query)

#     # ==========================
#     # System
#     # ==========================

#     elif text == "time" or "what time" in text:
#         return f"🕒 Current Time: {get_time()}"

#     elif "battery" in text:
#         return get_battery()

#     elif "ram" in text:
#         return get_ram()

#     elif "cpu" in text:
#         return get_cpu()

#     elif "computer name" in text:
#         return get_pc_name()

#     elif "windows version" in text:
#         return get_windows()

#     elif "screenshot" in text:
#         return take_screenshot()

#     elif "lock pc" in text:
#         return lock_pc()

#     elif "restart pc" in text:
#         return restart_pc()

#     elif "shutdown pc" in text:
#         return shutdown_pc()

#     elif "sleep pc" in text:
#         return sleep_pc()

#     elif text == "date" or "today" in text:
#         return f"📅 Today's Date: {get_date()}"


# # ==========================
# # Memory
# # ==========================

#     elif text.startswith("remember "):

#         sentence = prompt[9:]

#     if " is " in sentence:

#         key, value = sentence.split(" is ", 1)

#         return remember(key.strip(), value.strip())

#     else:

#         return "Use:\nRemember my name is Aiman"


#     elif "what do you remember" in text:

#         return everything()


#     elif "what is my" in text:

#         key = text.replace("what is my", "").strip()

#     value = recall(key)

#     if value:

#         return f"Your {key} is {value}"

#     return f"I don't know your {key} yet."

#     # ==========================
#     # AI
#     # ==========================

#     return ask_gemini(prompt)