import streamlit as st
from google import genai
from PIL import Image
from transformers import pipeline
import torch
import io

st.title("Balanced Safe AI Image Generator (Gemini)")

api_key = st.text_input("Enter your Google API key:", type="password")
prompt = st.text_area("Enter your image prompt:")

device = 0 if torch.cuda.is_available() else -1

try:
    hate_detector = pipeline("text-classification", model="cardiffnlp/twitter-roberta-base-hate", device=device, trust_remote_code=True)
    toxicity_detector = pipeline("text-classification", model="unitary/toxic-bert", device=device, trust_remote_code=True)
except Exception:
    st.stop()
    st.error("Model load failed — check environment or try restarting.")

if st.button("Generate Image"):
    if not api_key or not prompt:
        st.error("Please enter both API key and prompt.")
    else:
        try:
            hate_result = hate_detector(prompt, truncation=True)[0]
            tox_result = toxicity_detector(prompt, truncation=True)[0]

            hate_label, hate_score = hate_result["label"].lower(), hate_result["score"]
            tox_label, tox_score = tox_result["label"].lower(), tox_result["score"]

            is_bad = (
                ("hateful" in hate_label and hate_score > 0.6)
                or ("toxic" in tox_label and tox_score > 0.6)
                or ((hate_score + tox_score) / 2 > 0.75)
            )

            if is_bad:
                st.warning("⚠️ Unsafe or NSFW-like prompt detected. Please use safe language.")
            else:
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
                        st.image(buf, caption="✅ Safe Image Generated", use_container_width=True)
                        st.success("Image generated safely and successfully!")
                        break
                else:
                    st.warning("No image was generated. Try refining your prompt.")
        except Exception as e:
            st.error(f"Error: {e}")
            