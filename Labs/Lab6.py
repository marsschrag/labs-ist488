import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

init_chat_model('claude-haiku-4-5-20251001')

st.title('Lab 6: Movie Recommendation Chatbot')

st.sidebar.selectbox('Select a movie genre:', ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi'], key='genre')
st.sidebar.selectbox('Select a mood:', ['Happy', 'Sad', 'Excited', 'Relaxed'], key='mood')
st.sidebar.selectbox('Select a persona:',  ['Film Critic', 'Casual Friend', 'Movie Journalist'], key='persona')

PromptTemplate(
    input_variables=['genre', 'mood', 'persona'],
    template=(
        "You are a {persona} who loves movies. Recommend 3 movies that fit the below criteria:\n"
        "- Genre: {genre}\n"
        "- Mood: {mood}\n"
        "Please provide a brief explanation for your recommendations."
    )
).format(
    genre=st.session_state.genre,
    mood=st.session_state.mood,
    persona=st.session_state.persona
)

#part b step 3 is next


