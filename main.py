from tkinter import *
# from tkinter import messagebox
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"
current_word = {}
to_learn = {}

# ---------------------------- Flash card content ------------------------------- #
try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/spanish_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_word, flip_timer
    window.after_cancel(flip_timer)
    current_word = random.choice(to_learn)
    canvas.itemconfig(card_title, text="Spanish", fill="black")
    canvas.itemconfig(card_word, text=current_word["spanish"], fill="black")
    canvas.itemconfig(canvas_img, image=front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    global current_word
    canvas.itemconfig(canvas_img, image=back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_word["english"], fill="white")

def is_known():
    to_learn.remove(current_word)
    data_is_known = pandas.DataFrame(to_learn)
    data_is_known.to_csv("data/words_to_learn.csv", index=False)

    next_card()


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Learn Spanish!")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
wallpaper = PhotoImage(file="")
front_img = PhotoImage(file="./images/card_front.png")
back_img = PhotoImage(file="./images/card_back.png")
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_img = canvas.create_image(400, 270, image=front_img)
canvas.grid(column=0, row=0, columnspan=2)
window.config(background=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# ---------------------------- Buttons ------------------------------- #


check_img = PhotoImage(file="./images/right.png")
check_button = Button(image=check_img, highlightthickness=0, command=is_known)
check_button.config(padx=50, pady=50)
check_button.grid(column=1, row=1)
card_title = canvas.create_text(400, 150, fill="black", font=(FONT_NAME, 40, "italic"))
card_word = canvas.create_text(400, 263, fill="black", font=(FONT_NAME, 60, "bold"))
x_img = PhotoImage(file="./images/wrong.png")
x_button = Button(image=x_img, highlightthickness=0, command=next_card)
x_button.config(padx=50, pady=50)
x_button.grid(column=0, row=1)

next_card()
window.mainloop()
