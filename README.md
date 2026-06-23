# 🧠 AI Agent CI/CD Project (Langflow + DLQ + GitHub Actions)

This project demonstrates a **robust AI agent architecture** with:

- Langflow workflow execution
- External API integration (Wikipedia simulation)
- Smart failure handling (DLQ - Dead Letter Queue)
- Automated testing with pytest
- CI/CD pipeline using GitHub Actions

---

# 🚀 Project Goal

The goal of this project is to ensure that:

> ❗ If an external API (like Wikipedia) fails, the AI system does NOT crash  
> Instead, the request is redirected to a **DLQ (quarantine system)** and monitored.

---

# 🏗️ Architecture
