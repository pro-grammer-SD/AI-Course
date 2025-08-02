import data
import customtkinter

lives = 3

def valid_data():
    while True:
        global data_obj
        data_obj = data.get_data()

        category = data_obj.get("category", "Unknown")
        difficulty = data_obj.get("difficulty", "Unknown")
        qtype = data_obj.get("type", "Unknown")
        question = data_obj.get("question", "Unknown")
        correct = data_obj.get("correct_answer", "Unknown")
        incorrect = data_obj.get("incorrect_answers", [])

        if "Unknown" in (category, difficulty, qtype, question, correct):
            continue
        if not incorrect or "Unknown" in incorrect:
            continue

        return {
            "category": category,
            "difficulty": difficulty,
            "type": qtype,
            "question": question,
            "correct": correct,
            "incorrect": incorrect,
        }

def get_options(correct, incorrect):
    import random, html
    options = [html.unescape(opt) for opt in incorrect]
    options.append(html.unescape(correct))
    random.shuffle(options)
    return options

def load_question():
    global current_options, question_data
    selected_option.set("")

    question_data = valid_data()

    catgeory.configure(text="Category: " + question_data["category"].replace("amp;", ""))
    difficulty.configure(text="Difficulty: " + question_data["difficulty"])
    qtype.configure(text="Type: " + question_data["type"])
    question.configure(text="Q: " + question_data["question"])

    for rb in current_options:
        rb.destroy()
    current_options = []

    options = get_options(question_data["correct"], question_data["incorrect"])

    for option in options:
        rb = customtkinter.CTkRadioButton(frame, text=option, variable=selected_option, value=option)
        rb.pack(anchor="w", pady=2)
        current_options.append(rb)

    result_label.configure(text="")

def update_lives_bar():
    progress.set(lives / 3)

def button_callback():
    global lives
    selected = selected_option.get()
    if selected == question_data["correct"]:
        result_label.configure(text="✅ Correct!", text_color="green")
    else:
        lives -= 1
        update_lives_bar()
        result_label.configure(text=f"❌ Wrong! Correct: {question_data['correct']}", text_color="red")
        if lives == 0:
            result_label.configure(text="💀 Game Over!", text_color="red")
            button.configure(state="disabled")
            return
    app.after(1500, load_question)

app = customtkinter.CTk()
app.geometry("700x450")
app.title("Quiz UI")

frame = customtkinter.CTkFrame(app)
frame.pack(padx=20, pady=20, fill="both", expand=True)

selected_option = customtkinter.StringVar(value="")
current_options = []

progress = customtkinter.CTkProgressBar(frame, width=200)
progress.pack(pady=10)
progress.set(1.0)

catgeory = customtkinter.CTkLabel(frame, text="")
catgeory.pack(anchor="w", pady=(10, 5))

difficulty = customtkinter.CTkLabel(frame, text="")
difficulty.pack(anchor="w", pady=5)

qtype = customtkinter.CTkLabel(frame, text="")
qtype.pack(anchor="w", pady=5)

question = customtkinter.CTkLabel(frame, text="", wraplength=650, justify="left")
question.pack(anchor="w", pady=(10, 20))

button = customtkinter.CTkButton(frame, text="Submit", command=button_callback)
button.pack(pady=(15, 5))

result_label = customtkinter.CTkLabel(frame, text="", font=("Arial", 14))
result_label.pack(pady=10)

load_question()

app.mainloop()
