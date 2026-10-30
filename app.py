"""StudyBuddy: lecture notes -> flashcards."""
import json
import os

import streamlit as st
from openai import OpenAI

# Switched off Nemotron the night before the deadline; it was faster to prototype with this.
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = "gpt-4o-mini"

PROMPT = ("Turn these notes into 5 flashcards. Reply with JSON only: "
          '[{"q": "...", "a": "..."}]\n\n')


def flashcards(notes: str) -> list:
    resp = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": PROMPT + notes}])
    return json.loads(resp.choices[0].message.content)


st.title("StudyBuddy")
notes = st.text_area("Your notes")
if st.button("Make flashcards") and notes:
    for card in flashcards(notes):
        with st.expander(card["q"]):
            st.write(card["a"])
