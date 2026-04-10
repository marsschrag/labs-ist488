import streamlit as st

st.title('Lab 8: Document Retrieval and Reranking')

st.write('Use the query box below to retrieve the top matching documents and rerank them based on keyword overlap and date relevance.')

query = st.text_input('Question', value='When is the midterm?')

if 'docs' not in st.session_state:
    st.session_state.docs = [
        'The midterm exam will be held on October 14 during class time.',
        'Homework 3 is due before the midterm review session.',
        'The final project rubric is posted on Blackboard.',
        'Office hours are Tuesdays from 3–5 PM.',
        'The midterm review session will cover Chapters 1 through 4.',
        'Quiz 2 covers retrieval, embeddings, and reranking.',
    ]

with st.expander('Document library', expanded=False):
    for idx, doc in enumerate(st.session_state.docs, start=1):
        st.write(f'{idx}. {doc}')


def retrieval_score(query, doc):
    query_words = set(query.lower().split())
    doc_words = set(doc.lower().split())
    return len(query_words & doc_words)


def rerank_score(doc):
    score = 0
    doc_lower = doc.lower()
    if 'midterm' in doc_lower:
        score += 2
    if 'exam' in doc_lower:
        score += 2
    if any(char.isdigit() for char in doc):
        score += 3
    return score

if query.strip() == '':
    st.warning('Please type a query to see retrieval results.')
else:
    scored_docs = [(doc, retrieval_score(query, doc)) for doc in st.session_state.docs]
    scored_docs.sort(key=lambda x: x[1], reverse=True)
    top3 = scored_docs[:3]

    st.subheader('Top 3 retrieval results')
    for rank, (doc, score) in enumerate(top3, 1):
        st.markdown(f'**Rank {rank}**  \n- Score: {score}  \n- Document: {doc}')

    reranked = [(doc, rerank_score(doc)) for doc, _ in top3]
    reranked.sort(key=lambda x: x[1], reverse=True)

    st.subheader('Reranked top 3')
    for rank, (doc, score) in enumerate(reranked, 1):
        st.markdown(f'**Rank {rank}**  \n- Rerank score: {score}  \n- Document: {doc}')

    final_answer = reranked[0][0] if reranked else 'No answer available.'
    st.success('Final answer:')
    st.write(final_answer)
