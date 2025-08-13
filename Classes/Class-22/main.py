import os

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

import requests
from dotenv import load_dotenv
import customtkinter as ctk
from css_for_ctk.apply import apply_styles

load_dotenv()

@apply_styles(open("style.css", "r").read())
class SentimentApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.API_URL = "https://router.huggingface.co/hf-inference/models/distilbert/distilbert-base-uncased-finetuned-sst-2-english"
        self.headers = {"Authorization": f"Bearer {os.environ['HF_TOKEN']}"}

        self.input_entry = ctk.CTkEntry(self)
        self.analyze_button = ctk.CTkButton(self, command=self.analyze_sentiment)
        self.result_label = ctk.CTkLabel(self, text="")

    def query(self, payload):
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        return response.json()

    def analyze_sentiment(self):
        text = self.input_entry.get()
        if not text:
            self.result_label.configure(text="Please enter some text!")
            return
        output = self.query({"inputs": text})
        sentiment = output[0][0]['label']
        self.result_label.configure(text=f"Sentiment: {sentiment}")

if __name__ == "__main__":
    app = SentimentApp()
    app.mainloop()
    