import streamlit as st
from google import genai
from PIL import Image
import io
from pysentimiento import create_analyzer

st.title("Smart Safe AI Image Generator (Gemini)")

api_key = st.text_input("Enter your Google API key:", type="password")
prompt = st.text_area("Enter your image prompt:")

analyzer = create_analyzer(task="toxicity", lang="en")

if st.button("Generate Image"):
    if not api_key or not prompt:
        st.error("Please enter both API key and prompt.")
    else:
        analysis = analyzer.predict(prompt)
        if analysis.output == "toxic" or analysis.probas["toxic"] > 0.5:
            st.warning("⚠️ NSFW or toxic prompt detected. Please use safe language.")
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
                