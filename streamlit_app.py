import streamlit as st
import json

# =====================================
# DIRECT IMPORTS (no FastAPI needed)
# =====================================

from main import solve_question
from memory import memory_manager

# =====================================
# CONFIG
# =====================================

st.set_page_config(
    page_title="Student Study Helper",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #F8F7F4;
}

[data-testid="stSidebar"] {
    background-color: #1C1C1E !important;
    border-right: none;
}
[data-testid="stSidebar"] * {
    color: #E5E5EA !important;
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #FFFFFF !important;
    font-size: 13px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 600;
}

.study-header {
    padding: 2.5rem 0 1.5rem;
    border-bottom: 1px solid #E4E2DA;
    margin-bottom: 2rem;
}
.study-header h1 {
    font-size: 28px;
    font-weight: 600;
    color: #1C1C1E;
    margin: 0 0 6px;
    letter-spacing: -0.5px;
}
.study-header p {
    font-size: 15px;
    color: #6B6B6B;
    margin: 0;
}

.topic-badge {
    display: inline-block;
    background: #EEF0FB;
    color: #3C3489;
    font-size: 12px;
    font-weight: 500;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 0.02em;
    margin-bottom: 1.25rem;
}

.conf-high   { background: #EAF3DE; color: #27500A; }
.conf-medium { background: #FAEEDA; color: #633806; }
.conf-low    { background: #FCEBEB; color: #791F1F; }
.conf-badge {
    display: inline-block;
    font-size: 12px;
    font-weight: 500;
    padding: 4px 12px;
    border-radius: 20px;
    margin-left: 10px;
}

.step-tile {
    display: flex;
    gap: 16px;
    align-items: flex-start;
    padding: 16px 20px;
    background: #FFFFFF;
    border: 1px solid #E4E2DA;
    border-radius: 12px;
    margin-bottom: 10px;
}
.step-number {
    flex-shrink: 0;
    width: 28px;
    height: 28px;
    background: #1C1C1E;
    color: #FFFFFF;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}
.step-text {
    font-size: 15px;
    color: #1C1C1E;
    line-height: 1.6;
    margin: 2px 0 0;
}

.final-answer-box {
    background: #1C1C1E;
    color: #F8F7F4;
    border-radius: 12px;
    padding: 20px 24px;
    margin-top: 1.5rem;
    font-size: 16px;
    line-height: 1.6;
}
.final-answer-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #8E8E93;
    margin-bottom: 8px;
}

.rejected-box {
    background: #FCEBEB;
    border: 1px solid #F7C1C1;
    border-radius: 12px;
    padding: 16px 20px;
    color: #791F1F;
    font-size: 15px;
}

/* ── JSON panel ── */
.json-panel {
    background: #1C1C1E;
    border-radius: 12px;
    padding: 20px;
    height: 100%;
}
.json-panel-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #636366;
    margin-bottom: 14px;
}

/* Override Streamlit's st.json background inside the dark panel */
.json-panel [data-testid="stJson"] {
    background: transparent !important;
}

.col-divider {
    border-left: 1px solid #E4E2DA;
    padding-left: 2rem;
}

.hist-card {
    background: #2C2C2E;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 8px;
}
.hist-q {
    font-size: 13px;
    color: #E5E5EA !important;
    font-weight: 500;
    margin-bottom: 4px;
}
.hist-a {
    font-size: 12px;
    color: #8E8E93 !important;
    line-height: 1.4;
}

.stTextArea textarea {
    border: 1.5px solid #E4E2DA !important;
    border-radius: 10px !important;
    background: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    color: #1C1C1E !important;
    padding: 14px 16px !important;
    resize: vertical;
}
.stTextArea textarea:focus {
    border-color: #3C3489 !important;
    box-shadow: 0 0 0 3px rgba(83, 74, 183, 0.12) !important;
}

.stButton > button {
    background: #1C1C1E !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 28px !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    width: 100% !important;
    transition: opacity 0.15s ease !important;
}
.stButton > button:hover {
    opacity: 0.85 !important;
}

hr { border-color: #E4E2DA; }

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# =====================================
# SESSION STATE
# =====================================

if "session_id" not in st.session_state:
    st.session_state.session_id = "student_001"

if "history" not in st.session_state:
    st.session_state.history = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = ""

if "auto_solve" not in st.session_state:
    st.session_state.auto_solve = False

if "last_result" not in st.session_state:
    st.session_state.last_result = None

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:
    st.markdown("### 📐 Study Helper")
    st.markdown("---")
    st.markdown("#### History")

    if not st.session_state.history:
        st.markdown(
            "<p style='color:#636366;font-size:13px;'>No questions yet.</p>",
            unsafe_allow_html=True
        )
    else:
        for item in reversed(st.session_state.history):
            q_preview = item["question"][:60] + ("…" if len(item["question"]) > 60 else "")
            a_preview = item["answer"].get("final_answer", "")[:80] + "…"
            st.markdown(f"""
            <div class="hist-card">
                <div class="hist-q">{q_preview}</div>
                <div class="hist-a">{a_preview}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("Clear history"):
        st.session_state.history = []
        st.session_state.last_result = None
        memory_manager.clear(st.session_state.session_id)
        st.rerun()

    st.markdown(
        "<p style='color:#636366;font-size:12px;margin-top:2rem;'>"
        "Covers: Maths · Statistics · Calculus · Algebra · Probability · Linear Algebra"
        "</p>",
        unsafe_allow_html=True
    )

# =====================================
# HEADER
# =====================================

st.markdown("""
<div class="study-header">
    <h1>Student Study Helper</h1>
    <p>Ask a maths or statistics question and get a clear, step-by-step solution.</p>
</div>
""", unsafe_allow_html=True)

# =====================================
# EXAMPLE CHIPS
# =====================================

st.markdown(
    "<p style='font-size:13px;color:#6B6B6B;margin-bottom:8px;'>Try an example</p>",
    unsafe_allow_html=True
)

examples = [
    "Find the mean of 2, 4, 6, 8, 10",
    "Differentiate x² + 5x + 1",
    "Explain Bayes' theorem",
    "Calculate variance of 1, 2, 3, 4, 5",
]

cols = st.columns(len(examples))
for col, ex in zip(cols, examples):
    with col:
        if st.button(ex, key=f"ex_{ex}"):
            st.session_state.pending_question = ex
            st.session_state.auto_solve = True
            st.rerun()

st.markdown("<div style='margin-bottom:1rem'></div>", unsafe_allow_html=True)

# =====================================
# INPUT
# =====================================

question = st.text_area(
    "Your question",
    value=st.session_state.pending_question,
    height=130,
    placeholder="e.g. What is the standard deviation of 3, 7, 7, 19?",
    label_visibility="collapsed",
    key="question_input"
)

st.markdown("<div style='margin-bottom:0.5rem'></div>", unsafe_allow_html=True)

solve_clicked = st.button("Solve →")

if question != st.session_state.pending_question:
    st.session_state.pending_question = question

# =====================================
# SOLVE
# =====================================

should_solve = solve_clicked or st.session_state.auto_solve

if st.session_state.auto_solve:
    st.session_state.auto_solve = False

if should_solve:
    if not question.strip():
        st.warning("Enter a question first.")
    else:
        with st.spinner("Working through it…"):
            result = solve_question(
                question=question,
                session_id=st.session_state.session_id
            )
        st.session_state.last_result = result
        st.session_state.history.append({
            "question": question,
            "answer": result
        })

# =====================================
# RESULTS — two columns: UI  |  JSON
# =====================================

if st.session_state.last_result:

    result = st.session_state.last_result
    topic        = result.get("topic", "")
    steps        = result.get("steps", [])
    final_answer = result.get("final_answer", "")
    confidence   = result.get("confidence", "")
    is_rejected  = topic == "Rejected"

    st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:11px;font-weight:600;color:#6B6B6B;"
        "letter-spacing:0.08em;text-transform:uppercase;"
        "margin-bottom:1rem;'>Result</p>",
        unsafe_allow_html=True
    )

    left_col, right_col = st.columns([3, 2], gap="large")

    # ── LEFT: styled solution ──────────────────────
    with left_col:

        if is_rejected:
            st.markdown(f"""
            <div class="rejected-box">
                <strong>Question not accepted</strong><br>{final_answer}
            </div>
            """, unsafe_allow_html=True)

        else:
            conf_class = (
                "conf-high"   if str(confidence).lower() == "high"
                else "conf-medium" if str(confidence).lower() == "medium"
                else "conf-low"
            )
            st.markdown(f"""
            <div style="margin-bottom:1rem;">
                <span class="topic-badge">{topic}</span>
                <span class="conf-badge {conf_class}">{confidence} confidence</span>
            </div>
            """, unsafe_allow_html=True)

            if steps:
                st.markdown(
                    "<p style='font-size:11px;font-weight:600;color:#1C1C1E;"
                    "letter-spacing:0.08em;text-transform:uppercase;"
                    "margin:0 0 0.75rem;'>Solution steps</p>",
                    unsafe_allow_html=True
                )
                for i, step in enumerate(steps, start=1):
                    st.markdown(f"""
                    <div class="step-tile">
                        <div class="step-number">{i}</div>
                        <div class="step-text">{step}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="final-answer-box">
                <div class="final-answer-label">Answer</div>
                {final_answer}
            </div>
            """, unsafe_allow_html=True)

    # ── RIGHT: raw JSON ────────────────────────────
    with right_col:
        st.markdown(
            "<p style='font-size:11px;font-weight:600;color:#6B6B6B;"
            "letter-spacing:0.08em;text-transform:uppercase;"
            "margin-bottom:0.75rem;'>Raw JSON output</p>",
            unsafe_allow_html=True
        )
        st.code(
            json.dumps(result, indent=2),
            language="json"
        )