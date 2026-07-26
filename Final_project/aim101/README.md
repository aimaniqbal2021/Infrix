# 🤖 AIM101 — AI Intelligent Manager

AIM101 is a Jarvis-like AI assistant built using Python and Streamlit.  
It combines AI (Hugging Face), system automation, web commands, and a modern chat UI.

---

## 🚀 Features

### 🤖 AI Assistant
- Hugging Face Inference API
- Natural conversations
- Code generation
- Explanations & summaries

### 💻 System Commands
- Open Chrome
- Open Google / YouTube / GitHub / Gmail
- Show Date & Time

### 🌐 Web Automation
- Browser control
- Quick navigation commands

### 🧠 Chat Interface
- Streamlit-based UI
- Chat-style interaction
- Sidebar with quick commands

---

## 📁 Project Structure


AIM101/
│
├── ai/
│ └── gemini.py # Hugging Face AI logic
│
├── commands/
│ ├── apps.py
│ ├── browser.py # Command processor
│ ├── system.py
│ └── web.py
│
├── ui/
│ ├── chat.py
│ ├── home.py
│ ├── sidebar.py
│ └── theme.py
│
├── history/ # (Planned: chat history storage)
├── logs/ # Logs
├── memory/ # (Planned: AI memory)
│
├── voice/
│ ├── speech.py
│ └── tts.py
│
├── utils/
│ └── helpers.py
│
├── app.py # Main Streamlit app
├── config.py
├── .env
├── requirements.txt
└── README.md

---

## ⚙️ Installation

### 1. Clone the project
```bash
git clone <your-repo>
cd AIM101
2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
3. Install dependencies
pip install -r requirements.txt
4. Add environment variables

Create .env file:

HF_TOKEN=your_huggingface_token_here
▶️ Run the App
streamlit run app.py
🧠 How It Works
User enters a prompt in UI
app.py sends it to:
→ commands/browser.py
Command is:
matched (open chrome, time, etc.)
OR sent to AI (ai/gemini.py)
Response is shown in chat UI
⚠️ Known Issues (IMPORTANT)
❌ 1. Chat History Not Saved

Problem:

Chats disappear on refresh
No old conversations stored

Reason:

Using temporary memory only (no file/database)

Fix (Planned):

Store chats in /history/*.json
Track current chat session
❌ 2. AI Error: [Errno 11001] getaddrinfo failed

Problem:

AI responses fail

Causes:

No internet connection
Invalid Hugging Face token
DNS/network issue

Fix:

Check internet
Verify .env
Test API manually
❌ 3. Commands Not Triggering (e.g., install wireshark)

Problem:

Commands go to AI instead of executing

Reason:

Weak command matching logic

Fix:

Improve parsing in process_command()
Use .lower() and keyword matching

Example fix:

command = command.lower()

if "install" in command and "wireshark" in command:
    ...
❌ 4. Software Installation Not Working

Problem:

Install commands fail silently

Reasons:

No admin privileges
winget not installed
OS compatibility

Fix:

Run terminal as Administrator
Check winget --version
🛠 Future Improvements
🧠 AI
Better prompt engineering
Streaming responses
Multi-model support
💬 Chat
Persistent chat history
Multiple conversations
Rename chats
🧠 Memory
Long-term memory system
Context awareness
🎤 Voice
Speech-to-text
Wake word (Jarvis style)
Text-to-speech responses
⚙️ System
App launching
File management
Task automation
📦 Updating Dependencies

To generate requirements.txt:

pip freeze > requirements.txt
🤝 Contributing

This project is under active development.
Feel free to fork and improve.

📜 License

MIT License

👨‍💻 Author

AIM101 Project by Aiman Iqbal


---

# 🔥 BONUS (IMPORTANT)

When you update dependencies later:

```bash
pip freeze > requirements.txt

👉 This saves ALL installed packages automatically