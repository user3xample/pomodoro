#! /usr/bin/env python3
#==============================================================================#
# title             : pomodoro, main.py
# Git               : https://github.com/user3xample/pomodoro
# description       : Pomodoro Technique timer with some speech chucked in for good
#                     measure.
# author            : Paul Abel
# date              : 12/06/2023
# version           : 1.0
# usage             : ./pomodoro
# notes             : In development.
# python_version    : Python 3, tested on 3.11
# licence           : GNU General Public License v3.0
#		              https://github.com/user3xample/updater/blob/main/LICENSE
# dependencies      : tkinter, gtts , pygames, io.
#                     In a folder with tomato.png
#                     (need internet connection for gtts as its google translate)
#==============================================================================#

from tkinter import *
import math
from gtts import gTTS
import pygame
from io import BytesIO

# ---------------------------- CONSTANTS ------------------------------- #
WHITE = "#FFF4F4"
RED = "#F24C3D"
GREEN = "#22A699"  # its Teal not green
YELLOW = "#f29727"  # bg colour
FONT_NAME = "Courier"
WORK_MIN = 25  # norm 25
SHORT_BREAK_MIN = 5  # normally 5
LONG_BREAK_MIN = 30  # 15-30 min's
reps = 0  # keep at zero.
timer = None # Leave Alone.

# ---------------------------- TIMER RESET ------------------------------- # 

def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text=f"Work: {WORK_MIN} mins\nshortbreak: {SHORT_BREAK_MIN} mins\nLong: {LONG_BREAK_MIN}"
                         f" mins\n4 X work = long break", fg=WHITE, bg=YELLOW, font=(FONT_NAME, 30, "bold"))
    check_marks.config(text="")
    global reps
    reps = 0

# ---------------------------- SPEACH MECHANISM ------------------------------ #
def say(text):
    tts = gTTS(text=text, lang='en', tld='com' )
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# ---------------------------- TIMER MECHANISM ------------------------------- # 

def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        say(f"Lets take a breather for a bit you have been working for {WORK_MIN*4} minutes")
        count_down(long_break_sec)
        title_label.config(text=">>: Long Break ", fg=RED)
    elif reps % 2 == 0:
        say("Time for a short break")
        count_down(short_break_sec)
        title_label.config(text=">>: Short Break", fg=WHITE)
    else:
        count_down(work_sec)
        title_label.config(text=">>: Work Time  ", fg=WHITE)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("My Pomodoro Timer")
window.config(padx=100, pady=50, bg=YELLOW)


title_label = Label(text=f"Work: {WORK_MIN} mins\nshortbreak: {SHORT_BREAK_MIN} mins\nLong: {LONG_BREAK_MIN}"
                         f" mins\n4 X work = long break", fg=WHITE, bg=YELLOW, font=(FONT_NAME, 30, "bold"))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 115, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", highlightthickness=10, command=start_timer, font="bold")
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=10, command=reset_timer, font="bold")
reset_button.grid(column=2, row=2)

check_marks = Label(fg=RED, bg=YELLOW, font="bold")
check_marks.grid(column=1, row=3)


window.mainloop()
