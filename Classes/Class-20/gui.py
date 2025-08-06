import customtkinter
from CTkMessagebox import CTkMessagebox
from fetch import fetch

app = customtkinter.CTk()
app.geometry("700x450")

msg = CTkMessagebox(
    title="Proceed?",
    message="This program will waste your time. This is a warning from the developers of this program. Shall you want to proceed, dear user? Don't blame us for any waste of time.",
    icon="warning",
    option_1="No",
    option_2="Yes (you are sure to risk everything)"
)
response = msg.get()

if response == "No":
    app.destroy()

label = customtkinter.CTkLabel(
    app,
    text="",
    justify="left",
    wraplength=650,
    fg_color="transparent"
)
label.pack(padx=20, pady=10)

def reenable_button():
    button.configure(state="normal")

def button_callback():
    label.configure(text=fetch())
    button.configure(state="disabled")
    app.after(3000, reenable_button)  

button = customtkinter.CTkButton(
    app,
    height=60,
    text="get a random fact that is useless and will waste your time\n(There is a 3 seconds timeout to not cook up your system)",
    command=button_callback
)
button.pack(padx=20, pady=40)

app.mainloop()
