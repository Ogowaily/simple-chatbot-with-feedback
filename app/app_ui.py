import streamlit as st
import requests

LLM_URL = "http://127.0.0.1:8000/llm"

st.title("Simple ChatBot  with Feedback")

 
if "question" not in st.session_state:
    st.session_state.question = ""
if "output" not in st.session_state:
    st.session_state.output = ""
if "token_url" not in st.session_state:
    st.session_state.token_url = ""

 
question = st.text_input("Ask a question:", st.session_state.question)

if st.button("Submit Question") and question:
    st.session_state.question = question
    with st.spinner("Getting response from LLM..."):
        response = requests.post(
            f"{LLM_URL}/invoke",
            json={"input": {"question": question}}
        ).json()

    st.session_state.output = response.get("output", "")
    feedback_tokens = response.get("metadata", {}).get("feedback_tokens", [])
    if feedback_tokens:
        st.session_state.token_url = feedback_tokens[0]["token_url"]

 
if st.session_state.output:
    st.text_area("LLM Response", value=st.session_state.output, height=150)

 
if st.session_state.token_url:
    st.success("Token ready for feedback")

    score = st.slider("Score", 0, 5, 5)
    comment = st.text_area("Comment", "Response was helpful")

    if st.button("Send Feedback"):
        feedback_data = {
            "token_or_url": st.session_state.token_url,
            "score": score,
            "value": score,
            "comment": comment,
            "correction": {},
            "metadata": {"question": st.session_state.question}
        }

        fb_response = requests.post(f"{LLM_URL}/token_feedback", json=feedback_data)
        if fb_response.status_code == 200:
            st.success("Feedback sent successfully!")
        else:
            st.error(f"Error sending feedback: {fb_response.text}")
