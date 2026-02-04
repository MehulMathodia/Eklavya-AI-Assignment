# Eklavya AI: Agentic Content Generator

## 📌 Overview
**Eklavya AI** is an **Agentic AI Pipeline** designed to generate structured, age-appropriate educational content.  
It follows a **Generator–Reviewer architecture** with an automated **self-correction loop**, ensuring high-quality and strictly formatted outputs.

The system is built using **LangChain** and **Llama 3 (via Groq)** and produces educational explanations and MCQs in **valid JSON format**, making it easy to integrate with frontend or downstream systems.

---

## 🚀 Key Features
- **Generator Agent**  
  Generates draft educational content (Explanations + MCQs) based on the selected Grade and Topic.

- **Reviewer Agent**  
  Reviews the generated content for:
  - Age-appropriateness  
  - Factual accuracy  
  - Strict JSON validity  

- **Automated Refinement Loop**  
  If the Reviewer flags issues (e.g., content is too complex), feedback is sent back to the Generator, which regenerates a corrected version automatically.

- **Structured Output**  
  Ensures all final outputs follow a strict JSON schema for seamless frontend integration.

- **Real-Time UI**  
  Built using **Streamlit** for instant interaction and visualization of the agent workflow.

---

## 🛠️ Tech Stack
- **Language:** Python  
- **Framework:** LangChain (Agent logic)  
- **LLM:** Llama 3 (via Groq API for high-speed inference)  
- **Interface:** Streamlit  
- **Validation:** Pydantic (structured data enforcement)

---

## ⚙️ Installation & Setup

### 1. Get a Free Groq API Key
1. Visit: https://console.groq.com/keys  
2. Log in using Google or GitHub  
3. Click **Create API Key**  
4. Copy the key (starts with `gsk_...`)  

---

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 3. Run the Application
```bash
python -m streamlit run app.py
```

---

### 4. Enter Credentials
- App opens at `http://localhost:8501`
- Paste your Groq API Key in the sidebar

---

## 📂 Project Structure
```
.
├── app.py
├── requirements.txt
├── README.md
```

---

## 🧪 Usage Examples

### Example 1: Normal Flow
- Grade: 4  
- Topic: Photosynthesis  

Approved in one pass.

### Example 2: Refinement Loop
- Grade: 1  
- Topic: Quantum Physics  

Automatically simplified and regenerated.

---

## 👤 Author
**Submitted by:** Mehul Mathodia
