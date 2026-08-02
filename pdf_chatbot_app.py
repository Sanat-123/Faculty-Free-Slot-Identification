"""
=====================================================================
Faculty Free Slot Identification - PDF Chatbot
=====================================================================
A Streamlit chatbot for this project where you can upload a
faculty-wise timetable PDF directly and then chat with the bot about
free faculty, teachers, subjects, rooms, classes and timetables.

Run it with:

    pip install -r requirements.txt
    streamlit run pdf_chatbot_app.py

Then open the URL shown in the terminal (default http://localhost:8501)
"""

import os
import sys
from pathlib import Path

# ----------------------------------------------------------------
# Make project modules importable no matter where streamlit runs
# ----------------------------------------------------------------

ROOT = os.path.dirname(os.path.abspath(__file__))

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pandas as pd
import streamlit as st

from pdf_pipeline import (
    parse_faculty_pdf,
    build_database,
    activate,
    answer_query,
)

# ----------------------------------------------------------------
# Constants
# ----------------------------------------------------------------

SAMPLE_PDF = Path("data") / "Facultywise TT 20 sep.pdf"

RESULT_COLUMNS = [
    "Teacher",
    "Day",
    "Slot",
    "Subject",
    "Room",
    "Class",
    "Group",
    "Type",
]

# Intents whose result rows are rendered as a table
TABLE_INTENTS = {"SHOW_TIMETABLE", "FIND_ROOM", "FIND_SUBJECT"}

SAMPLE_QUESTIONS = [
    "Who is free on Monday slot 3?",
    "Who teaches Python?",
    "Show timetable of 3CS-DS-A",
    "Where is Python for DS Lab?",
    "Subjects of Dr. Pankaj Dadheech",
    "Which rooms are free on Tuesday slot 4?",
]

# ----------------------------------------------------------------
# Page config
# ----------------------------------------------------------------

st.set_page_config(
    page_title="Timetable PDF Chatbot",
    page_icon="📚",
    layout="wide",
)

# ----------------------------------------------------------------
# Session state
# ----------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_id" not in st.session_state:
    st.session_state.pdf_id = None

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

if "stats" not in st.session_state:
    st.session_state.stats = None


# ----------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------

def load_pdf(name: str, file_bytes: bytes) -> bool:
    """
    Parse the uploaded PDF, build a fresh SQLite database and
    activate it for the NLP engine.
    """
    try:
        with st.spinner(f"📖 Parsing `{name}` ..."):

            database = parse_faculty_pdf(file_bytes)

            db_path, stats = build_database(database)

            activate(db_path)

    except Exception as exc:

        st.sidebar.error(f"❌ Could not load the PDF.\n\n{exc}")

        # Remember this file so we don't retry it on every rerun
        st.session_state.pdf_id = (name, len(file_bytes))

        return False

    st.session_state.pdf_id = (name, len(file_bytes))
    st.session_state.pdf_name = name
    st.session_state.stats = stats
    st.session_state.messages = []

    return True


def ask(question: str) -> None:
    """
    Run one question through the NLP pipeline and store
    both user and assistant messages.
    """
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    try:

        answer = answer_query(question)

    except Exception as exc:

        answer = {
            "text": f"⚠️ Sorry, something went wrong: {exc}",
            "intent": "ERROR",
            "rows": [],
            "detection": {},
        }

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer["text"],
            "intent": answer.get("intent"),
            "rows": answer.get("rows", []),
            "detection": answer.get("detection", {}),
        }
    )


# ----------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------

with st.sidebar:

    st.title("📚 Timetable Chatbot")

    st.caption("Faculty Free Slot Identification")

    st.divider()

    # ------------------- PDF upload -------------------

    st.subheader("📄 Upload PDF")

    uploaded = st.file_uploader(
        "Faculty-wise timetable PDF",
        type=["pdf"],
        help=(
            "One page per teacher, starting with 'Teacher <Name>' "
            "and a Mo-Sa slot table — like the sample PDF."
        ),
    )

    if uploaded is not None:

        uploaded_id = (uploaded.name, uploaded.size)

        if st.session_state.pdf_id != uploaded_id:

            if load_pdf(uploaded.name, uploaded.getvalue()):
                st.rerun()

    elif st.button("📥 Load sample PDF", width="stretch"):

        if SAMPLE_PDF.exists():

            if load_pdf(SAMPLE_PDF.name, SAMPLE_PDF.read_bytes()):
                st.rerun()

        else:

            st.error("Sample PDF not found in `data/`.")

    # ------------------- Loaded stats -------------------

    if st.session_state.pdf_name:

        st.success(
            f"✅ Loaded **{st.session_state.pdf_name}**"
        )

        stats = st.session_state.stats or {}

        c1, c2 = st.columns(2)

        c1.metric("👨‍🏫 Teachers", stats.get("teachers", 0))
        c2.metric("🗓️ Records", stats.get("records", 0))

        c3, c4 = st.columns(2)

        c3.metric("📖 Subjects", stats.get("subjects", 0))
        c4.metric("🏫 Classes", stats.get("classes", 0))

    st.divider()

    # ------------------- Sample questions -------------------

    st.subheader("💡 Try asking")

    for question in SAMPLE_QUESTIONS:

        if st.button(question, key=f"sample_{question}", width="stretch"):

            ask(question)
            st.rerun()

    st.divider()

    if st.button("🗑 Clear chat", width="stretch"):

        st.session_state.messages = []
        st.rerun()

    st.caption("Powered by the project's own NLP engine "
               "(intent → entities → planner → SQLite)")


# ----------------------------------------------------------------
# Main area
# ----------------------------------------------------------------

st.title("🎓 Timetable PDF Chatbot")

if st.session_state.pdf_name:

    st.caption(
        f"Chatting with **{st.session_state.pdf_name}** — ask anything "
        "about free faculty, teachers, subjects, rooms or timetables."
    )

else:

    st.caption(
        "Upload a faculty timetable PDF on the left (or load the sample) "
        "and start asking questions."
    )

st.divider()

# ----------------------------------------------------------------
# Empty state (no PDF loaded yet)
# ----------------------------------------------------------------

if not st.session_state.pdf_name:

    col1, col2 = st.columns([1.4, 1])

    with col1:

        st.markdown(
            """
### 🚀 How it works

**1. Upload** a faculty-wise timetable PDF — one page per teacher,
starting with `Teacher <Name>` and a Mo–Sa slot table.

**2. Chat** with the bot in natural language, for example:

- 👨‍🏫 *"Who is free on Monday slot 3?"*
- 📖 *"Who teaches Python?"*
- 📅 *"Show timetable of 3CS-DS-A"*
- 🚪 *"Where is Python for DS Lab?"*
- 📋 *"Subjects of Dr. Pankaj Dadheech"*
- 🪑 *"Which rooms are free on Tuesday slot 4?"*

The PDF is parsed, cleaned and loaded into a temporary SQLite
database, and every answer comes from the project's own NLP engine.
"""
        )

    with col2:

        st.info(
            "**No PDF yet?**\n\nClick **📥 Load sample PDF** in the "
            "sidebar to try the chatbot with the bundled timetable "
            "(`data/Facultywise TT 20 sep.pdf`)."
        )

    st.stop()

# ----------------------------------------------------------------
# Chat history
# ----------------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            # ---------- Table view for structured results ----------

            rows = message.get("rows") or []

            if (
                message.get("intent") in TABLE_INTENTS
                and rows
                and isinstance(rows[0], tuple)
            ):

                st.dataframe(
                    pd.DataFrame(rows, columns=RESULT_COLUMNS),
                    width="stretch",
                    hide_index=True,
                )

            # ---------- Detection details (transparency) ----------

            detection = message.get("detection")

            if detection and detection.get("intent"):

                with st.expander("🔎 What I detected"):

                    lines = [
                        f"**Intent** : `{detection.get('intent')}`",
                        f"**Day** : {detection.get('day') or '—'}   |   "
                        f"**Slot** : {detection.get('slot') or '—'}",
                    ]

                    entities = detection.get("entities", {})

                    for entity_type, values in entities.items():

                        if values:
                            lines.append(
                                f"**{entity_type.title()}** : "
                                + ", ".join(str(v) for v in values)
                            )

                    st.markdown("\n\n".join(lines))

# ----------------------------------------------------------------
# Chat input
# ----------------------------------------------------------------

prompt = st.chat_input(
    "Ask about the timetable, e.g. 'Who is free on Monday slot 3?'"
)

if prompt:

    ask(prompt)
    st.rerun()
