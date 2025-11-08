import streamlit as st
from google import genai
from PIL import Image
from transformers import pipeline
import io

st.title("Safe AI Image Generator (Gemini)")

api_key = st.text_input("Enter your Google API key:", type="password")
prompt = st.text_area("Enter your image prompt:")

moderator = pipeline("text-classification", model="facebook/roberta-hate-speech-dynabench-r4-target")

if st.button("Generate Image"):
    if not api_key or not prompt:
        st.error("Please enter both API key and prompt.")
    else:
        analysis = moderator(prompt)[0]
        label = analysis["label"].lower()
        score = analysis["score"]
        if ("hate" in label or "offensive" in label or score > 0.6):
            st.warning("⚠️ Unsafe or NSFW-like prompt detected. Please use appropriate language.")
        else:
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.5-flash-image",
                    contents=[prompt],
                )
                image_displayed = False
                for part in response.parts:
                    if part.inline_data is not None:
                        image = part.as_image()
                        buf = io.BytesIO()
                        image.save(buf, format="PNG")
                        buf.seek(0)
                        st.image(buf, caption="✅ Safe Image Generated", use_container_width=True)
                        st.success("Image generated safely and successfully!")
                        image_displayed = True
                        break
                if not image_displayed:
                    st.warning("No image was generated. Try refining your prompt.")
            except Exception as e:
                st.error(f"Error: {e}")
                