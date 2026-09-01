# 🔍 Agentic AI Code Reviewer

An automated, low-latency AI Code Review Agent powered by **Groq Cloud API (Llama-3.3-70B)** and **Streamlit**. It autonomously parses code diffs, pull request snippets, and script files to detect bugs, assess security vulnerabilities, and generate structured engineering audit reports.

## 🚀 Live Demo
🔗 [Click Here to View Live App](https://agentic-code-reviewer-c343x2yqw.streamlit.app)

## ✨ Core Features & Agentic Architecture
* **Autonomous Code Audit:** Operates as a senior engineering agent analyzing git diffs across multiple review lenses (Full Audit, Bug & Security Focus, Performance & Refactoring).
* **Structured Output Parsing:** Enforces clear, deterministic reporting layout—delivering Executive Summaries, Bug/Vulnerability tracking, and refactored code blocks.
* **Resilient Input Processing:** UTF-8 sanitization engine to seamlessly handle raw git patches, special characters, and code comments without encoding crashes.
* **Ultra-Fast Inference:** Leverages Groq's high-speed inference engine (`llama-3.3-70b-versatile`) with low temperature settings ($0.2$) for reliable technical analysis.

## 🛠️ Tech Stack & Skills Demonstrated
* **Agentic AI & Orchestration:** System-prompted autonomous review workflow
* **LLM Engine:** Groq Cloud API (`llama-3.3-70b-versatile`)
* **Code Parsing:** Git diff processing & UTF-8 character sanitization
* **UI & Deployment:** Streamlit Cloud
