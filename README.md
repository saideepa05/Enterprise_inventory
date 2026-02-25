# Enterprise Inventory & Policy Intelligence 

A production-grade Hybrid AI Agent that bridges the gap between structured relational data (SQL) and unstructured corporate knowledge (RAG). Built with **LangChain**, **GPT-5-Mini**, and **Streamlit**.

##  Key Features
- **Hybrid AI Orchestration**: A smart decision layer that automatically routes queries between SQL and RAG tools based on user intent.
- **SQL Intelligence**: Natural language querying of a 50k+ record diamond inventory database (SQLite).
- **RAG Capability**: Semantic search across corporate policy documents using **FAISS** vector store.
- **Premium Dashboard**: A professional Streamlit UI with custom CSS, glassmorphism, and responsive design.
- **Optimized Performance**: Modular architecture with efficient tool-calling and response synthesis.

##  Tech Stack
- **LLM**: GPT-5-Mini (via OpenAI)
- **Framework**: LangChain (LCEL)
- **Vector Store**: FAISS
- **Database**: SQLite
- **UI**: Streamlit
- **Data**: Pandas / Requests

##  Project Structure
- `app.py`: The main dashboard and user interface.
- `hybrid_agent.py`: The core "Brain" containing the orchestrator, SQL, and RAG logic.
- `setup_data.py`: Script to download the raw external dataset.
- `init_inventory_db.py`: ETL script to transform CSV data into a SQL database.
- `grading_policies.txt`: Sample company handbook for RAG retrieval.
- `requirements.txt`: Python dependencies.

##  Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/saideepa05/Enterprise_inventory.git
   cd Enterprise_inventory
   ```

2. **Set up Environment Variables**:
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Data**:
   Download the dataset and create the local SQLite database:
   ```bash
   python setup_data.py
   python init_inventory_db.py
   ```

5. **Launch the App**:
   ```bash
   python -m streamlit run app.py
   ```

##  Example Queries
- **SQL**: "What is the average price of Ideal cut diamonds?"
- **RAG**: "What is the restocking fee for high-end returns?"
- **Hybrid**: "Find the price of the most expensive diamond and tell me if I need manager approval to sell it."

---
*Developed for the UPSKILL LangChain program.*
