import random
import re
from colorama import Fore, Style, init

init(autoreset=True)

cities = ["Paris", "Tokyo", "New York", "Barcelona", "Rome", "Dubai"]
packing_tips = [
    "Roll your clothes to save space.",
    "Pack versatile outfits you can mix and match.",
    "Don't forget a universal charger.",
    "Pack travel-size toiletries."
]
jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "I asked the librarian if the library had books on paranoia. She whispered, 'They're right behind you.'",
    "Why did the scarecrow win an award? Because he was outstanding in his field!"
]

state = None
last_city = None

print(f"{Fore.CYAN}TravelBot: Hey! I'm your travel buddy ✈️")
print("I can:")
print("- Suggest travel spots (say 'recommendation')")
print("- Offer packing tips (say 'packing')")
print("- Tell a joke (say 'joke')")
print("Type 'exit' or 'bye' to end.\n")

while True:
    user = input(Fore.YELLOW + "You: " + Style.RESET_ALL).strip().lower()

    if user in ["exit", "bye"]:
        print(f"{Fore.CYAN}TravelBot: Safe travels! 👋")
        break

    if state == "confirm_city":
        if re.search(r"\byes\b", user):
            print(f"{Fore.CYAN}TravelBot: Awesome! Enjoy {last_city}!")
        elif re.search(r"\bno\b", user):
            print(f"{Fore.CYAN}TravelBot: No worries. Maybe try {random.choice(cities)}?")
        else:
            print(f"{Fore.CYAN}TravelBot: Just say 'yes' or 'no'.")
        state = None
        continue

    if re.search(r"\b(recommend|city|travel|trip)\b", user):
        last_city = random.choice(cities)
        print(f"{Fore.CYAN}TravelBot: How about {last_city}?")
        print(f"{Fore.CYAN}TravelBot: Do you like it? (yes/no)")
        state = "confirm_city"
    elif re.search(r"\bpack|packing\b", user):
        print(f"{Fore.CYAN}TravelBot: {random.choice(packing_tips)}")
    elif re.search(r"\bjoke\b", user):
        print(f"{Fore.CYAN}TravelBot: {random.choice(jokes)}")
    else:
        print(f"{Fore.CYAN}TravelBot: I didn't get that. Try 'recommendation', 'packing', or 'joke'.")
