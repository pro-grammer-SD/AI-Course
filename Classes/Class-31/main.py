import streamlit as st
import streamlit_shadcn_ui as shadcn
from google import genai
from google.genai import types

gak = st.text_input("Enter your Google API Key", placeholder="AI-xyz")
st.link_button("Don't have one? Get it here.", "https://aistudio.google.com/api-keys")

try:
    client = genai.Client(api_key=gak)
    st.badge("Thank you for entering your API key. You may proceed now.", icon=":material/check_circle:", color="green")
except ValueError:
    st.badge("If you want to proceed, you must enter an API key!", icon=":material/gpp_maybe:", color="red")

st.link_button("Proceed", "/chat.py")
