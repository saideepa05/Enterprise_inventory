import streamlit as st
import os
import pandas as pd

st.set_page_config(page_title="Enterprise Intelligence", layout="wide")

st.title("Enterprise Inventory & Policy Intelligence")
st.markdown("""
This production-level hybrid agent combines **SQL (Structured Data)** and **RAG (Unstructured Policies)** 
to answer enterprise-level questions.
""")

# Sidebar
with st.sidebar:
    st.header("Project Info")
    st.info("""
    **How it works:**  
    - **SQL**: For numbers, prices, counts  
    - **RAG**: For policies, rules, approvals
    """)
    
    csv_path = "diamonds.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        st.write(f"Inventory size: **{len(df):,}** items")
    
    st.header("Try These Queries")
    st.markdown("""
    1. *How many Ideal cut diamonds do we have?*
    2. *What is the return policy?*
    3. *What is the most expensive diamond and do I need manager approval?*
    """)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask about inventory or policies..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                from hybrid_agent import orchestrator
                response = orchestrator(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"Error: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
