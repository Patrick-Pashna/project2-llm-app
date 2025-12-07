# -*- coding: utf-8 -*-
"""
Created on Wed Dec  3 15:41:33 2025

@author: mpashna
"""

import streamlit as st
from transformers import pipeline

# 1. Load an open-source question-answering model
qa_model = pipeline(
    "question-answering",
    model="deepset/roberta-base-squad2"
)

# 2. Page layout
st.title("Project 2: Web-Based LLM App")

st.header("Input to AI")

# Text box for the user question
user_question = st.text_input("Enter your question:")

# File uploader for an optional document
uploaded_file = st.file_uploader(
    "Upload attachment (optional):",
    type=["txt", "pdf", "docx", "html"]
)

st.markdown("---")
st.subheader("AI Response:")

# 3. Helper function to turn uploaded file into text
def read_uploaded_file(file):
    if file is None:
        return ""

    data = file.read()

    # Try to decode bytes as UTF-8 text
    try:
        return data.decode("utf-8", errors="ignore")
    except AttributeError:
        # If it's already a string
        return str(data)
    except UnicodeDecodeError:
        # If decoding fails (e.g., binary PDF), just ignore
        return ""

# 4. Button logic – call the model when clicked
if st.button("Ask AI"):
    if not user_question.strip():
        st.warning("Please enter a question.")
    else:
        # Read context from uploaded file (if any)
        context_text = read_uploaded_file(uploaded_file)
         # Limit context to first 20,000 characters to keep it manageable
        max_chars = 20000
        context_text = context_text[:max_chars]

        # If there is no usable context, tell the model to answer directly
        if not context_text.strip():
            context_text = (
                "No document was provided or it could not be read as text. "
                "Answer the user's question directly using your general knowledge."
            )

        with st.spinner("Thinking..."):
            result = qa_model(
                question=user_question,
                context=context_text
            )

        answer = result.get("answer", "(No answer returned.)")
        st.write(answer)
