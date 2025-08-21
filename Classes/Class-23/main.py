from transformers import pipeline
import PyPDF2

def summarize_pdf(pdf_path):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

    text = ""
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()

    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary

print(summarize_pdf("aura.pdf"))
