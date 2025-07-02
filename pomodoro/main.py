from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25*60
SHORT_BREAK_MIN = 5*60
LONG_BREAK_MIN = 20*60
reps = 0
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def restarting():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    time_label.config(text="Timer")
    mark_label["text"] = ""
    global reps
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
def starting():
    global reps
    reps += 1

    if reps % 8 == 0:
        time_label["text"] = "Long break time"
        count_down(LONG_BREAK_MIN)
    elif reps % 2 == 0:
        time_label["text"] = "Short break time"
        count_down(SHORT_BREAK_MIN)
    else:
        time_label["text"] = "Work time"
        count_down(WORK_MIN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(n):
    count_min = math.floor(n/60)
    count_sec = n % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}"
    if count_min < 10:
        count_min = f"0{count_min}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if n > 0:
        global timer
        timer = window.after(1000, count_down, n-1)
    else:
        starting()
        if reps % 2 == 1:
            mark_label["text"] += check_mark


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="pomodoro\\tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

time_label = Label(text="Time", font=(FONT_NAME, 35, "bold"), fg=GREEN, bg=YELLOW)
time_label.grid(column=1, row=0)

check_mark = "✓"
mark_label = Label(text="", font=(FONT_NAME, 20, "bold"), fg=GREEN, bg=YELLOW)
mark_label.grid(column=1, row=3)

start_btn = Button(text="Start", command=starting)
start_btn.grid(column=0, row=2)

reset_btn = Button(text="Reset", command=restarting)
reset_btn.grid(column=2, row=2)

window.mainloop()
