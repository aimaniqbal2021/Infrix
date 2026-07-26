import streamlit as st



from commands.browser import process_command
# from commands.engine import process_command
st.set_page_config(
    page_title="AIM",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

from history.history_manager import (
    create_new_chat,
    save_chat,
    load_chat,
    get_all_chats,
)

# ---------------- Session ----------------

from history.history_manager import (
    create_new_chat,
    save_chat,
    load_chat,
    get_all_chats,
    get_current_chat,
    save_current_chat,
)

chat_id = get_current_chat()
messages = load_chat(chat_id)

# ---------------- Sidebar ----------------

with st.sidebar:

    st.title("🤖 AIM")

    st.write("AI Intelligent Manager")

    st.divider()

    if st.button("🗑 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("Quick Commands")

    st.write("💻 Open Chrome")
    st.write("🌐 Open Google")
    st.write("🎥 Open YouTube")
    st.write("🐙 Open GitHub")
    st.write("📧 Open Gmail")
    st.write("📅 Date")
    st.write("🕒 Time")

    st.divider()

    st.caption("Version 1.0")

# ---------------- Main ----------------

st.title("🤖 AIM")
st.caption("Your Personal AI Desktop Assistant")

# Chat History

for message in messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
prompt = st.chat_input("Ask AIM anything...")

if prompt:

    messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤖 AIM is thinking..."):

            answer = process_command(prompt)
            st.markdown(answer)

    messages.append({"role": "assistant", "content": answer})

    save_chat(chat_id, messages)
# prompt = st.chat_input("Ask AIM anything...")

# if prompt:

#     st.session_state.messages.append(
#         {
#             "role": "user",
#             "content": prompt
#         }
#     )

#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):

#         with st.spinner("🤖 AIM is thinking..."):

#             answer = process_command(prompt)

#             st.markdown(answer)

#     st.session_state.messages.append(
#         {
#             "role": "assistant",
#             "content": answer
#         }
#     )










# import streamlit as st

# from ai.gemini import ask_gemini

# from commands.apps import *
# from commands.system import *
# from commands.web import *

# st.set_page_config(
#     page_title="AIM",
#     page_icon="🤖",
#     layout="wide",
# )

# # -----------------------------
# # Session State
# # -----------------------------

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # -----------------------------
# # Sidebar
# # -----------------------------

# with st.sidebar:

#     st.title("🤖 AIM")

#     st.markdown("### AI Intelligent Manager")

#     if st.button("🗑 New Chat"):
#         st.session_state.messages = []
#         st.rerun()

#     st.divider()

#     st.markdown("## Commands")

#     st.markdown("""
# ### 💻 Applications

# - Open Chrome
# - Open VSCode
# - Open Notepad
# - Open Calculator
# - Open CMD
# - Open Explorer

# ### 🌐 Websites

# - Open Google
# - Open YouTube
# - Open GitHub
# - Open Gmail
# - Open Facebook
# - Open ChatGPT

# ### 🔍 Search

# Search Google Python

# Search YouTube AI

# ### 📅 System

# Time

# Date
# """)

#     st.divider()

#     st.caption("AIM Version 1.0")

# # -----------------------------
# # Main
# # -----------------------------

# st.title("🤖 AIM")

# st.caption("Your Personal AI Assistant")

# # -----------------------------
# # Chat History
# # -----------------------------

# for message in st.session_state.messages:

#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # -----------------------------
# # User Input
# # -----------------------------

# prompt = st.chat_input("Ask AIM anything...")

# if prompt:

#     st.session_state.messages.append(
#         {
#             "role": "user",
#             "content": prompt
#         }
#     )

#     with st.chat_message("user"):
#         st.markdown(prompt)

#     text = prompt.lower().strip()

#     # -----------------------------
#     # Desktop Apps
#     # -----------------------------

#     if "open chrome" in text:
#         answer = open_chrome()

#     elif "open vscode" in text or "open visual studio code" in text:
#         answer = open_vscode()

#     elif "open notepad" in text:
#         answer = open_notepad()

#     elif "calculator" in text:
#         answer = open_calculator()

#     elif "open cmd" in text:
#         answer = open_cmd()

#     elif "command prompt" in text:
#         answer = open_cmd()

#     elif "open explorer" in text:
#         answer = open_explorer()

#     elif "file explorer" in text:
#         answer = open_explorer()

#     # -----------------------------
#     # Websites
#     # -----------------------------

#     elif "open google" in text:
#         answer = open_google()

#     elif "open youtube" in text:
#         answer = open_youtube()

#     elif "open github" in text:
#         answer = open_github()

#     elif "open gmail" in text:
#         answer = open_gmail()

#     elif "open facebook" in text:
#         answer = open_facebook()

#     elif "open chatgpt" in text:
#         answer = open_chatgpt()

#     # -----------------------------
#     # Google Search
#     # -----------------------------

#     elif text.startswith("search google "):

#         query = prompt[14:]

#         answer = search_google(query)

#     # -----------------------------
#     # YouTube Search
#     # -----------------------------

#     elif text.startswith("search youtube "):

#         query = prompt[15:]

#         answer = search_youtube(query)

#     # -----------------------------
#     # Time
#     # -----------------------------

#     elif text == "time" or "what time" in text:

#         answer = f"🕒 Current Time: {get_time()}"

#     # -----------------------------
#     # Date
#     # -----------------------------

#     elif text == "date" or "today" in text:

#         answer = f"📅 Today's Date: {get_date()}"

#     # -----------------------------
#     # AI
#     # -----------------------------

#     else:

#         with st.spinner("🤖 AIM is thinking..."):

#             answer = ask_gemini(prompt)

#     # -----------------------------
#     # Assistant Reply
#     # -----------------------------

#     with st.chat_message("assistant"):

#         st.markdown(answer)

#     st.session_state.messages.append(
#         {
#             "role": "assistant",
#             "content": answer
#         }
#     )




# # from commands.web import *

# # import streamlit as st

# # from ai.gemini import ask_gemini

# # from commands.apps import (
# #     open_chrome,
# #     open_vscode,
# #     open_notepad,
# #     open_calculator,
# #     open_cmd,
# #     open_explorer,
# # )

# # from commands.system import (
# #     get_time,
# #     get_date,
# # )

# # st.set_page_config(
# #     page_title="AIM",
# #     page_icon="🤖",
# #     layout="wide"
# # )

# # if "messages" not in st.session_state:
# #     st.session_state.messages = []

# # # ===========================
# # # Sidebar
# # # ===========================

# # with st.sidebar:

# #     st.title("🤖 AIM")

# #     st.write("### Desktop AI Assistant")

# #     if st.button("🗑 New Chat"):
# #         st.session_state.messages = []
# #         st.rerun()

# #     st.divider()

# #     st.write("### Features")

# #     st.write("✅ AI Chat")
# #     st.write("✅ Open Chrome")
# #     st.write("✅ Open VS Code")
# #     st.write("✅ Open Notepad")
# #     st.write("✅ Open Calculator")
# #     st.write("✅ Open CMD")
# #     st.write("✅ File Explorer")
# #     st.write("✅ Time & Date")

# #     st.divider()

# #     st.caption("Version 1.0")

# # # ===========================
# # # Main Page
# # # ===========================

# # st.title("🤖 AIM")
# # st.caption("AI Intelligent Manager")

# # # Display chat history

# # for msg in st.session_state.messages:

# #     with st.chat_message(msg["role"]):
# #         st.markdown(msg["content"])

# # # ===========================
# # # User Input
# # # ===========================

# # prompt = st.chat_input("Ask AIM anything...")

# # if prompt:

# #     st.session_state.messages.append(
# #         {
# #             "role": "user",
# #             "content": prompt,
# #         }
# #     )

# #     with st.chat_message("user"):
# #         st.markdown(prompt)

# #     text = prompt.lower().strip()

# #     # ===========================
# #     # Built-in Commands
# #     # ===========================

# #     if "open chrome" in text:
# #         answer = open_chrome()

# #     elif "open vscode" in text or "open visual studio code" in text:
# #         answer = open_vscode()

# #     elif "open notepad" in text:
# #         answer = open_notepad()

# #     elif "calculator" in text:
# #         answer = open_calculator()

# #     elif "open cmd" in text or "command prompt" in text:
# #         answer = open_cmd()

# #     elif "open explorer" in text or "file explorer" in text:
# #         answer = open_explorer()

# #     elif "time" in text:
# #         answer = f"🕒 Current Time: {get_time()}"

# #     elif "date" in text:
# #         answer = f"📅 Today's Date: {get_date()}"

# #     else:

# #         with st.chat_message("assistant"):

# #             with st.spinner("Thinking..."):

# #                 answer = ask_gemini(prompt)

# #                 st.markdown(answer)

# #         st.session_state.messages.append(
# #             {
# #                 "role": "assistant",
# #                 "content": answer,
# #             }
# #         )

# #         st.stop()

# #     # ===========================
# #     # Display Command Response
# #     # ===========================

# #     with st.chat_message("assistant"):
# #         st.markdown(answer)

# #     st.session_state.messages.append(
# #         {
# #             "role": "assistant",
# #             "content": answer,
# #         }
# #     )







# # # from commands.apps import (
# # #     open_chrome,
# # #     open_vscode,
# # #     open_notepad,
# # #     open_calculator,
# # #     open_cmd,
# # #     open_explorer,
# # # )
# # # from commands.system import get_time, get_date

# # # import streamlit as st
# # # from ai.gemini import ask_gemini

# # # st.set_page_config(
# # #     page_title="AIM",
# # #     page_icon="🤖",
# # #     layout="wide"
# # # )

# # # if "messages" not in st.session_state:
# # #     st.session_state.messages = []

# # # with st.sidebar:

# # #     st.title("🤖 AIM")

# # #     if st.button("🗑 New Chat"):
# # #         st.session_state.messages = []
# # #         st.rerun()

# # #     st.divider()

# # #     st.write("Version 1.0")

# # # st.title("🤖 AIM")
# # # st.caption("AI Intelligent Manager")

# # # for msg in st.session_state.messages:

# # #     with st.chat_message(msg["role"]):
# # #         st.markdown(msg["content"])

# # # prompt = st.chat_input("Ask AIM anything...")

# # # if prompt:

# # #     st.session_state.messages.append(
# # #         {
# # #             "role": "user",
# # #             "content": prompt,
# # #         }
# # #     )

# # #     with st.chat_message("user"):
# # #         st.markdown(prompt)

# # #     with st.chat_message("assistant"):

# # #         with st.spinner("Thinking..."):

# # #             answer = ask_gemini(prompt)

# # #             st.markdown(answer)

# # #     st.session_state.messages.append(
# # #         {
# # #             "role": "assistant",
# # #             "content": answer,
# # #         }
# # #     )


    