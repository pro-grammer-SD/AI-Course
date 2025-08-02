import random
import html
from fetch import get_data

data = get_data()

def get_category():
    return html.unescape(data.get("category", "Unknown"))

def get_correct_answer():
    return html.unescape(data.get("correct_answer", "Unknown"))

def get_difficulty():
    return html.unescape(data.get("difficulty", "Unknown"))

def get_incorrect_answers():
    return [html.unescape(ans) for ans in data.get("incorrect_answers", [])]

def get_question():
    return html.unescape(data.get("question", "Unknown"))

def get_type():
    return html.unescape(data.get("type", "Unknown"))

def get_options():
    options = get_incorrect_answers().copy()
    options.append(get_correct_answer())
    random.shuffle(options)
    return options

print(get_options())
