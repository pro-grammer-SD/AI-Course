import streamlit as st
from google import genai
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch, io

st.title("⚖️ Balanced Safe AI Image Generator (Gemini)")

api_key = st.text_input("Enter your Google API key:", type="password")
prompt = st.text_area("Enter your image prompt:")

@st.cache_resource(show_spinner=False)
def load_detectors():
    torch.set_grad_enabled(False)
    model_name = "unitary/toxic-bert"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        low_cpu_mem_usage=True,
        torch_dtype=torch.float32,
        device_map=None
    ).to("cpu")
    detector = pipeline("text-classification", model=model, tokenizer=tokenizer, device=-1)
    return detector

try:
    detector = load_detectors()
except Exception as e:
    st.error(f"Model failed to load: {e}")
    st.stop()

if st.button("Generate Image"):
    if not api_key or not prompt:
        st.error("Please enter both API key and prompt.")
    else:
        try:
            result = detector(prompt, truncation=True)[0]
            label, score = result["label"].lower(), result["score"]

            if ("toxic" in label and score > 0.6) or score > 0.8:
                st.warning("⚠️ Unsafe or NSFW-like prompt detected. Please use safe language.")
            else:
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
            