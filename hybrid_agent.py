import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.utilities import SQLDatabase
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# ============================================================
# 1. SQL TOOL - Queries the inventory database
# ============================================================
db = SQLDatabase.from_uri("sqlite:///inventory.db")

def query_inventory_sql(question: str) -> str:
    """Converts a natural language question to SQL, runs it, returns the answer."""
    llm = ChatOpenAI(model="gpt-5-mini", temperature=0)
    
    schema = db.get_table_info()
    
    prompt = ChatPromptTemplate.from_template("""
    You are a SQL expert. Given this database schema:
    {schema}
    
    Write a SQLite query to answer: {question}
    
    Return ONLY the raw SQL query. No markdown, no explanation.
    """)
    
    sql_chain = prompt | llm | StrOutputParser()
    sql_query = sql_chain.invoke({"schema": schema, "question": question}).strip()
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    
    try:
        result = db.run(sql_query)
        
        summary_prompt = ChatPromptTemplate.from_template("""
        The user asked: {question}
        The SQL query was: {sql_query}
        The result was: {result}
        
        Provide a clear, natural language answer.
        """)
        summary_chain = summary_prompt | llm | StrOutputParser()
        return summary_chain.invoke({
            "question": question, 
            "sql_query": sql_query, 
            "result": result
        })
    except Exception as e:
        return f"SQL Error: {e}"


# ============================================================
# 2. RAG TOOL - Searches the policy documents (using FAISS)
# ============================================================
def query_policies_rag(question: str) -> str:
    """Searches grading policies for relevant information using FAISS."""
    with open("grading_policies.txt", "r") as f:
        text = f.read()
    
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.create_documents([text])
    
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever()
    
    results = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in results])
    
    llm = ChatOpenAI(model="gpt-5-mini", temperature=0)
    prompt = ChatPromptTemplate.from_template("""
    Based on the following company policy documents:
    {context}
    
    Answer this question: {question}
    
    Provide a clear, helpful answer based only on the policy information above.
    """)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"context": context, "question": question})


# ============================================================
# 3. ORCHESTRATOR - Decides which tool to use
# ============================================================
def orchestrator(query: str) -> str:
    """Main entry point. Decides whether to use SQL, RAG, or both."""
    llm = ChatOpenAI(model="gpt-5-mini", temperature=0)
    
    prompt = ChatPromptTemplate.from_template("""
    Classify this query into exactly one category:
    
    - SQL: inventory numbers, prices, counts, diamond attributes (carat, cut, color, clarity)
    - RAG: company policies, return rules, grading standards, manager approvals
    - BOTH: needs inventory data AND policy information
    
    Query: {query}
    
    Respond with exactly one word: SQL, RAG, or BOTH
    """)
    
    chain = prompt | llm | StrOutputParser()
    decision = chain.invoke({"query": query}).strip().upper()
    
    results = []
    
    if "SQL" in decision or "BOTH" in decision:
        sql_answer = query_inventory_sql(query)
        results.append(f"**📊 Inventory Data:**\n{sql_answer}")
    
    if "RAG" in decision or "BOTH" in decision:
        rag_answer = query_policies_rag(query)
        results.append(f"**📋 Policy Information:**\n{rag_answer}")
    
    if not results:
        rag_answer = query_policies_rag(query)
        results.append(f"**📋 Policy Information:**\n{rag_answer}")
    
    return "\n\n---\n\n".join(results)


if __name__ == "__main__":
    print("\n--- Test: RAG ---")
    print(orchestrator("What is the return policy for diamonds?"))
