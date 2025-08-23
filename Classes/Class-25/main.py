import os
import subprocess
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from rich.prompt import Prompt
from rich.console import Console

load_dotenv()
console = Console()

client = InferenceClient(
    provider="hf-inference",
    api_key=os.environ["USE_MAAMS_FREE_API_KEY_TO_LIKE_JUST_GET_MAAM_HIT_API_LIMITS_IN_JUST_ONE_SECOND"],
)

while True:
    subprocess.run("cls", shell=True, check=True)
    prompt_text = Prompt.ask("[bold cyan]Enter your image prompt (or 'quit' to exit)")
    if prompt_text.lower() in {"quit", "exit"}:
        break

    try:
        image = client.text_to_image(
            prompt_text,
            model="black-forest-labs/FLUX.1-dev",
        )
        output_path = "output.png"
        image.save(output_path)
        console.print(f"[green]Image saved to {output_path}[/green]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        