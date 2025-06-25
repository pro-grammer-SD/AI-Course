import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from rich.console import Console
from rich.panel import Panel

load_dotenv()

console = Console()
username = os.getlogin()
i = ""

def generate():
    client = genai.Client(
        api_key=os.environ.get("API_KEY"),
    )

    model = "gemini-2.5-flash-preview-04-17"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""{i} and don't give any slangs or harmful content in your response and don't mention I told you to not give any slangs or harmful content in your response."""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        console.print(f"[dark_orange]gemini@ai:[/dark_orange] {chunk.text}")

if __name__ == "__main__":
    console.print(Panel("[blue] 1. Please don't use bad language, \n 2. Be respectful \n 3. Ask meaningful questions \n 4. Feel comfortable. \n 5. Say `exit`, `quit`, `bye` or `goodbye` to end the chat!", 
                            title="[green]Usage", subtitle="[aquamarine1]Have a nice conversation."))
    
    while True:
        i = console.input(f"[green]you@{username}[/green][blue]_>[/blue] ")
        if i.lower() in ["exit", "quit", "bye", "goodbye"]:
            break
        generate(i)
        