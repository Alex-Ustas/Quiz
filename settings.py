import tkinter as tk
from tkinter import ttk

BG_COLOR = "#98F254"
ACTIVE_BG_COLOR = "#60BE0E"
FG_COLOR = "#3050A0"
SELECTED_FG_COLOR = "#A02A1A"
SUCCESS_FG_COLOR = "#40800A"

QUIZ_DATA = 'data/quiz.json'
USER_DATA = 'data/user.json'


def button_settings(window: tk.Tk, text: str, width=20):
    button = tk.Button(window, text=text, width=width,
                       bg=BG_COLOR, fg=FG_COLOR, font=("Courier New", 18, "bold"), activebackground=ACTIVE_BG_COLOR)
    return button


def combobox_settings(window: tk.Tk, val: list, x: int, y: int, width=100):
    combo = ttk.Combobox(window, values=val, background=ACTIVE_BG_COLOR, foreground=FG_COLOR,
                         font=("Courier New", 18, "bold"))
    combo.place(x=x, y=y, width=width)
    return combo


def label_settings(window, text: str, x: int, y: int):
    label = tk.Label(window, text=text, background=BG_COLOR, foreground=FG_COLOR,
                     font=("Courier New", 18, "bold"), justify='left')
    label.place(x=x, y=y)
    return label


def small_label_settings(window, text: str, x: int, y: int):
    label = tk.Label(window, text=text, background=BG_COLOR, foreground=SELECTED_FG_COLOR,
                     font=("Courier New", 9, "bold"), justify='left')
    label.place(x=x, y=y)
    return label


def transparent_label_settings(window, text: str):
    style = ttk.Style()
    style.configure('TTKLabel', background='transparent')
    label = ttk.Label(window, text=text, foreground=FG_COLOR, style='TTKLabel',
                     font=("Courier New", 18, "bold"), justify='left')
    return label


def window_settings(window: tk.Tk, width: int, height: int, title='Quiz'):
    window.title(title)  # title
    window.iconbitmap("img/q.ico")  # window title icon
    window.resizable(False, False)  # Disable resizing
    window.config(bg=BG_COLOR)  # background color

    x = (window.winfo_screenwidth() - width) // 2
    y = (window.winfo_screenheight() - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")  # set size of window and move it to center of the screen
