import os
import streamlit as st

# Streamlit Cloud Secrets 불러오기
if "UPSTAGE_API_KEY" in st.secrets:
    os.environ["UPSTAGE_API_KEY"] = st.secrets["UPSTAGE_API_KEY"]
    os.environ["PINECONE_API_KEY"] = st.secrets["PINECONE_API_KEY"]
    os.environ["PINECONE_ENVIRONMENT"] = st.secrets["PINECONE_ENVIRONMENT"]

UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
