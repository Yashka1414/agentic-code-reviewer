import streamlit as st
import sqlite3
from groq import Groq

st.set_page_config(page_title="Text-to-SQL Enterprise Engine", page_icon="🗄️", layout="wide")
st.title("🗄️ Text-to-SQL Engine & Query Executor")

# Security & API Setup
st.sidebar.header("⚙️ API Configuration")
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")
if not api_key:
    st.info("Please enter your Groq API Key in the sidebar to run SQL synthesis.")
    st.stop()

try:
    client = Groq(api_key=api_key)
except Exception as e:
    st.error(f"Authentication Error: {str(e)}")
    st.stop()

# In-Memory SQLite Setup for Real Query Execution
@st.cache_resource
def init_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            department TEXT,
            salary REAL
        )
    """)
    cursor.executemany("""
        INSERT INTO employees VALUES (?, ?, ?, ?)
    """, [
        (1, "Alice", "Engineering", 95000),
        (2, "Bob", "Sales", 65000),
        (3, "Charlie", "Engineering", 110000),
        (4, "Diana", "Marketing", 72000)
    ])
    conn.commit()
    return conn

conn = init_db()

st.subheader("📋 Active Database Schema (`employees`)")
st.code("""
TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary REAL
)
""", language="sql")

query_input = st.text_input("Ask a natural language question (e.g., 'What is the average salary in Engineering?'):")

if st.button("Generate & Execute SQL") and query_input:
    with st.spinner("Translating natural language to SQL query..."):
        system_prompt = (
            "You are an expert SQL Data Engineer. Translate the user's natural language request into valid SQLite code. "
            "Output ONLY the raw SQL query inside SQL code block. Do not add markdown text outside code block."
        )

        try:
            # Using active, production-stable Groq Model ID
            res = client.chat.completions.create(
                model="openai/gpt-oss-20b",  # updated: llama3-8b-8192 was decommissioned by Groq
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Schema: employees(id, name, department, salary)\nRequest: {query_input}"}
                ],
                temperature=0.1
            )

            raw_sql = res.choices[0].message.content.strip().replace("```sql", "").replace("```", "").strip()

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🛠️ Generated SQL Query")
                st.code(raw_sql, language="sql")

            with col2:
                st.markdown("### 📊 Database Results")
                try:
                    cursor = conn.cursor()
                    cursor.execute(raw_sql)
                    results = cursor.fetchall()
                    cols = [desc[0] for desc in cursor.description] if cursor.description else []
                    st.dataframe(results, use_container_width=True)
                except Exception as sql_err:
                    st.error(f"SQL Execution Error: {str(sql_err)}")

        except Exception as e:
            st.error(f"REST API Execution Error: {str(e)}")
