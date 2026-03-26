import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = init_chat_model("gpt-4o-mini", model_provider="openai")

st.title('Lab 6: Movie Recommendation Chatbot')

st.sidebar.selectbox('Select a movie genre:', ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi'], key='genre')
st.sidebar.selectbox('Select a mood:', ['Happy', 'Sad', 'Excited', 'Relaxed'], key='mood')
st.sidebar.selectbox('Select a persona:',  ['Film Critic', 'Casual Friend', 'Movie Journalist'], key='persona')

template = PromptTemplate(
    input_variables=['genre', 'mood', 'persona'],
    template=(
        "You are a {persona} who loves movies. Recommend 3 movies that fit the below criteria:\n"
        "- Genre: {genre}\n"
        "- Mood: {mood}\n"
        "Please provide a brief explanation for your recommendations."
    )
)

chain = template | llm | StrOutputParser()

if "last_recommendation" not in st.session_state:
    st.session_state.last_recommendation = None

if st.button('Get Movie Recommendations'):
    st.session_state.last_recommendation = chain.invoke({
        "genre": st.session_state.genre,
        "mood": st.session_state.mood,
        "persona": st.session_state.persona
    })
    st.write(st.session_state.last_recommendation)

st.divider()
follow_up = st.text_input('Ask a follow-up question about these movies:')

followup_prompt = PromptTemplate(  
    input_variables=['recommendations', 'question'],
    template="Based on the following movie recommendations:\n{recommendations}\nAnswer the following question: {question}"
)

followup_chain = followup_prompt | llm | StrOutputParser()

if follow_up:
    if not st.session_state.last_recommendation:
        st.warning('Please get movie recommendations first!')
    else:
        answer = followup_chain.invoke({
            "recommendations": st.session_state.last_recommendation,
            "question": follow_up
        })
        st.write(answer)

