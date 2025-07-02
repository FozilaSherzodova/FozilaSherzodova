from tkinter import *
import requests


def get_quote():
    response = requests.get(url="https://official-joke-api.appspot.com/random_joke")
    response.raise_for_status()
    joke = response.json()
    question = joke["setup"]
    answer = joke["punchline"]
    canvas.itemconfig(quote_text, text=f"{question}\n---{answer}")


window = Tk()
window.title("Funny Questions...")
window.config(padx=50, pady=50)

speech_img = PhotoImage(file="joke api\speech bubble.png")

canvas = Canvas(window, width=400, height=304)
canvas.create_image(200, 152, image=speech_img)
quote_text = canvas.create_text(200, 100, text="Click the button for a joke!", width=200, font=("Arial", 10))
canvas.grid(row=0, column=0, columnspan=2)

btn = Button(text="click", highlightthickness=0, command=get_quote, width=10, height=5)
btn.grid(row=1, column=0, columnspan=2)


window.mainloop()
