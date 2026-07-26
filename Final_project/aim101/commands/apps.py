import os
import subprocess


def launch(path):
    try:
        subprocess.Popen(path)
        return True
    except:
        return False


def open_chrome():

    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ]

    for path in paths:
        if os.path.exists(path):
            launch(path)
            return "✅ Opening Google Chrome..."

    return "❌ Google Chrome not found."


def open_vscode():

    paths = [
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"),
        r"C:\Program Files\Microsoft VS Code\Code.exe",
    ]

    for path in paths:
        if os.path.exists(path):
            launch(path)
            return "✅ Opening VS Code..."

    return "❌ VS Code not found."


def open_notepad():
    subprocess.Popen("notepad")
    return "📝 Opening Notepad..."


def open_calculator():
    subprocess.Popen("calc")
    return "🧮 Opening Calculator..."


def open_cmd():
    subprocess.Popen("cmd")
    return "💻 Opening Command Prompt..."


def open_powershell():
    subprocess.Popen("powershell")
    return "💙 Opening PowerShell..."


def open_explorer():
    subprocess.Popen("explorer")
    return "📁 Opening File Explorer..."


def open_paint():
    subprocess.Popen("mspaint")
    return "🎨 Opening Paint..."


def open_task_manager():
    subprocess.Popen("taskmgr")
    return "📊 Opening Task Manager..."


def open_control_panel():
    subprocess.Popen("control")
    return "⚙ Opening Control Panel..."


def open_settings():
    os.system("start ms-settings:")
    return "⚙ Opening Windows Settings..."


def open_camera():
    os.system("start microsoft.windows.camera:")
    return "📷 Opening Camera..."


def open_snipping_tool():
    subprocess.Popen("snippingtool")
    return "✂ Opening Snipping Tool..."


def open_word():
    os.system("start winword")
    return "📄 Opening Microsoft Word..."


def open_excel():
    os.system("start excel")
    return "📊 Opening Microsoft Excel..."


def open_powerpoint():
    os.system("start powerpnt")
    return "📽 Opening PowerPoint..."










# import subprocess
# import os

# def open_chrome():
#     paths = [
#         r"C:\Program Files\Google\Chrome\Application\chrome.exe",
#         r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
#     ]

#     for path in paths:
#         if os.path.exists(path):
#             subprocess.Popen(path)
#             return "✅ Opening Google Chrome..."

#     return "❌ Chrome not found."


# def open_vscode():
#     paths = [
#         os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"),
#         r"C:\Program Files\Microsoft VS Code\Code.exe",
#     ]

#     for path in paths:
#         if os.path.exists(path):
#             subprocess.Popen(path)
#             return "✅ Opening VS Code..."

#     return "❌ VS Code not found."


# def open_notepad():
#     subprocess.Popen("notepad")
#     return "✅ Opening Notepad..."


# def open_calculator():
#     subprocess.Popen("calc")
#     return "✅ Opening Calculator..."


# def open_cmd():
#     subprocess.Popen("cmd")
#     return "✅ Opening Command Prompt..."


# def open_explorer():
#     subprocess.Popen("explorer")
#     return "✅ Opening File Explorer..."








# # import subprocess
# # import os

# # def open_chrome():
# #     paths = [
# #         r"C:\Program Files\Google\Chrome\Application\chrome.exe",
# #         r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
# #     ]

# #     for path in paths:
# #         if os.path.exists(path):
# #             subprocess.Popen(path)
# #             return "Opening Google Chrome."

# #     return "Chrome is not installed."


# # def open_vscode():
# #     paths = [
# #         r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe",
# #         r"C:\Program Files\Microsoft VS Code\Code.exe",
# #     ]

# #     for path in paths:
# #         path = os.path.expandvars(path)
# #         if os.path.exists(path):
# #             subprocess.Popen(path)
# #             return "Opening VS Code."

# #     return "VS Code not found."


# # def open_notepad():
# #     subprocess.Popen("notepad")
# #     return "Opening Notepad."


# # def open_calculator():
# #     subprocess.Popen("calc")
# #     return "Opening Calculator."


# # def open_cmd():
# #     subprocess.Popen("cmd")
# #     return "Opening Command Prompt."


# # def open_explorer():
# #     subprocess.Popen("explorer")
# #     return "Opening File Explorer."