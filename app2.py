import tkinter as tk
from tkinter import messagebox
import random

# Дані про слово "hra" з усіма 14 форм (7 для однини і 7 для множини)
words_data = {
    "hra": {
        "Nominative Singular": "hra",
        "Genitive Singular": "hry",
        "Dative Singular": "hře",
        "Accusative Singular": "hru",
        "Vocative Singular": "hro",
        "Locative Singular": "hře",
        "Instrumental Singular": "hrou",
        "Nominative Plural": "hry",
        "Genitive Plural": "her",
        "Dative Plural": "hrám",
        "Accusative Plural": "hry",
        "Vocative Plural": "hry",
        "Locative Plural": "hrách",
        "Instrumental Plural": "hrami"
    }
}

# Кількість тестів (питань)
num_tests = 5

# Лічильники правильних і неправильних відповідей
correct_count = 0
incorrect_count = 0

# Створення головного вікна (навчального)
learning_window = tk.Tk()
learning_window.title("Массур Вікторія - Чеська мова")
learning_window.geometry("500x450")

# Текст з навчальною інформацією
text = """Чеська мова має сім відмінків. Як і українська мова, чеська має складну систему відмінювання, яка вимагає запам'ятовування форм для різних відмінків.  Кожен відмінок має свої закінчення, які залежать від роду (чоловічий, жіночий, середній) та числа (однина, множина) іменника. Від української системи відмінків чеська відрізняється лиш тим, що за граматичною традицією орудний відмінок йде за місцевим, а кличний — за знахідним.

Чеська мова - назви відмінків | ukrajinština - názvy pádů | питання до них
Називний відмінок = 1. pád (nominativ) – otázky: Kdo? Co?
Родовий відмінок = 2. pád (genitiv) – otázky: Koho? Čeho?
Давальний відмінок = 3. pád (dativ) – otázky: Komu? Čemu?
Знахідний відмінок = 4. pád (akuzativ) – otázky: Koho? Co?
Кличний відмінок = 5. pád (vokativ) – otázky: -
Місцевий відмінок   = 6. pád (lokál)   – otázky: O kom? O čem? (používá se s předložkami)
Орудний відмінок = 7. pád (instrumentál) – otázky: S kým? S čím?
однина́ = jednotné číslo - jedn.č., j.č. (singulár)
множина́ = množné číslo - mn.č. (plurál)
чолові́чий рід = mužský rod (maskulinum)
жіно́чий рід = ženský rod (femininum)
сере́дній рід = střední rod (neutrum)
"""
label_text = tk.Label(learning_window, text=text, justify="left", wraplength=450)
label_text.pack(pady=20)

# Кнопка для переходу до тесту
button_to_quiz = tk.Button(learning_window, text="Перейти до тесту", command=lambda: show_quiz_window(0))
button_to_quiz.pack()

# Створення вікна для тесту
quiz_window = tk.Toplevel()
quiz_window.title("Массур Вікторія - Чеська мова: Тест")
quiz_window.geometry("500x300")
quiz_window.withdraw()

current_test = 0

def show_quiz_window(index):
    global current_test, selected_case, correct_answer, answers
    if index >= num_tests:
        messagebox.showinfo("Результати тесту", f"Правильних відповідей: {correct_count}\nНеправильних відповідей: {incorrect_count}")
        quiz_window.withdraw()
        learning_window.deiconify()
        return

    current_test = index
    # Використовуємо слово "hra"
    selected_word = "hra"
    forms = words_data[selected_word]
    # Випадково обираємо одну з 14 форм
    selected_case, correct_answer = random.choice(list(forms.items()))
    question_label.config(text=f"Яка форма слова '{selected_word}' у {selected_case}?")

    # Формуємо список унікальних варіантів, виключаючи всі входження правильної відповіді
    options = list({value for value in forms.values() if value != correct_answer})
    # Випадково обираємо 3 дистрактори, якщо їх достатньо
    distractors = random.sample(options, 3) if len(options) >= 3 else options

    answers = [correct_answer] + distractors
    random.shuffle(answers)

    for i, ans in enumerate(answers):
        radio_buttons[i].config(text=ans, value=ans)

    var.set(None)
    learning_window.withdraw()
    quiz_window.deiconify()

def check_answer():
    global current_test, correct_count, incorrect_count
    selected_option = var.get()
    if selected_option == correct_answer:
        correct_count += 1
        messagebox.showinfo("Результат", "Правильно!")
    else:
        incorrect_count += 1
        messagebox.showinfo("Результат", f"Ні, правильна відповідь: \"{correct_answer}\"")
    show_quiz_window(current_test + 1)

def return_to_learning():
    quiz_window.withdraw()
    learning_window.deiconify()

question_label = tk.Label(quiz_window, text="")
question_label.pack(pady=10)

var = tk.StringVar()
radio_buttons = [tk.Radiobutton(quiz_window, text="", variable=var, value="") for _ in range(4)]
for rb in radio_buttons:
    rb.pack(anchor="w")

button_answer = tk.Button(quiz_window, text="Відповісти", command=check_answer)
button_answer.pack(pady=10)

button_back = tk.Button(quiz_window, text="Повернутися до початкового вікна", command=return_to_learning)
button_back.pack(pady=10)

learning_window.mainloop()
