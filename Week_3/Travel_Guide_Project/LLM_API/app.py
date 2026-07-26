import os
import streamlit as st
from huggingface_hub import login
from nlp.pipeline import run_pipeline
from llm.generator import generate_answer

# ─── HuggingFace Auth ────────────────────────────────────────────────────────
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except Exception:
    HF_TOKEN = os.environ.get("HF_TOKEN", "")

if HF_TOKEN:
    try:
        login(HF_TOKEN)
    except Exception as e:
        st.warning(f"Could not log in to Hugging Face: {e}")
else:
    st.warning("No HF_TOKEN found. Add it to .streamlit/secrets.toml as HF_TOKEN = \"your_token_here\".")

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Infrix · Tourist Guide Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Root vars ── */
:root {
    --bg:       #0d0f14;
    --surface:  #13161e;
    --border:   #1e2330;
    --accent:   #6c63ff;
    --accent2:  #00e5c0;
    --text:     #e2e8f0;
    --muted:    #64748b;
    --user-bg:  #1a1d2e;
    --bot-bg:   #111420;
}

/* ── Global reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Top banner ── */
.top-banner {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 22px 28px 18px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 24px;
}
.top-banner .logo-ring {
    width: 46px; height: 46px;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex; align-items: center; justify-content: center;
    font-size: 22px;
}
.top-banner h1 {
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.3px !important;
    margin: 0 !important; padding: 0 !important;
    color: var(--text) !important;
}
.top-banner .sub {
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 2px;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Stat cards ── */
.stat-row {
    display: flex; gap: 14px;
    margin-bottom: 24px;
}
.stat-card {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
}
.stat-card .label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--muted);
    margin-bottom: 6px;
}
.stat-card .value {
    font-size: 1.6rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ── Chat container ── */
.chat-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
}
.chat-header {
    padding: 14px 20px;
    border-bottom: 1px solid var(--border);
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    color: var(--muted);
    display: flex; align-items: center; gap: 8px;
}
.chat-header .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--accent2);
    box-shadow: 0 0 6px var(--accent2);
}

/* ── Message bubbles ── */
.msg-user {
    display: flex;
    justify-content: flex-end;
    margin: 12px 20px;
}
.msg-user .bubble {
    background: linear-gradient(135deg, #6c63ff22, #6c63ff44);
    border: 1px solid #6c63ff55;
    border-radius: 14px 14px 4px 14px;
    padding: 12px 16px;
    max-width: 70%;
    font-size: 0.9rem;
    line-height: 1.5;
}

.msg-bot {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin: 12px 20px;
}
.msg-bot .avatar {
    width: 32px; height: 32px;
    border-radius: 8px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex; align-items: center; justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
    margin-top: 2px;
}
.msg-bot .bubble {
    background: var(--bot-bg);
    border: 1px solid var(--border);
    border-radius: 4px 14px 14px 14px;
    padding: 12px 16px;
    max-width: 75%;
    font-size: 0.9rem;
    line-height: 1.6;
}

/* ── NLP insight panel ── */
.nlp-panel {
    background: var(--bot-bg);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 10px;
    padding: 14px 18px;
    margin: 0 20px 12px 52px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
}
.nlp-panel .row { display: flex; gap: 8px; margin-bottom: 4px; }
.nlp-panel .key { color: var(--muted); min-width: 70px; }
.nlp-panel .val { color: var(--accent2); }
.nlp-panel .badge {
    display: inline-block;
    background: #6c63ff22;
    border: 1px solid #6c63ff44;
    border-radius: 4px;
    padding: 1px 6px;
    color: var(--accent);
    margin-right: 4px;
    font-size: 0.68rem;
}

/* ── Sidebar content ── */
.sidebar-section {
    margin-bottom: 24px;
}
.sidebar-label {
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: var(--muted);
    margin-bottom: 10px;
    font-weight: 600;
}
.history-item {
    padding: 8px 12px;
    border-radius: 8px;
    background: #1e2330;
    margin-bottom: 6px;
    font-size: 0.78rem;
    color: #94a3b8;
    cursor: pointer;
    border: 1px solid transparent;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.history-item:hover { border-color: var(--accent); color: var(--text); }

.intent-chip {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    margin: 3px;
}
.chip-DESTINATIONS  { background: #ff6b6b22; border: 1px solid #ff6b6b55; color: #ff6b6b; }
.chip-ACCOMMODATION { background: #ffd93d22; border: 1px solid #ffd93d55; color: #ffd93d; }
.chip-TRANSPORT     { background: #6bcb7722; border: 1px solid #6bcb7755; color: #6bcb77; }
.chip-FOOD          { background: #4d96ff22; border: 1px solid #4d96ff55; color: #4d96ff; }
.chip-GENERAL       { background: #6c63ff22; border: 1px solid #6c63ff55; color: #a78bfa; }

/* ── Streamlit input override ── */
[data-testid="stChatInput"] textarea {
    background: #13161e !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px #6c63ff33 !important;
}

/* ── Native Streamlit widget fixes (these were invisible before) ── */
[data-testid="stMetric"] {
    background: transparent !important;
}
[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
}
[data-testid="stMetricValue"] {
    color: var(--text) !important;
}
.stButton button {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
}
.stButton button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}
[data-testid="stMarkdownContainer"] p {
    color: var(--text) !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--muted) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ───────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "nlp_meta" not in st.session_state:
    st.session_state.nlp_meta = []
if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:20px 0 10px'>
        <div style='font-size:1.1rem;font-weight:700;letter-spacing:-0.3px'>⚡ Infrix NLP</div>
        <div style='font-size:0.72rem;color:#64748b;font-family:JetBrains Mono,monospace;margin-top:4px'>
            intelligence · v3.0
        </div>
    </div>
    <hr style='border:none;border-top:1px solid #1e2330;margin:0 0 20px'>
    """, unsafe_allow_html=True)

    # Stats
    n_turns = len([m for m in st.session_state.messages if m["role"] == "user"])
    intents_seen = list({m["intent"] for m in st.session_state.nlp_meta}) if st.session_state.nlp_meta else []

    st.markdown('<div class="sidebar-label">Session Stats</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.metric("Queries", n_turns)
    col2.metric("Intents", len(intents_seen))

    if intents_seen:
        st.markdown('<div class="sidebar-label" style="margin-top:20px">Detected Intents</div>', unsafe_allow_html=True)
        chips = "".join(f'<span class="intent-chip chip-{i}">{i}</span>' for i in intents_seen)
        st.markdown(chips, unsafe_allow_html=True)

    # History
    user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
    if user_msgs:
        st.markdown('<div class="sidebar-label" style="margin-top:24px">Recent Queries</div>', unsafe_allow_html=True)
        for m in reversed(user_msgs[-6:]):
            preview = m["content"][:42] + ("…" if len(m["content"]) > 42 else "")
            st.markdown(f'<div class="history-item">↗ {preview}</div>', unsafe_allow_html=True)

    # Clear
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑 Clear Session", use_container_width=True):
        st.session_state.messages = []
        st.session_state.nlp_meta = []
        st.rerun()

    # Model info
    st.markdown("""
    <hr style='border:none;border-top:1px solid #1e2330;margin:20px 0 14px'>
    <div class="sidebar-label">Model</div>
    <div style='font-size:0.72rem;font-family:JetBrains Mono,monospace;color:#94a3b8'>
        Qwen/Qwen2.5-7B-Instruct<br>
        <span style='color:#64748b'>via HF Inference API</span>
    </div>
    <div class="sidebar-label" style="margin-top:16px">Pipeline</div>
    <div style='font-size:0.72rem;font-family:JetBrains Mono,monospace;color:#94a3b8;line-height:1.8'>
        TF-IDF Retrieval<br>spaCy NER<br>Intent Classifier<br>Prompt Builder
    </div>
    """, unsafe_allow_html=True)

# ─── Main Area ────────────────────────────────────────────────────────────────
# Top banner
st.markdown("""
<div class="top-banner">
    <div class="logo-ring">⚡</div>
    <div>
        <h1>Tourist Guide Assistant</h1>
        <div class="sub">Travel Knowledge Base · LLM + NLP Pipeline</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Stat cards
total_q = len([m for m in st.session_state.messages if m["role"] == "user"])
last_intent = st.session_state.nlp_meta[-1]["intent"] if st.session_state.nlp_meta else "—"
last_ents = len(st.session_state.nlp_meta[-1]["entities"]) if st.session_state.nlp_meta else 0

st.markdown(f"""
<div class="stat-row">
    <div class="stat-card">
        <div class="label">Total Queries</div>
        <div class="value">{total_q:02d}</div>
    </div>
    <div class="stat-card">
        <div class="label">Last Intent</div>
        <div class="value" style="font-size:1.1rem;padding-top:6px">{last_intent}</div>
    </div>
    <div class="stat-card">
        <div class="label">Entities Found</div>
        <div class="value">{last_ents}</div>
    </div>
    <div class="stat-card">
        <div class="label">Model</div>
        <div class="value" style="font-size:0.75rem;padding-top:8px">Qwen2.5-7B</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Chat area
st.markdown("""
<div class="chat-wrap">
    <div class="chat-header">
        <div class="dot"></div>
        Conversation · Live
    </div>
""", unsafe_allow_html=True)

# Empty state
if not st.session_state.messages:
    st.markdown("""
    <div style='text-align:center;padding:60px 20px;'>
        <div style='font-size:2.5rem;margin-bottom:14px'>🧠</div>
        <div style='font-size:1rem;font-weight:600;color:#e2e8f0;margin-bottom:8px'>Ask anything about your trip</div>
        <div style='font-size:0.8rem;color:#64748b'>Try: "What's the best time to visit Hunza?" or "Where should I stay in Skardu?"</div>
        </div>
    """, unsafe_allow_html=True)


# Render messages
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-user">
            <div class="bubble">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="msg-bot">
            <div class="avatar">⚡</div>
            <div class="bubble">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

        # Show NLP insight panel for this turn
        turn_idx = sum(1 for m in st.session_state.messages[:i+1] if m["role"] == "assistant") - 1
        if turn_idx < len(st.session_state.nlp_meta):
            meta = st.session_state.nlp_meta[turn_idx]
            entity_badges = "".join(
                f'<span class="badge">{e["text"]} <span style="color:#64748b">·</span> {e["label"]}</span>'
                for e in meta["entities"]
            ) or '<span style="color:#64748b">none</span>'
            st.markdown(f"""
            <div class="nlp-panel">
                <div class="row"><span class="key">intent</span><span class="val">{meta["intent"]}</span></div>
                <div class="row"><span class="key">entities</span><span class="val">{entity_badges}</span></div>
                <div class="row"><span class="key">docs</span><span class="val">{meta["doc_count"]} retrieved</span></div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ─── Chat Input ───────────────────────────────────────────────────────────────
prompt = st.chat_input("Ask a question about your trip…")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Running NLP pipeline…"):
        nlp_result = run_pipeline(prompt)
        answer = generate_answer(
            query=prompt,
            intent=nlp_result["intent"],
            entities=nlp_result["entities"],
            documents=nlp_result["documents"],
            api_token=HF_TOKEN,
        )

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.nlp_meta.append({
        "intent": nlp_result["intent"],
        "entities": nlp_result["entities"],
        "doc_count": len(nlp_result["documents"]),
    })
    st.session_state.total_queries += 1
    st.rerun()
