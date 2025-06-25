import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

data = {
    'title': [
        # Adult
        'The Matrix','John Wick','Inception','Interstellar','The Dark Knight',
        'Pulp Fiction','Fight Club','Forrest Gump','The Social Network','Tenet',
        'Blade Runner 2049','The Prestige','The Imitation Game','Arrival','Whiplash',
        # Kids/Family
        'Inside Out 2','Despicable Me 4','Mufasa: The Lion King','Sonic the Hedgehog 3',
        'Paddington in Peru','A Sloth Story','The Day the Earth Blew Up: A Looney Tunes Movie',
        'A Minecraft Movie','Snow White','Orion and the Dark','The Wild Robot',
        'No Time to Spy: A Loud House Movie','The Casagrandes Movie',
        'How to Train Your Dragon','Elio','The Bad Guys 2','Zootopia 2','Smurfs'
    ],
    'description': [
        # adult descriptions...
        'A computer hacker learns about the true nature of reality...',
        # ... same as before
        'A linguist works with aliens to understand their language...',
        # kids/family descriptions
        'Riley navigates puberty with new emotions.', # Inside Out 2
        'Gru and family face a new villain with help from Minions.', # DM4
        'Prequel adventures of Mufasa’s cub.', # Mufasa
        'Sonic, Knuckles & Tails fight new adversary.', # SH3
        'Paddington travels to Peru on a family mystery.', # Paddington
        'A sloth family starts a food truck in the city.', # Sloth Story
        'Daffy & Porky unite to stop alien invasion.', # Looney Tunes
        'Live-action kids into Minecraft Overworld.', # Minecraft
        'Greta Gerwig version of the classic fairytale.', # Snow White
        'A boy overcomes fear through adventure with Dark.', # Orion
        'Stranded robot befriends animals on an island.', # Wild Robot
        'The Loud family accidentally go undercover on spy mission.', # Loud House
        'Ronnie Anne & family face demigod in Mexico trip.', # Casagrandes
        'Hiccup befriends Toothless in live-action Viking tale.', # How to Train...
        'Pixar kid becomes Earth’s ambassador in space.', # Elio
        'Reformed villains pull off another heist.', # Bad Guys 2
        'Judy & Nick solve a new case in animal city.', # Zootopia 2
        'Blue characters save Papa Smurf in live-action musical.', # Smurfs
    ]
}

# Ensure title and description lengths match
if len(data['title']) != len(data['description']):
    min_len = min(len(data['title']), len(data['description']))
    data['title'] = data['title'][:min_len]
    data['description'] = data['description'][:min_len]

df = pd.DataFrame(data)
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['description'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
indices = pd.Series(df.index, index=df['title']).drop_duplicates()

def recommend(title, user_interest=None, n=5):
    if title not in indices: return ["Movie not found."]
    idx = indices[title]
    sims = sorted(enumerate(cosine_sim[idx]), key=lambda x: x[1], reverse=True)[1:]
    if user_interest:
        iv = tfidf.transform([user_interest])
        scores = cosine_similarity(iv, tfidf_matrix).flatten()
        sims = [(i, s * scores[i]) for i, s in sims]
    return [df['title'][i] for i, _ in sorted(sims, key=lambda x: x[1], reverse=True)[:n]]

console.print(Panel.fit("🎥 [bold cyan]All‑Ages Recommender[/bold cyan]", style="magenta"))
movie = Prompt.ask("Which one you liked?", choices=list(df['title']))
mood = Prompt.ask("Mood/keywords? Skip with Enter.", default="")
recs = recommend(movie, user_interest=mood)
console.print("\n[bold underline green]You’ll enjoy:[/bold underline green]")
for i, m in enumerate(recs, 1):
    console.print(f"[bold yellow]{i}.[/bold yellow] {m}")
