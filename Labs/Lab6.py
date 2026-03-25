import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

init_chat_model('claude-haiku-4-5-20251001')

st.title('Lab 6: Movie Recommendation Chatbot')

