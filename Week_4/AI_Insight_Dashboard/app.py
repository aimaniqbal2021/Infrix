"""
CodeLens — Local AI Code Review Dashboard
Author: Aiman Iqbal

A Streamlit dashboard that reviews source code using a locally running
Ollama model. Nothing leaves the machine — no cloud calls, no API keys.
See README.md for setup and usage instructions.
"""

import streamlit as st
import requests
import json
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="CodeLens — Code Review Dashboard",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# THEME / CSS
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

.stApp {
    background-color: #0a1414;
    color: #d6e6e6;
}

#MainMenu, footer, header { visibility: hidden; }

[data-testid="stSidebar"] {
    background-color: #0d1a1a;
    border-right: 1px solid #163030;
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #2dd4bf;
}

/* Stat tile */
.stat-tile {
    background: #0f1f1f;
    border: 1px solid #1c3838;
    border-radius: 10px;
    padding: 18px 20px;
    text-align: center;
}
.stat-tile .num {
    font-size: 30px;
    font-weight: 700;
    line-height: 1;
}
.stat-tile .lbl {
    font-size: 11px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #5b7d7d;
    margin-top: 8px;
}

/* Severity badges */
.sev-critical { color: #f87171; border-color: #4a1f1f; background: #1f0f0f; }
.sev-high     { color: #fb923c; border-color: #4a2f10; background: #1f150a; }
.sev-medium   { color: #facc15; border-color: #4a3f10; background: #1f1a0a; }
.sev-low      { color: #60a5fa; border-color: #10304a; background: #0a151f; }

.issue-card {
    border: 1px solid #1c3838;
    border-left-width: 4px;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 10px;
    background: #0d1a1a;
}
.issue-title {
    font-weight: 600;
    font-size: 14px;
    margin-bottom: 4px;
}
.issue-body {
    font-size: 13px;
    color: #a8c4c4;
    line-height: 1.55;
}
.issue-line-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #5b7d7d;
}

.strength-row, .suggestion-row {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    padding: 9px 0;
    border-bottom: 1px solid #142828;
    font-size: 13px;
    color: #cde3e3;
}
.strength-dot { width:7px; height:7px; min-width:7px; border-radius:50%; background:#2dd4bf; margin-top:6px; }
.suggestion-dot { width:7px; height:7px; min-width:7px; border-radius:50%; background:#818cf8; margin-top:6px; }

.summary-panel {
    background: #0f1c1c;
    border-left: 3px solid #2dd4bf;
    padding: 16px 20px;
    border-radius: 0 8px 8px 0;
    font-size: 14px;
    color: #a8c4c4;
    line-height: 1.7;
}

.stButton > button {
    background: linear-gradient(135deg, #0f766e, #2dd4bf);
    color: #04110f;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    padding: 10px 22px;
}
.stButton > button:hover { opacity: 0.85; color: #04110f; }

.stTextInput > div > input,
.stSelectbox > div > div,
.stTextArea > div > textarea {
    background: #0f1f1f !important;
    border: 1px solid #1c3838 !important;
    color: #d6e6e6 !important;
}

.history-item {
    padding: 8px 10px;
    border-radius: 6px;
    font-size: 12px;
    color: #a8c4c4;
    border: 1px solid transparent;
    margin-bottom: 4px;
}
.history-item.active {
    border-color: #2dd4bf;
    background: #10201f;
    color: #2dd4bf;
}

.chat-user {
    background: #10201f; border-radius: 12px 12px 4px 12px;
    padding: 10px 15px; margin: 6px 0; font-size: 13px; text-align: right; color: #d6e6e6;
}
.chat-ai {
    background: #0d1a1a; border: 1px solid #1c3838; border-radius: 12px 12px 12px 4px;
    padding: 10px 15px; margin: 6px 0; font-size: 13px; color: #a8c4c4;
}

.status-up { color: #2dd4bf; }
.status-down { color: #f87171; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# OLLAMA CLIENT
# ─────────────────────────────────────────────────────────────────────────────

OLLAMA_HOST = "http://localhost:11434"


@st.cache_data(ttl=10)
def ollama_is_up():
    try:
        r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


@st.cache_data(ttl=30)
def available_models():
    try:
        r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        names = [m["name"] for m in r.json().get("models", [])]
        return names if names else ["llama3"]
    except Exception:
        return ["llama3"]


def run_model(prompt, model, max_tokens=2500, temperature=0.15):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature, "num_predict": max_tokens},
    }
    r = requests.post(f"{OLLAMA_HOST}/api/generate", json=payload, timeout=240)
    r.raise_for_status()
    return r.json().get("response", "").strip()


# ─────────────────────────────────────────────────────────────────────────────
# PROMPTS
# ─────────────────────────────────────────────────────────────────────────────

LANGUAGE_HINTS = {
    ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript", ".jsx": "JavaScript (React)",
    ".tsx": "TypeScript (React)", ".java": "Java", ".go": "Go", ".rb": "Ruby",
    ".php": "PHP", ".c": "C", ".cpp": "C++", ".cs": "C#", ".rs": "Rust", ".sql": "SQL",
}


def guess_language(filename):
    ext = Path(filename).suffix.lower()
    return LANGUAGE_HINTS.get(ext, "unknown")


def review_prompt(code, language_hint):
    lang_ctx = f"\nThe file extension suggests this is: {language_hint}" if language_hint != "unknown" else ""
    return f"""You are a strict, senior code reviewer doing a pull-request review. Be direct and specific — cite line numbers where possible.{lang_ctx}

CODE:
\"\"\"
{code[:6000]}
\"\"\"

Return ONLY a raw JSON object, no markdown fences, no commentary outside the JSON:

{{
  "detected_language": "best guess at language",
  "quality_score": number from 1 to 10,
  "quality_score_reason": "one sentence justification",
  "summary": "2-3 sentence overall verdict on this code, written like a reviewer leaving a PR comment",
  "issues": [
    {{
      "severity": "critical | high | medium | low",
      "category": "bug | security | performance | style | maintainability",
      "line": number or null,
      "title": "short issue title",
      "detail": "what's wrong and why it matters"
    }}
  ],
  "strengths": ["specific things done well, be concrete"],
  "refactor_suggestions": ["concrete refactor or improvement ideas, not generic advice"]
}}"""


def chat_prompt(code, question):
    return f"""You are reviewing the code below. Answer the question directly in 2-5 sentences, referencing specific lines or patterns where relevant. No filler.

CODE:
\"\"\"
{code[:6000]}
\"\"\"

QUESTION: {question}"""


def severity_rank(sev):
    return {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(sev, 4)


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────────────────────

if "reviews" not in st.session_state:
    st.session_state.reviews = {}   # name -> {"code":..., "language":..., "result":..., "chat":[]}
if "active_review" not in st.session_state:
    st.session_state.active_review = None

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🧭 CodeLens")
    st.caption("Local AI code review — runs entirely on your machine")
    st.markdown("---")

    up = ollama_is_up()
    st.markdown(
        f'<span class="{"status-up" if up else "status-down"}">● Ollama {"online" if up else "offline"}</span>',
        unsafe_allow_html=True,
    )
    if not up:
        st.error("Start Ollama first:\n\n`ollama serve`")

    model = st.selectbox("Model", available_models())

    st.markdown("---")
    st.markdown("### Session History")
    if st.session_state.reviews:
        for name in st.session_state.reviews:
            is_active = name == st.session_state.active_review
            cls = "history-item active" if is_active else "history-item"
            if st.button(f"📄 {name}", key=f"hist_{name}", use_container_width=True):
                st.session_state.active_review = name
                st.rerun()
    else:
        st.caption("Reviewed files will show up here.")

    st.markdown("---")
    st.markdown("""
**Setup**
1. [Download Ollama](https://ollama.com)
2. `ollama pull llama3`
3. `ollama serve`
    """)

# ─────────────────────────────────────────────────────────────────────────────
# HEADER + INPUT
# ─────────────────────────────────────────────────────────────────────────────

st.markdown('<h1 style="font-size:26px; font-weight:700; margin-bottom:2px;">Code Review Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#5b7d7d; font-size:14px; margin-bottom:24px;">Paste code or upload a file. Get a PR-style review, scored and broken down by severity.</p>', unsafe_allow_html=True)

input_col1, input_col2 = st.columns([3, 2])

with input_col1:
    uploaded_file = st.file_uploader("Upload a source file", type=list(k.strip(".") for k in LANGUAGE_HINTS) + ["txt"])
with input_col2:
    pasted_name = st.text_input("Or name a pasted snippet", placeholder="e.g. auth_handler.py")

pasted_code = st.text_area("…or paste code directly here", height=160, placeholder="def example():\n    pass")

review_clicked = st.button("Run Review", disabled=not up)

if review_clicked:
    if uploaded_file is not None:
        code_text = uploaded_file.read().decode("utf-8", errors="ignore")
        file_key = uploaded_file.name
        lang_hint = guess_language(uploaded_file.name)
    elif pasted_code.strip():
        file_key = pasted_name.strip() if pasted_name.strip() else f"snippet_{len(st.session_state.reviews)+1}.txt"
        code_text = pasted_code
        lang_hint = guess_language(file_key)
    else:
        st.warning("Upload a file or paste some code first.")
        code_text = None

    if code_text and len(code_text.strip()) > 10:
        with st.spinner(f"Reviewing {file_key} with {model}..."):
            raw = run_model(review_prompt(code_text, lang_hint), model)
        try:
            s, e = raw.find("{"), raw.rfind("}") + 1
            result = json.loads(raw[s:e])
        except Exception:
            st.error("Model returned something that wasn't valid JSON. Try again or switch models.")
            with st.expander("Raw model output"):
                st.code(raw)
            result = None

        if result:
            st.session_state.reviews[file_key] = {
                "code": code_text,
                "language": lang_hint,
                "result": result,
                "chat": [],
            }
            st.session_state.active_review = file_key
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# ACTIVE REVIEW DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────

active = st.session_state.active_review
if active and active in st.session_state.reviews:
    entry = st.session_state.reviews[active]
    result = entry["result"]
    issues = sorted(result.get("issues", []), key=lambda i: severity_rank(i.get("severity", "low")))
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for i in issues:
        sev = i.get("severity", "low")
        if sev in counts:
            counts[sev] += 1

    st.markdown("---")

    top1, top2, top3, top4, top5 = st.columns(5)
    score = result.get("quality_score", 0)
    with top1:
        st.markdown(f'<div class="stat-tile"><div class="num" style="color:#2dd4bf;">{score}/10</div><div class="lbl">Quality Score</div></div>', unsafe_allow_html=True)
    with top2:
        st.markdown(f'<div class="stat-tile"><div class="num" style="color:#f87171;">{counts["critical"]}</div><div class="lbl">Critical</div></div>', unsafe_allow_html=True)
    with top3:
        st.markdown(f'<div class="stat-tile"><div class="num" style="color:#fb923c;">{counts["high"]}</div><div class="lbl">High</div></div>', unsafe_allow_html=True)
    with top4:
        st.markdown(f'<div class="stat-tile"><div class="num" style="color:#facc15;">{counts["medium"]}</div><div class="lbl">Medium</div></div>', unsafe_allow_html=True)
    with top5:
        st.markdown(f'<div class="stat-tile"><div class="num" style="color:#60a5fa;">{counts["low"]}</div><div class="lbl">Low</div></div>', unsafe_allow_html=True)

    tab_overview, tab_issues, tab_strengths, tab_refactor, tab_chat = st.tabs(
        ["📊 Overview", "🐞 Issues", "✅ Strengths", "🛠 Refactor Ideas", "💬 Ask CodeLens"]
    )

    with tab_overview:
        st.markdown(f"**File:** `{active}`  ·  **Detected language:** {result.get('detected_language', entry['language'])}")
        st.markdown(f'<div class="summary-panel">{result.get("summary", "")}</div>', unsafe_allow_html=True)
        st.caption(result.get("quality_score_reason", ""))
        with st.expander("View submitted code"):
            st.code(entry["code"][:6000], language=entry["language"].lower() if entry["language"] != "unknown" else None)

    with tab_issues:
        if issues:
            for i in issues:
                sev = i.get("severity", "low")
                line_tag = f'line {i["line"]}' if i.get("line") else "general"
                st.markdown(f"""
                <div class="issue-card sev-{sev}">
                    <div class="issue-title">{i.get('title','Issue')} <span class="issue-line-tag">· {line_tag} · {i.get('category','')}</span></div>
                    <div class="issue-body">{i.get('detail','')}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.success("No issues flagged by the model.")

    with tab_strengths:
        strengths = result.get("strengths", [])
        if strengths:
            rows = "".join(f'<div class="strength-row"><div class="strength-dot"></div><div>{s}</div></div>' for s in strengths)
            st.markdown(rows, unsafe_allow_html=True)
        else:
            st.caption("No specific strengths called out.")

    with tab_refactor:
        suggestions = result.get("refactor_suggestions", [])
        if suggestions:
            rows = "".join(f'<div class="suggestion-row"><div class="suggestion-dot"></div><div>{s}</div></div>' for s in suggestions)
            st.markdown(rows, unsafe_allow_html=True)
        else:
            st.caption("No refactor suggestions given.")

    with tab_chat:
        for msg in entry["chat"]:
            cls = "chat-user" if msg["role"] == "user" else "chat-ai"
            st.markdown(f'<div class="{cls}">{msg["content"]}</div>', unsafe_allow_html=True)

        quick_qs = [
            "What's the single riskiest part of this code?",
            "How would you test this?",
            "Is this production-ready?",
            "What would you change first?",
        ]
        qcols = st.columns(2)
        for idx, q in enumerate(quick_qs):
            with qcols[idx % 2]:
                if st.button(q, key=f"quick_{active}_{idx}"):
                    with st.spinner("Thinking..."):
                        ans = run_model(chat_prompt(entry["code"], q), model, max_tokens=400)
                    entry["chat"].append({"role": "user", "content": q})
                    entry["chat"].append({"role": "ai", "content": ans})
                    st.rerun()

        with st.form(f"chat_form_{active}", clear_on_submit=True):
            qc, bc = st.columns([5, 1])
            with qc:
                user_q = st.text_input("", placeholder="Ask anything about this code...", label_visibility="collapsed")
            with bc:
                sent = st.form_submit_button("Ask")
            if sent and user_q.strip():
                with st.spinner("Thinking..."):
                    ans = run_model(chat_prompt(entry["code"], user_q), model, max_tokens=400)
                entry["chat"].append({"role": "user", "content": user_q})
                entry["chat"].append({"role": "ai", "content": ans})
                st.rerun()

elif not st.session_state.reviews:
    st.markdown("""
    <div style="text-align:center; padding:70px 20px; color:#264646;">
        <div style="font-size:52px; margin-bottom:18px;">🧭</div>
        <div style="font-size:17px; font-weight:600; color:#3d6060; margin-bottom:8px;">Paste or upload code to run your first review</div>
        <div style="font-size:13px; color:#2d5252;">Runs fully locally via Ollama — no cloud calls, no API keys.</div>
    </div>
    """, unsafe_allow_html=True)
