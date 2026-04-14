import streamlit as st
import json
import os
from openai import OpenAI

st.title("Lab 9: Long-Term Memory Chatbot")

#part b
def memories_load():
    if os.path.exists('memories.json'):
        with open('memories.json', 'r') as f:
            return json.load(f)
    else:
        return {}

def memories_save(memories):
    with open('memories.json', 'w') as f:
        json.dump(memories, f)

st.sidebar.title("Saved Memories")
memories = memories_load()
if memories:
    for key, value in memories.items():
        st.sidebar.write(f"{key}: {value}")
else:
    st.sidebar.write("No memories saved yet.")

st.sidebar.button("Clear Memories", on_click=lambda: memories_save({}))

#part c: build the chatbot
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
 
def build_system_prompt():
    base_prompt = "You are a helpful assistant with long-term memory."
    memories = memories_load()
    if memories:
        memory_lines = "\n".join(f"- {key}: {value}" for key, value in memories.items())
        base_prompt += (
            "\n\nHere are things you remember about this user from past conversations:\n"
            + memory_lines
        )
    return base_prompt
 
def extract_memories(user_message, assistant_message):
    existing_memories = memories_load()
    existing_str = (
        json.dumps(existing_memories) if existing_memories else "None saved yet."
    )
 
    extraction_prompt = f"""You are a memory extraction assistant. 
Your job is to identify new facts about the user worth remembering long-term, 
such as their name, location, preferences, interests, job, or any other personal details.
Existing memories already saved (do NOT duplicate these): {existing_str}
 
User message: "{user_message}"
Assistant response: "{assistant_message}"
 
Return ONLY a JSON object of new facts to remember (key-value pairs), 
with no extra text, explanation, or markdown. 
If there are no new facts, return an empty object: {{}}
 
Example output: {{"name": "Alice", "favorite_color": "blue"}}"""
 
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[{"role": "user", "content": extraction_prompt}],
            temperature=0,
        )
        raw = response.choices[0].message.content.strip()
        new_facts = json.loads(raw)
 
        if new_facts:
            updated = memories_load()
            updated.update(new_facts)
            memories_save(updated)
 
    except Exception as e:
        pass

if user_input := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    system_prompt = build_system_prompt()
    api_messages = [{"role": "system", "content": system_prompt}] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]
 
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=api_messages,
    )
    assistant_reply = response.choices[0].message.content
 
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
    extract_memories(user_input, assistant_reply)
    st.rerun()


