import sqlite3
import tkinter as tk
from tkinter import ttk

#завд 7
DATABASE_PATH = 'vocab.db'

#завдання 1: Створити базу даних (БД) SQLite для двомовного словника. БД містить одну таблицю під назвою vocab
#завдання 9
def create_and_fill_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

 #завдання 2:  Зробити мінімум 4 категорії, до яких належатимуть слова. Кожне слово в БД буде належати до однієї з категорій.   
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS vocab (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            foreign_word TEXT COLLATE NOCASE,
            ukrainian_translation TEXT,
            UNIQUE (category, foreign_word)
        )
    ''')
#завдання 3: Наповнити БД словами (мінімум 50) та їхніми перекладами, використавши інформацію з довільних доступних джерел. ID слів не повинні повторюватись (ключове поле таблиці). Кожне слово має бути прив’язане до певної категорії.
    data = [
        ('Кольори', 'modrá', 'синій'),
        ('Кольори', 'červená', 'червоний'),
        ('Кольори', 'žlutá', 'жовтий'),
        ('Кольори', 'zelená', 'зелений'),
        ('Кольори', 'černá', 'чорний'),
        ('Кольори', 'bílá', 'білий'),
        ('Кольори', 'šedá', 'сірий'),
        ('Кольори', 'oranžová', 'оранжевий'),
        ('Кольори', 'fialová', 'фіолетовий'),
        ('Кольори', 'růžová', 'рожевий'),
        
        ('Їжа', 'jablko', 'яблуко'),
        ('Їжа', 'banán', 'банан'),
        ('Їжа', 'chléb', 'хліб'),
        ('Їжа', 'mléko', 'молоко'),
        ('Їжа', 'sýr', 'сир'),
        ('Їжа', 'vejce', 'яйце'),
        ('Їжа', 'máslo', 'масло'),
        ('Їжа', 'maso', 'м’ясо'),
        ('Їжа', 'ryba', 'риба'),
        ('Їжа', 'zelenina', 'овочі'),
        
        ('Тварини', 'pes', 'собака'),
        ('Тварини', 'kočka', 'кіт'),
        ('Тварини', 'kůň', 'кінь'),
        ('Тварини', 'pták', 'птах'),
        ('Тварини', 'kráva', 'корова'),
        ('Тварини', 'ovce', 'вівця'),
        ('Тварини', 'prase', 'свиня'),
        ('Тварини', 'ryba', 'риба'),
        ('Тварини', 'zajíc', 'заєць'),
        ('Тварини', 'myš', 'миша'),
        
        ('Транспорт', 'auto', 'автомобіль'),
        ('Транспорт', 'autobus', 'автобус'),
        ('Транспорт', 'vlak', 'поїзд'),
        ('Транспорт', 'letadlo', 'літак'),
        ('Транспорт', 'loď', 'корабель'),
        ('Транспорт', 'motocykl', 'мотоцикл'),
        ('Транспорт', 'kolo', 'велосипед'),
        ('Транспорт', 'tramvaj', 'трамвай'),
        ('Транспорт', 'metro', 'метро'),
        ('Транспорт', 'taxi', 'таксі'),
        
        ('Час', 'hodina', 'година'),
        ('Час', 'minuta', 'хвилина'),
        ('Час', 'sekunda', 'секунда'),
        ('Час', 'den', 'день'),
        ('Час', 'týden', 'тиждень'),
        ('Час', 'měsíc', 'місяць'),
        ('Час', 'rok', 'рік'),
        ('Час', 'včera', 'вчора'),
        ('Час', 'dnes', 'сьогодні'),
        ('Час', 'zítra', 'завтра'),
        
        ('Природа', 'strom', 'дерево'),
        ('Природа', 'květina', 'квітка'),
        ('Природа', 'řeka', 'річка'),
        ('Природа', 'hora', 'гора'),
        ('Природа', 'moře', 'море'),
        ('Природа', 'obloha', 'небо'),
        ('Природа', 'slunce', 'сонце'),
        ('Природа', 'déšť', 'дощ'),
        ('Природа', 'vítr', 'вітер'),
        ('Природа', 'sníh', 'сніг')
    ]

    for category, foreign_word, ukrainian_translation in data:
        cursor.execute("SELECT COUNT(*) FROM vocab WHERE category = ? AND foreign_word = ?", (category, foreign_word))
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.execute('INSERT INTO vocab (category, foreign_word, ukrainian_translation) VALUES (?, ?, ?)', 
                           (category, foreign_word, ukrainian_translation))
    
    conn.commit()
    conn.close()

#створення та заповнення бази даних
create_and_fill_database()

#отримання списку категорій
def fetch_categories():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM vocab")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

#завдання 10 та 11
def fetch_words(category=None):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    if category:
        cursor.execute("SELECT category, foreign_word, ukrainian_translation FROM vocab WHERE category = ? ORDER BY foreign_word COLLATE NOCASE ASC", (category,))
    else:
        cursor.execute("SELECT category, foreign_word, ukrainian_translation FROM vocab ORDER BY foreign_word COLLATE NOCASE ASC")
    words = cursor.fetchall()
    conn.close()
    return words

#завдання 14
def update_table(category=None):
    words = fetch_words(category)
    for row in tree.get_children():
        tree.delete(row)
    for word in words:
        tree.insert('', tk.END, values=word)

#обробник вибору категорії в ComboBox
def on_category_change(event):
    selected_category = category_combo.get()
    update_table(selected_category)

#завдання 13
def on_row_select(event):
    selected_item = tree.focus()
    if selected_item:
        values = tree.item(selected_item, 'values')
        selected_label.config(text=f"{values[1]} — {values[2]}")

#завд 4: Створити новий графічний (віконний) проєкт. В заголовку форми вивести власне прізвище, ім’я та номер групи, номер ЛР.
root = tk.Tk()
root.title("Массур Вікторія Сергіївна - ПЛ, 4-й курс, 1 група - ЛР 3")

#завдання 5: У вікні програми зробити 2 вкладки (Tab): «Словник» і «Про автора». 
tab_control = ttk.Notebook(root)
tab_dict = ttk.Frame(tab_control)
tab_about = ttk.Frame(tab_control)
tab_control.add(tab_dict, text="Словник")
tab_control.add(tab_about, text="Про автора")
tab_control.pack(expand=1, fill="both")


title_label = tk.Label(tab_dict, text="Чесько-український словник", font=("Arial", 14))
title_label.pack(pady=5)

#завдання 6, 8
category_label = tk.Label(tab_dict, text="Виберіть категорію:", font=("Arial", 12))
category_label.pack()
category_combo = ttk.Combobox(tab_dict, values=fetch_categories(), font=("Arial", 12))
category_combo.pack(pady=5)
category_combo.bind("<<ComboboxSelected>>", on_category_change)


# Завдання 12: Реалізація смуг прокрутки в таблиці
frame = ttk.Frame(tab_dict)
frame.pack(fill=tk.BOTH, expand=True)

scrollbar_y = tk.Scrollbar(frame, orient="vertical")
scrollbar_x = tk.Scrollbar(frame, orient="horizontal")

columns = ('Категорія', 'Чеський переклад', 'Український переклад')
tree = ttk.Treeview(frame, columns=columns, show='headings', yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
tree.heading('Категорія', text='Категорія')
tree.heading('Чеський переклад', text='Чеський переклад')
tree.heading('Український переклад', text='Український переклад')

scrollbar_y.config(command=tree.yview)
scrollbar_x.config(command=tree.xview)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
tree.pack(fill=tk.BOTH, expand=True)


#виведення вибраного слова
selected_label = tk.Label(tab_dict, text="Вибране слово: ", font=("Arial", 12))
selected_label.pack(pady=5)

tree.bind('<ButtonRelease-1>', on_row_select)

update_table()

#завдання 5: У «Про автора» вивести інформацію про себе в елемент Label (або аналогічний). Шрифт — Arial, 16 пт., жирний, вирівнювання по центру форми, вміст напису — мінімум 2 рядки тексту (ПІБ, група тощо).
about_label = tk.Label(
    tab_about,
    text="Массур Вікторія Сергіївна\n"
         "Народилася 08.07.2004 року у Дніпрі. У 2021 році закінчила СШ № 134 м. Дніпра та \n"
         "вступила до Київського національного університету імені Тараса Шевченка на освітню програму \n"
         "«Прикладна (комп’ютерна) лінгвістика та англійська мова».",
    font=("Arial", 16, "bold"),
    justify="center"
)
about_label.pack(expand=True)

root.mainloop()
