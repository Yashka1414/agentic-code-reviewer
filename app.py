import streamlit as st
from groq import Groq

st.set_page_config(page_title="Agentic AI Code Reviewer", page_icon="🔍", layout="wide")
st.title("🔍 Agentic AI Code Reviewer")

api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")
review_depth = st.sidebar.selectbox("Review Focus:", ["Full Audit", "Bug & Security Focus", "Performance & Refactor"])

if not api_key:
    st.info("Please enter your Groq API Key in the sidebar to start.")
    st.stop()

client = Groq(api_key=api_key)

code_diff = st.text_area("Paste Code / GitHub Diff here:", height=220, placeholder="Paste your python code, git diff, or pull request changes...")

if st.button("Run Agentic Review") and code_diff:
    system_prompt = (
        "You are an Expert Principal Software Engineer acting as an Automated Code Review Agent. "
        "Analyze the provided code diff/snippet and generate a structured review with:\n"
        "1. Executive Summary & Design Understanding\n"
        "2. Bug & Vulnerability Identification\n"
        "3. Performance & Code Quality Suggestions\n"
        "4. Refactored / Corrected Code Block\n"
        "Be concise, actionable, and clear."
    )

    with st.spinner("Analyzing code diff & executing agentic review..."):
        try:
            # Clean string encoding to prevent ASCII codec issues with emojis
            clean_input = code_diff.encode("utf-8", errors="ignore").decode("utf-8")
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Review Focus: {review_depth}\n\nCode Diff:\n{clean_input}"}
                ],
                temperature=0.2
            )
            
            st.success("Review Complete!")
            st.markdown("### 📋 Agent Code Review Report")
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error executing review: {e}")
