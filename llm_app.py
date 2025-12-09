# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 11:19:34 2025

@author: mohse
"""

# -*- coding: utf-8 -*-
"""
Project 2: Web-Based LLM App
Created on Wed Dec  3 15:41:33 2025

@author: mpashna
"""

import streamlit as st
import re
from PyPDF2 import PdfReader
from groq import Groq

# 1. Initialize Groq client for closed-source LLM (Question 4)
# For local testing, paste your key directly.
# For deployment on Streamlit Cloud, you will use:
# client = Groq(api_key=st.secrets["GROQ_API_KEY"])
client = Groq(api_key=st.secrets["GROQ_API_KEY"])



def answer_with_llm(question, context):
    """
    Send question + context to Groq's Llama-3 model and return the answer.
    """
    prompt = f"""
    You are a helpful assistant. Use the following article text to answer the user's question.
    If the answer is not contained in the text, say you don't know.

    Article text:
    {context}

    Question: {question}
    """

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content


# 2. Page layout
st.title("Project 2: Web-Based LLM App")

st.header("Input to AI (Question 1)")

# Text box for the user question
user_question = st.text_input("Enter your question:")

# File uploader for articles (can upload multiple PDFs for Q2)
uploaded_files = st.file_uploader(
    "Upload article(s) (optional, PDF or TXT):",
    type=["txt", "pdf"],
    accept_multiple_files=True
)

st.markdown("---")
st.subheader("AI Response (Question 1)")


# 3. Helper function to turn uploaded file into text
def read_uploaded_file(file):
    if file is None:
        return ""

    # Always reset pointer to the start in case fi
