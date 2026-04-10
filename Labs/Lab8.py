docs = [
    "The midterm exam will be held on October 14 during class time.",
    "Homework 3 is due before the midterm review session.",
    "The final project rubric is posted on Blackboard.",
    "Office hours are Tuesdays from 3–5 PM.",
    "The midterm review session will cover Chapters 1 through 4.",
    "Quiz 2 covers retrieval, embeddings, and reranking.",
]

query = "When is the midterm?"

def retrieval_score(query, doc):
    query_words = set(query.lower().split())
    doc_words   = set(doc.lower().split())
    return len(query_words & doc_words)

print("top 3 retrieval documents (by keyword overlap)")

scored_docs = [(doc, retrieval_score(query, doc)) for doc in docs]
scored_docs.sort(key=lambda x: x[1], reverse=True)
top3 = scored_docs[:3]

for rank, (doc, score) in enumerate(top3, 1):
    print(f"\nRank {rank}  |  Score: {score}")
    print(f"  \"{doc}\"")

def rerank_score(doc):
    score     = 0
    doc_lower = doc.lower()
    if "midterm" in doc_lower:
        score += 2
    if "exam" in doc_lower:
        score += 2
    if any(char.isdigit() for char in doc):
        score += 3
    return score

print("reranked top 3")


reranked = [(doc, rerank_score(doc)) for doc, _ in top3]
reranked.sort(key=lambda x: x[1], reverse=True)

for rank, (doc, score) in enumerate(reranked, 1):
    print(f"\nRank {rank}, rerank score: {score}")
    print(f"  \"{doc}\"")

print("final answer:")
final_answer = reranked[0][0]
print(f"\n  \"{final_answer}\"")