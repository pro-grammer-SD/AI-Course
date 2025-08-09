import os
import requests
from dotenv import load_dotenv

load_dotenv()

def main():
    API_URL = "https://router.huggingface.co/hf-inference/models/distilbert/distilbert-base-uncased-finetuned-sst-2-english"
    headers = {
        "Authorization": f"Bearer {os.environ['HF_TOKEN']}",
    }

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    while True:
        text = input("Enter text (or 'exit' to quit): ")
        if text.lower() == "exit":
            break
        output = query({"inputs": text})
        sentiment = output[0][0]['label']
        print("Sentiment:", sentiment)

if __name__ == "__main__":
    main()
    