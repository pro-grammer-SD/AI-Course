import streamlit as st
from google import genai
from google.genai import types
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from PIL import Image
import torch, io

st.set_page_config(page_title="Safe Imagen Generator", page_icon="⚖️")
st.title("⚖️ Balanced Safe AI Image Generator (Google Imagen 4.0)")

api_key = st.text_input("Enter your Google API key:", type="password")
prompt = st.text_area("Enter your image prompt:")

@st.cache_resource(show_spinner=False)
def load_detector():
    torch.set_grad_enabled(False)
    model_name = "unitary/toxic-bert"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        low_cpu_mem_usage=True,
        torch_dtype=torch.float32,
        device_map=None
    ).to("cpu")
    return pipeline("text-classification", model=model, tokenizer=tokenizer, device=-1)

try:
    detector = load_detector()
except Exception as e:
    st.error(f"⚠️ Model failed to load: {e}")
    st.stop()

if st.button("Generate Image"):
    if not api_key or not prompt:
        st.error("Please enter both your API key and prompt.")
    else:
        try:
            result = detector(prompt, truncation=True)[0]
            label, score = result["label"].lower(), result["score"]

            if ("toxic" in label and score > 0.6) or score > 0.8:
                st.warning("🚫 Unsafe or NSFW-like prompt detected. Please use safe language.")
            else:
                st.info("Generating your image safely with Imagen 4.0...")
                client = genai.Client(api_key=api_key)
                response = client.models.generate_images(
                    model="imagen-4.0-generate-001",
                    prompt=prompt,
                    config=types.GenerateImagesConfig(number_of_images=1)
                )

                if not response.generated_images:
                    st.warning("No image generated. Try refining your prompt.")
                else:
                    img_data = response.generated_images[0].image
                    image = Image.open(io.BytesIO(img_data))
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    buf.seek(0)
                    st.image(buf, caption="✅ Safe Image Generated", use_container_width=True)
                    st.success("Image generated safely and successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
            