import streamlit as st
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.llms import Ollama
import chromadb
import os
import argparse
import time
from readpdf import main

model =  "mistral:7b"
# For embeddings model, the example uses a sentence-transformers model
# https://www.sbert.net/docs/pretrained_models.html  - check for mode models
# "we can also use "all-mpnet-base-v2" model which provides the best quality, but all-MiniLM-L6-v2 is many times faster and still offers good quality."
if "embeddings_model_name" not in st.session_state:
    st.session_state["embeddings_model_name"] = "all-MiniLM-L6-v2"
if "persist_directory" not in st.session_state:
    st.session_state["persist_directory"] = "vector_db"
if "target_source_chunks" not in st.session_state:
    st.session_state["target_source_chunks"] = 4

from constants import CHROMA_SETTINGS


tab1, tab2 = st.tabs(["Data Indexer", "Chat"])

with tab1:
    uploaded_files = st.file_uploader("Upload the RFP/RFI documents", type = "pdf", accept_multiple_files = True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Save each file to the specified directory
            with open(os.path.join("my_pdfs", uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
        main()
        st.success(f"Files have been successfully saved and indexed")
with tab2:
    st.title("RFP Q&A")
    embeddings = HuggingFaceEmbeddings(model_name= st.session_state["embeddings_model_name"])

    db = Chroma(persist_directory=st.session_state["persist_directory"], embedding_function=embeddings)

    retriever = db.as_retriever(search_kwargs={"k": st.session_state["target_source_chunks"]})
    # # activate/deactivate the streaming StdOut callback for LLMs
    callbacks = [StreamingStdOutCallbackHandler()]

    llm = Ollama(model=model, callbacks=callbacks)

    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            res = qa(prompt)
            answer = res['result']
            response = st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": response})