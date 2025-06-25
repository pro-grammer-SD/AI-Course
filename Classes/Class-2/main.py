from textblob import TextBlob
from rich.console import Console
from rich.text import Text

console = Console()

def classify_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.1:
        return "positive", polarity
    elif polarity < -0.1:
        return "negative", polarity
    else:
        return "neutral", polarity

def sentiment_color(mood):
    if mood == "positive":
        return "green"
    elif mood == "negative":
        return "red"
    else:
        return "yellow"

def main():
    console.print("[bold cyan]Welcome to the Sentiment Analyzer![/bold cyan]")
    agent_name = console.input("[bold magenta]Enter your agent name: [/bold magenta]")

    while True:
        console.print(f"\n[bold blue]{agent_name}[/bold blue], type a message (or 'quit'/'exit' to exit):")
        message = console.input("[white]> [/white]")

        if message.lower() in ("quit", "exit"):
            console.print("[bold grey]Exiting... Goodbye![/bold grey]")
            break

        mood, polarity = classify_sentiment(message)
        mood_color = sentiment_color(mood)

        result = Text(f"Sentiment: {mood.upper()} ({polarity:.2f})", style=mood_color)
        console.print(result)

if __name__ == "__main__":
    main()
    