# import tkinter as tk
# from tkinter import ttk
from tkinter import messagebox
from random import shuffle

import loader
from settings import *


def count_percent(n: int, total: int) -> float:
    return 0 if total == 0 else round(n / total * 100, 2)


def click_main_window(window: tk.Tk):
    window.destroy()
    main()


def back_button(window: tk.Tk):
    button_back = button_settings(window, 'Главное меню')
    button_back.configure(command=lambda i=1: click_main_window(window))
    button_back.pack(side='bottom', fill='x')


def click_create_quiz(window: tk.Tk):
    window.destroy()
    window = tk.Tk()
    window_settings(window, 500, 400, 'Создание квиз')

    back_button(window)
    window.mainloop()


def on_select_quiz(*args):
    quiz, quiz_id, label = args
    selected_quiz = [q for q in quiz if q['id'] == quiz_id.get()][0]
    label.configure(text=f"{selected_quiz['name']}\nВсего вопросов: {len(selected_quiz['questions'])}")
    label.config(fg=SUCCESS_FG_COLOR)


def on_select_user(*args):
    user, username, label = args
    selected_user = [u for u in user if u['name'] == username.get()][0]
    answered = selected_user["answered_questions"]
    total = selected_user["total_questions"]
    percent = count_percent(answered, total)
    text = f'Пройдено квиз: {selected_user["quizes"]}\n'
    text += f'Правильных ответов {answered} из {total} ({percent}%)'
    label.configure(text=text)
    if total == answered:
        label.config(fg=SUCCESS_FG_COLOR)
    else:
        label.config(fg=SELECTED_FG_COLOR)


def get_question_text(quiz, q: int):
    return quiz['questions'][q - 1]['Q']


def on_change_status(username: str, score: list, status_bar_text):
    status_bar_text.config(text=f'{username}: Правильных ответов {score[0]} из {score[1]}')


def on_change_question(number_label, text_label, current_question, quiz):
    n = current_question.get()
    number_label.configure(text=f"Вопрос {n} из {len(quiz['questions'])}")
    text_label.configure(text=get_question_text(quiz, n))


def result_window(*args):
    window, quiz, user, username, score = args
    window.destroy()
    window = tk.Tk()
    window_settings(window, 600, 300, 'Результат')

    user_label = label_settings(window, username, 0, 0)
    user_label.pack(pady=5, side='top', fill='x')

    quiz_label = label_settings(window, quiz['name'], 0, 0)
    quiz_label.config(wraplength=590)
    quiz_label.pack(pady=5, side='top', fill='x')

    percent = count_percent(score[0], score[1])
    answer_label = label_settings(window, f'Правильных ответов {score[0]} из {score[1]} ({percent}%)', 0, 0)
    if score[0] == score[1]:
        answer_label.config(fg='green')
    else:
        answer_label.config(fg='red')
    answer_label.pack(pady=5, side='top', fill='x')

    total = [score[0] + user['answered_questions'], score[1] + user['total_questions']]
    percent = count_percent(total[0], total[1])
    total_score_label = label_settings(window, f'Общий счет: {total[0]} из {total[1]} ({percent}%)', 0, 0)
    if total[0] == total[1]:
        total_score_label.config(fg='green')
    else:
        total_score_label.config(fg='red')
    total_score_label.pack(pady=5, side='top', fill='x')

    loader.save_user_data(USER_DATA, username, total)

    back_button(window)


def click_confirm_answer(window: tk.Tk, current_question, data, score: list):
    global answers, right_answers, var, choices
    quiz, user, username, answers_frame, status_bar, status_bar_label = data
    questions = len(quiz['questions'])
    answer_type = quiz['questions'][current_question.get() - 1]['type']

    # check entered/selected data
    flag = 0
    if answer_type == 1 and var.get() == '' or answer_type == 2 and len([1 for i in range(len(var)) if var[i].get()]) == 0:
        messagebox.showerror("No data", 'Не выбран ни один ответ!')
        flag = 1
    elif answer_type == 3 and var.get() == '':
        messagebox.showerror("No data", 'Введите ответ!')
        flag = 1
    if flag:
        return

    miss = 1
    if answer_type == 1 and var.get() == right_answers[0]:
        miss = 0
    elif answer_type == 2:
        selected_answers = [choices[i] for i in range(len(answers)) if var[i].get()]
        right_answers.sort()
        selected_answers.sort()
        if right_answers == selected_answers:
            miss = 0
        # print('selected_answers =', selected_answers)
        # print('right_answers    =', right_answers)
    elif answer_type == 3 and var.get() == right_answers[0]:
        miss = 0
    score[0] = score[0] if miss else score[0] + 1
    score[1] += 1
    # print('score =', score)
    on_change_status(username, score, status_bar_label)

    if current_question.get() == questions:
        window.after(2000, lambda *args: result_window(window, quiz, user, username, score), (window, quiz, user, username, score))
        return

    current_question.set(current_question.get() + 1)
    generate_answers(answers_frame, quiz, current_question.get())


def generate_answers(frame, quiz, current_question: int):
    global answers, right_answers, var, choices
    current_question = quiz['questions'][current_question - 1]
    choices = current_question['choices']
    answer_type = current_question['type']
    if answer_type == 3:  # entry
        right_answers = [current_question['A']]
    else:
        right_answers = [choices[int(a)] for a in current_question['A'].split(';')]
    shuffle(choices)

    if len(answers):
        for answer in answers:
            answer.destroy()
    answers = []
    if answer_type == 1:  # radiobutton
        var = tk.StringVar()
        for i in range(len(choices)):
            radiobutton = tk.Radiobutton(frame, text=choices[i], value=choices[i], variable=var, justify='left',
                                         bg=BG_COLOR, fg=FG_COLOR, font=("Courier New", 16, "bold"),
                                         activebackground=BG_COLOR)
            radiobutton.grid(row=i, column=0, sticky='w', padx=10)
            answers.append(radiobutton)
    elif answer_type == 2:  # checkbox
        var = [tk.IntVar(value=0) for _ in range(len(choices))]
        for i in range(len(choices)):
            checkbutton = tk.Checkbutton(frame, text=choices[i], variable=var[i], justify='left',
                                         bg=BG_COLOR, fg=FG_COLOR, font=("Courier New", 16, "bold"),
                                         activebackground=BG_COLOR)
            checkbutton.grid(row=i, column=0, sticky='w', padx=10)
            answers.append(checkbutton)
    elif answer_type == 3:  # entry
        var = tk.StringVar(value='')
        entry = tk.Entry(frame, textvariable=var, fg=FG_COLOR, font=("Courier New", 16, "bold"))
        entry.pack(side='left', fill='x', padx=100, pady=10)
        answers = [entry]
    else:
        messagebox.showerror('Wrong type', f'Тип вопроса номер {answer_type} не определен!')


def game(window: tk.Tk, quiz_id: str, username: str, quiz_data, user_data):
    global answers, right_answers
    if quiz_id == '' or username == '':
        messagebox.showerror('No data', 'Не выбран квиз или не выбран участник!')
        return

    quiz = [q for q in quiz_data if q['id'] == quiz_id][0]
    user = [u for u in user_data if u['name'] == username][0]

    score = [0, 0]
    status_bar_text = tk.StringVar()
    status_bar_text.set(f'{username}: Правильных ответов {score[0]} из {score[1]}')
    # status_bar_text.trace('w', lambda *args: on_change_status(username, score, status_bar_text))
    # status_bar_text.set(f'{username}: Отвечено вопросов {score[0]} из {score[1]}')

    window.destroy()
    window = tk.Tk()
    window_settings(window, 1000, 800, f"Quiz {quiz['id']} {quiz['name']}")

    q_number_label = label_settings(window, '', 0, 0)
    q_number_label.pack(pady=5)

    q_text_label = tk.Label(window, bg=ACTIVE_BG_COLOR, fg='yellow', font=("Courier New", 18, "bold"),
                            justify='left', height=6, borderwidth=1, relief='solid', wraplength=900)
    q_text_label.pack(padx=5, pady=5, side='top', fill='x')
    q_text_label.propagate(False)

    status_bar = tk.Frame(window, borderwidth=1, relief='solid', bg=BG_COLOR, height=50)
    status_bar.pack(side='bottom', fill='x', padx=5, pady=5)
    status_bar.propagate(False)

    status_bar_label = label_settings(status_bar, status_bar_text.get(), 0, 0)
    # status_bar_label.config(textvariable=status_bar_text)
    status_bar_label.pack(pady=8)

    window.update()
    frame_height = (window.winfo_height() - q_number_label.winfo_height() * 2 -
                    q_text_label.winfo_height() - status_bar.winfo_height() - 53)
    answers_frame = tk.Frame(window, height=frame_height, borderwidth=1, relief='solid', bg=BG_COLOR)
    answers_frame.pack(padx=5, side='top', fill='x')
    answers_frame.propagate(False)

    current_question = tk.IntVar()
    current_question.trace('w', lambda *args: on_change_question(q_number_label, q_text_label, current_question, quiz))
    current_question.set(1)

    answers = []
    generate_answers(answers_frame, quiz, current_question.get())

    data = (quiz, user, username, answers_frame, status_bar, status_bar_label)
    button_confirm = button_settings(window, 'Ответ')
    button_confirm.configure(command=lambda i=1: click_confirm_answer(window, current_question, data, score))
    button_confirm.pack(side='bottom', padx=5)

    # window.update()
    # print('q_number_label =', q_number_label.winfo_height())
    # print('q_text_label =', q_text_label.winfo_height())
    # print('frame_height =', frame_height)
    # print('button_confirm =', button_confirm.winfo_height())


def click_play_quiz(window: tk.Tk):
    window.destroy()
    window = tk.Tk()
    window_settings(window, 700, 360, 'Играть!')

    label_settings(window, "Номер квиз", 20, 20)
    label_settings(window, "Участник", 20, 60)
    quiz_label = small_label_settings(window, "", 380, 20)
    user_label = small_label_settings(window, "", 380, 60)

    quiz = loader.get_json_data(QUIZ_DATA)
    quiz_list = [q['id'] for q in quiz]
    quiz_var = tk.StringVar()
    quiz_var.trace('w', lambda *args: on_select_quiz(quiz, quiz_var, quiz_label))
    combo_quiz = combobox_settings(window, quiz_list, 180, 20)
    combo_quiz.config(textvariable=quiz_var, state='readonly')

    user = loader.get_json_data(USER_DATA)
    user_list = [u['name'] for u in user]
    user_var = tk.StringVar()
    user_var.trace('w', lambda *args: on_select_user(user, user_var, user_label))
    combo_user = combobox_settings(window, user_list, 180, 60, 180)
    combo_user.config(textvariable=user_var, state='readonly')

    button_play = button_settings(window, 'Играть!')
    button_play.configure(command=lambda i=1: game(window, quiz_var.get(), user_var.get(), quiz, user))
    button_play.pack(pady=120)

    back_button(window)
    window.mainloop()


def main():
    root = tk.Tk()
    window_settings(root, 500, 250)

    button_create = button_settings(root, 'Создать квиз')
    button_create.configure(command=lambda i=1: click_create_quiz(root))
    button_create.pack(pady=50)

    button_play = button_settings(root, 'Пройти квиз')
    button_play.configure(command=lambda i=1: click_play_quiz(root))
    button_play.pack()

    root.mainloop()

answers, right_answers, choices = [], [], []
if __name__ == '__main__':
    main()
