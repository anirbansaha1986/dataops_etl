import streamlit as st
from rag.agent import ask_agent

st.set_page_config(page_title="DataOps AI Agent", layout="wide")

st.title("🤖 DataOps AI Agent")

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Input
user_input = st.text_input("Ask your question:")

if st.button("Submit"):

    if user_input:

        with st.spinner("Thinking..."):
            answer = ask_agent(user_input)

        st.session_state.history.append((user_input, answer))

# Display history
for q, a in reversed(st.session_state.history):

    st.markdown(f"**🧑 {q}**")
    st.markdown(f"**🤖 {a}**")
    st.markdown("---")