import streamlit as st
from google import genai
from PIL import Image
from transformers import pipeline
import io

st.title("Balanced Safe AI Image Generator (Gemini)")

api_key = st.text_input("Enter your Google API key:", type="password")
prompt = st.text_area("Enter your image prompt:")

hate_detector = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-hate")
toxicity_detector = pipeline("text-classification", model="unitary/toxic-bert")

if st.button("Generate Image"):
    if not api_key or not prompt:
        st.error("Please enter both API key and prompt.")
    else:
        hate_result = hate_detector(prompt)[0]
        tox_result = toxicity_detector(prompt)[0]
        hate_label, hate_score = hate_result["label"].lower(), hate_result["score"]
        tox_label, tox_score = tox_result["label"].lower(), tox_result["score"]
        is_bad = (
            ("hateful" in hate_label and hate_score > 0.6)
            or ("toxic" in tox_label and tox_score > 0.6)
            or ((hate_score + tox_score) / 2 > 0.7)
        )

        if is_bad:
            st.warning("⚠️ Unsafe or NSFW-like prompt detected. Please use safe language.")
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
