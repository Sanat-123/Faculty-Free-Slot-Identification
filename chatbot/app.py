import streamlit as st
from intents import process_query

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="University Analytics Assistant",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("🎓 University Analytics")

    st.divider()

    st.subheader("📊 Database")

    st.success("PostgreSQL Connected")

    st.divider()

    st.subheader("💡 Sample Questions")

    st.markdown("""
- total students
- total faculty
- list departments
- highest package
- average package
- companies
- books
- attendance S0001
- fee S0001
- hostel summary
""")

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []
        st.rerun()

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎓 University Analytics Assistant")

st.caption(
    "Ask anything about Students, Faculty, Placements, Library, Attendance, Fees or Hostel."
)

st.divider()

# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

prompt = st.chat_input("Ask your question...")

if prompt:

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    response = process_query(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )