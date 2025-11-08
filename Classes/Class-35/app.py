import streamlit as st
from google import genai
from PIL import Image
import io

st.title("Safe NSFW Image Generator (Gemini)")

api_key = st.text_input("Enter your Google API key:", type="password")
prompt = st.text_area("Enter your image prompt:")

if st.button("Generate Image"):
    if not api_key or not prompt:
        st.error("Please enter both API key and prompt.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=[prompt],
            )
            for part in response.parts:
                if part.inline_data is not None:
                    image = part.as_image()
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    buf.seek(0)
                    st.image(buf, caption="Generated Image", use_container_width=True)
                    break
            else:
                st.warning("No image was generated. Try refining your prompt.")
        except Exception as e:
            st.error(f"Error: {e}")
            