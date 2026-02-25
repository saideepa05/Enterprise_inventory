import streamlit as st
import os
import pandas as pd

st.set_page_config(page_title="Enterprise Intelligence", layout="wide", page_icon="💎")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Styling for the main title */
    .main-header {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        margin-bottom: 0.5rem;
    }
    
    /* Subtle subtitle */
    .sub-header {
        color: #64748B;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Sidebar styling for visibility */
    [data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Force white text in sidebar for contrast */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] span {
        color: white !important;
    }

    /* Style for the 'info' boxes in sidebar */
    [data-testid="stSidebar"] .stAlert {
        background-color: rgba(30, 58, 138, 0.4);
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Chat message container improvement */
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown('<h1 class="main-header">Enterprise Intelligence</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Hybrid AI Agent bridging SQL Performance & RAG Knowledge.</p>', unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("Project Overview")
    st.markdown("""
    **Architecture:**  
    - **Brain:** GPT-5-Mini  
    - **Data:** SQL + RAG
    - **Logic:** LCEL Orchestration
    """)
    
    csv_path = "diamonds.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        st.markdown(f"📊 **Inventory Size:** {len(df):,} items")
        st.markdown(f"💰 **Max Price:** ${df['price'].max():,}")
    
    st.divider()
    st.subheader("Try These Queries")
    
    # Handle button clicks by setting a session state trigger
    if st.button("How many Ideal cut diamonds?"):
        st.session_state.trigger_query = "How many Ideal cut diamonds do we have?"
    
    if st.button("What is the return policy?"):
        st.session_state.trigger_query = "What is the return policy for diamonds?"
        
    if st.button("Expensive Item Approval?"):
        st.session_state.trigger_query = "What is the price of the most expensive diamond and do I need manager approval to sell it?"

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- PROCESSING LOGIC ---
def process_query(q):
    with st.chat_message("user"):
        st.markdown(q)
    st.session_state.messages.append({"role": "user", "content": q})
    
    with st.chat_message("assistant"):
        with st.spinner("🧠 Orchestrating AI Tools..."):
            try:
                from hybrid_agent import orchestrator
                response = orchestrator(q)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"⚠️ **Error:** {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Check for sidebar button triggers
if "trigger_query" in st.session_state:
    query = st.session_state.trigger_query
    del st.session_state.trigger_query
    process_query(query)

# Main chat input
if prompt := st.chat_input("Query the system..."):
    process_query(prompt)
