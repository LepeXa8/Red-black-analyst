from tkinter import *

check = []
alives = [str(i) for i in range(1, 11)]
killed_at_night = []
numbers = [str(i) for i in range(1, 11)]
sheriff1 = {"красные": [],
            "черные": []}
sheriff2 = {"красные": [],
            "черные": []}
sheriff3 = {"красные": [],
            "черные": []}
votes = {"1": [],
         "2": [],
         "3": [],
         "4": [],
         "5": [],
         "6": [],
         "7": [],
         "8": [],
         "9": [],
         "10": []}
red = []
count_of_steps = 0
count_of_cycles = 1  # счетчик фаз и счетчик циклов (в одном цикле 3 фазы: ночь, день, голосование)
text = ""
window = Tk()
window.title("КРАСНО-ЧЕРНЫЙ АНАЛИТИК")

programm_flag = True


def three_sheriffs(s1, s2, s3):
    global text1
    text1 = f'В игре вскрылось 3 шерифа: один настоящий, два других – лжецы. Будет логично избавиться срзау от всех, а именно {s1}, {s2}, {s3}, ведь так мы убьем сразу двух черных.'


def balace(s1, s2):
    global text1
    if len(s1["черные"]) and len(s2["черные"]) and (len(set(s1["черные"]) & set(alives)) > 0) and (
            len(set(s2["черные"]) & set(alives)) > 0) and sheriff1["номер"] in alives and sheriff2["номер"] in alives:
        bl1 = list(set(s1["черные"]) & set(alives))[0]
        bl2 = list(set(s2["черные"]) & set(alives))[0]
        text1 = (
            f'В игре есть два шерифа, оба живы и у обоих есть черные проверки. Можно применить тактику "БАЛАНС", которая заключается  \n в удалении сначала черной проверки одного шерифа – {bl1}, а затем другого – {bl2}, что гарантированно уберет одного черного. \n'
            f' Более того, этот вид баланса является наиболее предподчтительным, так как мы не убили настоящего шерифа, который будет давать нам информацию')
    elif len(s1["черные"]) and (len(set(s1["черные"]) & set(alives)) > 0) and sheriff1["номер"] in alives and sheriff2[
        "номер"] in alives:
        bl1 = list(set(s1["черные"]) & set(alives))[0]
        text1 = (
            f'В игре есть два шерифа, оба живы и у одного из них есть черная проверка. Можно применить тактику "БАЛАНС", которая заключается  \n в удалении сначала черной проверки шерифа – {bl1}, а затем и самого шерифа – {s1["номер"]}, что гарантированно уберет одного черного. \n '
            f'Важно! Этот вид "баланса", как и остальные, применятся только при двух шерифах. \n Если шериф один, '
            f'и у него есть черная проверка, следует доверять этому шерифу')
    elif len(s2["черные"]) and (len(set(s2["черные"]) & set(alives)) > 0) and sheriff1["номер"] in alives and sheriff2[
        "номер"] in alives:
        bl1 = list(set(s2["черные"]) & set(alives))[0]
        text1 = (
            f'В игре есть два шерифа, оба живы и у одного из них есть черная проверка. Можно применить тактику "БАЛАНС", которая заключается  \n в удалении сначала черной проверки шерифа – {bl1}, а затем и самого шерифа – {s1["номер"]}, что гарантированно уберет одного черного. \n '
            f'Важно! Этот вид "баланса", как и остальные, применятся только при двух шерифах. \n Если шериф один, и у него есть черная проверка, следует доверять этому шерифу')


def one_sheriff_with_black_check(s1):
    global text1
    alive_reds = list(set(s1["красные"]) & set(alives))
    alive_black = ("").join(list(set(s1["черные"]) & set(alives)))
    text1 = f'В игре вскрылся только один шериф, значит, он настоящий, так как при вскрытии лжешерифа, настоящий шериф был бы тоже обязан вскрыться \n (двухшерифская игра). У него есть черные проверки: {alive_black}, за них нужно голосовать'


def voting(c_o_s):
    global count_of_steps
    global count_of_cycles
    global max_votes
    votingframe = LabelFrame(window, text=f"  ГОЛОСОВАНИЕ {count_of_cycles}", bd=3, font=("Arial Black", 12))
    votingframe.grid(row=count_of_cycles, column=2, sticky=W)
    global row_now2
    row_now2 = 0
    max_candidate = ""
    max_votes = -1
    def add_candidate():
        global row_now2, max_candidate, vote_entry, voters_entry, max_votes
        if row_now2 > 0:
            votes[vote_entry.get()].append((voters_entry.get()).split())
            if max(max_votes, len((voters_entry.get()).split())) == len((voters_entry.get()).split()):
                max_votes = len((voters_entry.get()).split())
                max_candidate = vote_entry.get()

        vote_text = Label(votingframe, text="За игрока номер", font=("Arial", 13))
        vote_text.grid(row=row_now2, column=0)
        vote_entry = Entry(votingframe, width=3, font=("Arial", 13))
        vote_entry.grid(row=row_now2, column=1, sticky=W)
        vote_text2 = Label(votingframe, text="голосуют игроки (через пробел):", font=("Arial", 13))
        vote_text2.grid(row=row_now2, column=2)
        voters_entry = Entry(votingframe, width=10, font=("Arial", 13))
        voters_entry.grid(row=row_now2, column=4, sticky=W)

        row_now2 += 1

    def vcontinue_():
        global count_of_cycles, vote_entry, voters_entry, row_now2, count_of_steps, max_candidate, max_votes

        if row_now2 > 0:
            votes[vote_entry.get()].append((voters_entry.get()).split())
            if max(max_votes, len((voters_entry.get()).split())) == len((voters_entry.get()).split()):
                max_votes = len((voters_entry.get()).split())
                max_candidate = vote_entry.get()
        alives.remove(max_candidate)
        count_of_steps += 1
        count_of_cycles += 1
        night(count_of_steps)

    add_candidate_btn = Button(votingframe, text="Добавить кандидатуру", font=("Arial", 13), command=add_candidate)
    add_candidate_btn.grid(row=100, column=0, sticky=W, columnspan=3)
    space = Label(votingframe, text=("    "), font=("Arial", 13))
    space.grid(row=100, column=5)
    continue_button = Button(votingframe, text="Далее", font=("Arial", 13), command=vcontinue_)
    continue_button.grid(row=101, column=0, sticky=W)

def day(c_o_s):
    global programm_flag
    global count_of_steps
    global clmn
    global text1
    clmn = 0
    def end():
        if sheriff_entry != None:  # обработка инфы по шерифству
            if sheriff1.get("номер") is None or sheriff1.get("номер") == sheriff_entry.get():
                sheriff1['номер'] = sheriff_entry.get()
                if color_of_sheriff_check.get() == 1:
                    sheriff1["красные"].append(sheriff_check.get())
                elif color_of_sheriff_check.get() == 2:
                    sheriff1["черные"].append(sheriff_check.get())
            elif sheriff2.get("номер") is None or sheriff2.get("номер") == sheriff_entry.get():
                sheriff2['номер'] = sheriff_entry.get()
                if color_of_sheriff_check.get() == 1:
                    sheriff2["красные"].append(sheriff_check.get())
                elif color_of_sheriff_check.get() == 2:
                    sheriff2["черные"].append(sheriff_check.get())
            elif sheriff3.get("номер") is None or sheriff3.get("номер") == sheriff_entry.get():
                sheriff3['номер'] = sheriff_entry.get()
                if color_of_sheriff_check.get() == 1:
                    sheriff3["красные"].append(sheriff_check.get())
                elif color_of_sheriff_check.get() == 2:
                    sheriff3["черные"].append(sheriff_check.get())

        if sheriff1.get("номер") in numbers and sheriff2.get("номер") in numbers and sheriff3.get("номер") in numbers:
            three_sheriffs(sheriff1["номер"], sheriff2["номер"], sheriff3["номер"])
        elif sheriff1.get("номер") in numbers and sheriff2.get("номер") in numbers:
            balace(sheriff1, sheriff2)
        elif sheriff1.get("номер") in numbers and len(sheriff1.get("номер")) > 0:
            one_sheriff_with_black_check(sheriff1)
        answerframe = LabelFrame(window, text="  РЕШЕНИЕ", bd=3, font=("Arial Black", 12))
        answerframe.grid(row=count_of_cycles + 1, column=0, sticky=W, columnspan=3)
        answer1 = Label(answerframe, text=text1, font=("Arial", 13))
        answer1.grid(row=0, column=0, sticky=W)

    # создаем рамку для дня
    dayframe = LabelFrame(window, text=f"  ДЕНЬ {count_of_cycles}", bd=3, font=("Arial Black", 12), width=1000)
    dayframe.grid(row=count_of_cycles, column=1, sticky=W)
    global row_now
    global sheriff_entry
    global sheriff_check
    global color_of_sheriff_check
    sheriff_entry = None
    row_now = 0

    def sheriff_openning():  # команда для вскрытия шерифа
        global row_now
        global sheriff_entry
        global sheriff_check
        global color_of_sheriff_check
        if sheriff_entry != None:  # обработка инфы по шерифству
            if sheriff1.get("номер") is None or sheriff1.get("номер") == sheriff_entry.get():
                sheriff1['номер'] = sheriff_entry.get()
                if color_of_sheriff_check.get() == 1:
                    sheriff1["красные"].append(sheriff_check.get())
                elif color_of_sheriff_check.get() == 2:
                    sheriff1["черные"].append(sheriff_check.get())
            elif sheriff2.get("номер") is None or sheriff2.get("номер") == sheriff_entry.get():
                sheriff2['номер'] = sheriff_entry.get()
                if color_of_sheriff_check.get() == 1:
                    sheriff2["красные"].append(sheriff_check.get())
                elif color_of_sheriff_check.get() == 2:
                    sheriff2["черные"].append(sheriff_check.get())
            elif sheriff3.get("номер") is None or sheriff3.get("номер") == sheriff_entry.get():
                sheriff3['номер'] = sheriff_entry.get()
                if color_of_sheriff_check.get() == 1:
                    sheriff3["красные"].append(sheriff_check.get())
                elif color_of_sheriff_check.get() == 2:
                    sheriff3["черные"].append(sheriff_check.get())

        # просто текст
        sheriff_openning_text = Label(dayframe, text="    Игрок номер", font=("Arial", 13))
        sheriff_openning_text.grid(row=row_now, column=0, sticky=W)
        # поле для ввода САМОГО ШЕРИФА
        sheriff_entry = Entry(dayframe, width=3, font=("Arial", 13))
        sheriff_entry.grid(row=row_now, column=2, sticky=W)
        # просто текст
        sheriff_openning_text_2 = Label(dayframe, text="вскрывается шерифом:  ", font=("Arial", 13))
        sheriff_openning_text_2.grid(row=row_now, column=3, sticky=W, columnspan=6)
        # поле для ввода ПРОВЕРКИ ШЕРИФА
        sheriff_check = Entry(dayframe, width=3, font=("Arial", 12))
        sheriff_check.grid(row=row_now, column=9, sticky=W)
        # просто текст
        sheriff_openning_text_3 = Label(dayframe, text=" проверенный ", font=("Arial", 13))
        sheriff_openning_text_3.grid(row=row_now, column=10, sticky=W)

        color_of_sheriff_check = IntVar()  # эта переменная принимает значение 1, если проверка шерифа красная и 2, если черная
        red_sheriff_check = Radiobutton(dayframe, text='красный', font=("Arial", 12), variable=color_of_sheriff_check,
                                        value=1)
        black_sheriff_check = Radiobutton(dayframe, text='черный', font=("Arial", 12), variable=color_of_sheriff_check,
                                          value=2)
        red_sheriff_check.grid(row=row_now, column=11, sticky=W)
        black_sheriff_check.grid(row=row_now, column=12, sticky=W)

        row_now += 1

    def continue_():
        global days_over
        global row_now
        global sheriff_entry
        global sheriff_check
        global color_of_sheriff_check
        global count_of_steps
        if sheriff_entry != None:  # обработка инфы по шерифству
            if sheriff1.get("номер") is None or sheriff1.get("номер") == sheriff_entry.get():
                sheriff1['номер'] = sheriff_entry.get()
                if color_of_sheriff_check.get() == 1:
                    sheriff1["красные"].append(sheriff_check.get())
                elif color_of_sheriff_check.get() == 2:
                    sheriff1["черные"].append(sheriff_check.get())
            elif sheriff2.get("номер") is None or sheriff2.get("номер") == sheriff_entry.get():
                sheriff2['номер'] = sheriff_entry.get()
                if color_of_sheriff_check.get() == 1:
                    sheriff2["красные"].append(sheriff_check.get())
                elif color_of_sheriff_check.get() == 2:
                    sheriff2["черные"].append(sheriff_check.get())
            elif sheriff3.get("номер") is None or sheriff3.get("номер") == sheriff_entry.get():
                sheriff3['номер'] = sheriff_entry.get()
                if color_of_sheriff_check.get() == 1:
                    sheriff3["красные"].append(sheriff_check.get())
                elif color_of_sheriff_check.get() == 2:
                    sheriff3["черные"].append(sheriff_check.get())
        row_now += 1
        days_over = True
        space = Label(dayframe, text=("    "), font=("Arial", 13))
        count_of_steps += 1
        voting(count_of_steps)

    add_check_btn = Button(dayframe, text="Добавить проверку", font=("Arial", 13), command=sheriff_openning)
    add_check_btn.grid(row=100, column=0, sticky=W, columnspan=3)

    continue_button = Button(dayframe, text="Далее", font=("Arial", 13), command=continue_)
    continue_button.grid(row=101, column=0, sticky=W)
    end_button = Button(dayframe, text="ПЕРЕЙТИ К РЕШЕНИЮ", font=("Arial", 13), command=end)
    end_button.grid(row=101, column=3, sticky=W, columnspan=2)

    space = Label(dayframe, text=("    "), font=("Arial", 13))
    space.grid(row=101, column=1, columnspan=2)


def night(c_o_s):  # ночь
    def killing_sheriff():  # комманда для ввода проверки от убитого ночью шерифа

        if is_he_sheriff.get():
            check_of_dead_sheriff.grid(row=1, column=2, sticky=W)
            check_of_dead_sheriff_text.grid(row=1, column=3, sticky=W)
            red_dead_sheriff_check.grid(row=1, column=4, sticky=W)
            black_dead_sheriff_check.grid(row=1, column=5, sticky=W)

        else:
            check_of_dead_sheriff.grid_remove()
            check_of_dead_sheriff_text.grid_remove()
            red_dead_sheriff_check.grid_remove()
            black_dead_sheriff_check.grid_remove()

    def continue_():  # команда, запускающаяся при нажатии кнопки ДАЛЕЕ
        global nights_over
        global count_of_steps
        if nightkilled.get() in alives:
            alives.remove(nightkilled.get())  # удаляем игрока из списка живых
            killed_at_night.append(nightkilled.get())  # добавляем убитого в список убитых ночью
            # ПОЗЖЕ ЗДЕСЬ НУЖНО ДОБАВИТЬ ОБРАБОТКУ ИНФОРМАЦИИ, ПОЛУЧЕННОЙ ОТ УБИТОГО ШЕРИФА!!!!
        count_of_steps += 1
        day(count_of_steps)

    # создаем рамку для ночи
    nightframe = LabelFrame(window, text=f"  НОЧЬ {count_of_cycles}", bd=3, font=("Arial Black", 12))
    nightframe.grid(row=count_of_cycles, column=0, sticky=W)
    # создаем текст "Убит игрок"
    nightlabel = Label(nightframe, text=("Убит игрок номер"), font=("Arial", 13))
    nightlabel.grid(row=0, column=0, sticky=W)
    # создаем поле для ввода убитого игрока этой ночью
    nightkilled = Entry(nightframe, width=3, font=("Arial", 12))
    nightkilled.grid(row=0, column=1, sticky=W)
    is_missing = IntVar()  # эта переменная принимает значение 1, если был промах
    missing_button = Checkbutton(nightframe, text=("Промах"), font=("Arial", 12), variable=is_missing)
    missing_button.grid(row=0, column=2, sticky=W, columnspan=2)

    is_he_sheriff = IntVar()  # эта переменная принимат значение 1, если мы нажали на кнопку
    is_he_sheriffbutton = Checkbutton(nightframe, text=("Вскрывается шерифом"), font=("Arial", 11),
                                      variable=is_he_sheriff, command=killing_sheriff)
    is_he_sheriffbutton.grid(row=1, column=0, sticky=W, columnspan=2)

    color_of_dead_sheriff_check = IntVar()  # эта переменная принимает значение 1, если проверка убитого шерифа краснаях и 2, если черная
    check_of_dead_sheriff = Entry(nightframe, width=3, font=("Arial", 12))  # поле для ввода проверки убитого шерифа
    check_of_dead_sheriff_text = Label(nightframe, text="  проверенный ", font=("Arial", 11))
    red_dead_sheriff_check = Radiobutton(nightframe, text='красный', font=("Arial", 11),
                                         variable=color_of_dead_sheriff_check, value=1)
    black_dead_sheriff_check = Radiobutton(nightframe, text='черный', font=("Arial", 11),
                                           variable=color_of_dead_sheriff_check, value=2)

    continue_button = Button(nightframe, text="Далее", font=("Arial", 13), command=continue_)
    continue_button.grid(row=2, column=0, sticky=W)


night(count_of_steps)

window.mainloop()

