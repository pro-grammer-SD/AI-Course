import requests
import flet as ft

def main(page: ft.Page):
    def get_joke(e):
        joke = requests.get("https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&format=txt").text
        joke_label.value = joke
        page.update()

    joke_label = ft.Text("", size=20, text_align=ft.alignment.center)
    get_joke_button = ft.ElevatedButton(text="Get a joke! 🤣", on_click=get_joke)
    page.add(joke_label, get_joke_button)

ft.app(main)
