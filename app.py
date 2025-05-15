import streamlit as st
from qa_chain_mistral import build_qa_chain

# Initialize QA Chain (load once, not every time)
@st.cache_resource
def load_qa():
    return build_qa_chain()

qa_chain = load_qa()

# Streamlit UI
st.set_page_config(page_title="JSOM AI Chatbot", page_icon="🎓", layout="wide")

st.title("🎓 JSOM AI Assistant")
st.caption("Ask anything about the Jindal School of Management!")

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
query = st.chat_input("Type your question here...")

if query:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    # Query QA chain
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = qa_chain(query)
            answer = response["result"]
            sources = response.get("source_documents", [])

            st.markdown(answer)

            if sources:
                st.markdown("---")
                st.markdown("**Sources:**")
                for doc in sources:
                    url = doc.metadata.get("source_url", "Unknown URL")
                    st.markdown(f"- [{url}]({url})")

    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": answer})
