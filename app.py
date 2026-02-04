import streamlit as st
from langchain_groq import ChatGroq  
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List

# --- 1. SETUP ---
st.set_page_config(page_title="Eklavya AI Agent Pipeline", layout="wide")
st.title("🤖 Eklavya AI: Agentic Content Generator")
st.markdown("### Powered by Llama 3 (via Groq - Free & Fast)")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Groq API Key", type="password") # Enter Groq Key here
    
    st.divider()
    st.header("Task Parameters")
    grade = st.slider("Target Grade", 1, 12, 4)
    topic = st.text_input("Topic", "Photosynthesis")
    run_btn = st.button("🚀 Run Agent Pipeline", type="primary")

if not api_key:
    st.info("Get your FREE key at console.groq.com and paste it above.")
    st.stop()

# Initialize LLM (Groq - Llama 3.3 70B is free and smart)
llm = ChatGroq(
    model="llama-3.3-70b-versatile",  
    temperature=0.7, 
    groq_api_key=api_key
)

# --- 2. DATA MODELS (Same as before) ---
class MCQ(BaseModel):
    question: str
    options: List[str]
    answer: str

class ContentOutput(BaseModel):
    explanation: str
    mcqs: List[MCQ]

class ReviewOutput(BaseModel):
    status: str = Field(description="Must be strictly 'pass' or 'fail'")
    feedback: List[str]

# --- 3. AGENT DEFINITIONS (Same Logic) ---
class GeneratorAgent:
    def __init__(self, llm):
        self.llm = llm
        self.parser = JsonOutputParser(pydantic_object=ContentOutput)

    def generate(self, grade, topic, feedback=None):
        prompt_text = """
        You are an expert educational content creator.
        Task: Create educational content for Grade {grade} on the topic '{topic}'.
        
        Requirements:
        1. Explanation must be age-appropriate.
        2. Create 3 Multiple Choice Questions (MCQs).
        3. Output MUST be valid JSON.
        """
        if feedback:
            prompt_text += f"\n\n🚨 CRITICAL FEEDBACK: {feedback}\nFIX THESE ISSUES."

        prompt_text += "\n\n{format_instructions}"

        prompt = PromptTemplate(
            template=prompt_text,
            input_variables=["grade", "topic"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        chain = prompt | self.llm | self.parser
        return chain.invoke({"grade": grade, "topic": topic})

class ReviewerAgent:
    def __init__(self, llm):
        self.llm = llm
        self.parser = JsonOutputParser(pydantic_object=ReviewOutput)

    def review(self, content_json, grade):
        prompt_text = """
        You are a strict educational content reviewer.
        Task: Review the content for Grade {grade}.
        
        Content:
        {content}
        
        Criteria:
        1. Age Appropriateness?
        2. Factual Correctness?
        3. Valid JSON format?

        Output JSON with status 'pass' or 'fail' and feedback.
        \n{format_instructions}
        """
        prompt = PromptTemplate(
            template=prompt_text,
            input_variables=["content", "grade"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        chain = prompt | self.llm | self.parser
        return chain.invoke({"content": str(content_json), "grade": grade})

# --- 4. EXECUTION ---
if run_btn:
    generator = GeneratorAgent(llm)
    reviewer = ReviewerAgent(llm)

    # Phase 1: Generation
    with st.status("🔄 Step 1: Generator Working...", expanded=True) as status:
        draft_content = generator.generate(grade, topic)
        st.subheader("Draft Output")
        st.json(draft_content)
        status.update(label="✅ Draft Generated!", state="complete")

    # Phase 2: Review
    with st.status("🧐 Step 2: Reviewer Analyzing...", expanded=True) as status:
        review_result = reviewer.review(draft_content, grade)
        st.subheader("Reviewer Report")
        st.json(review_result)
        
        if review_result['status'].lower() == 'pass':
             status.update(label="✅ Content Approved!", state="complete")
             st.balloons()
             st.success("Final Content Ready!")
        else:
             status.update(label="⚠️ Issues Found - Refining...", state="error")

    # Phase 3: Refinement
    if review_result['status'].lower() == 'fail':
        st.divider()
        with st.status("🛠️ Step 3: Refining Content...", expanded=True) as status:
            feedback_str = "; ".join(review_result['feedback'])
            refined_content = generator.generate(grade, topic, feedback=feedback_str)
            st.subheader("Refined Output")
            st.json(refined_content)
            status.update(label="✅ Refinement Complete!", state="complete")
            st.success("Refined Content Ready!")