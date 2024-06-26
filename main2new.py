import timeit
import random
import tkinter as tk
from tkinter import messagebox
from genetic2D import genetic
from db import create_and_connect, get_all_objects

def generate_base_population(n):
    list_of_segments = []
    for i in range(n):
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        p = random.randint(1, 20)
        name = i
        list_of_segments.append((a, b, p, name))
    return list_of_segments

def submit():
    try:
        # Параметры
        # k = 100 # количесвто перестановок в начальной популяции
        g = 100 # количество поколений
        c_x = 20 # целевой центр тяжести по оси x
        c_y = 1.5 # целевой центр тяжести по оси y
        h1 = 19 # минимальная длина
        h2 = 41 # максимальная длина
        columns = 5 # количество столбцов для загрузки

        db_name = db_name_entry.get()
        c_x = float(c_x_entry.get())
        c_y = float(c_y_entry.get())
        h1 = float(h1_entry.get())
        h2 = float(h2_entry.get())
        columns = int(columns_entry.get())

        # Закрываем окно ввода данных
        root.destroy()

        # Основная логика программы
        create_and_connect(db_name)
        list_of_segments = get_all_objects(db_name)
        print(f'\nСписок всех отрезков из бд: {list_of_segments}\n')

        k = int(len(list_of_segments) / 7)

        # Генетический метод
        start_time_genetic = timeit.default_timer()
        genetic(list_of_segments, k, g, c_x, c_y, h1, h2, columns, type='None')
        end_time_genetic = timeit.default_timer()
        print(f'Время поиска упаковки генетическим методом: {end_time_genetic - start_time_genetic} сек')

        # Показать сообщение об успешной обработке данных
        messagebox.showinfo("Успех", "Данные успешно введены и обработаны.")
    except ValueError as e:
        messagebox.showerror("Ошибка", f"Ошибка ввода данных: {e}")

# Создание основного окна
root = tk.Tk()
root.title("Ввод данных")

# Устанавливаем размер окна
root.geometry("400x300")

# Название базы данных
tk.Label(root, text="Введите название базы данных:").grid(row=0, column=0)
db_name_entry = tk.Entry(root)
db_name_entry.grid(row=0, column=1)

# Целевой центр тяжести по оси x
tk.Label(root, text="Введите целевой центр тяжести по оси x:").grid(row=1, column=0)
c_x_entry = tk.Entry(root)
c_x_entry.grid(row=1, column=1)

# Целевой центр тяжести по оси y
tk.Label(root, text="Введите целевой центр тяжести по оси y:").grid(row=2, column=0)
c_y_entry = tk.Entry(root)
c_y_entry.grid(row=2, column=1)

# Минимальная длина ряда
tk.Label(root, text="Введите минимальную длину ряда:").grid(row=3, column=0)
h1_entry = tk.Entry(root)
h1_entry.grid(row=3, column=1)

# Максимальная длина ряда
tk.Label(root, text="Введите максимальную длину ряда:").grid(row=4, column=0)
h2_entry = tk.Entry(root)
h2_entry.grid(row=4, column=1)

# Количество столбцов для загрузки
tk.Label(root, text="Введите количество столбцов для загрузки:").grid(row=5, column=0)
columns_entry = tk.Entry(root)
columns_entry.grid(row=5, column=1)

# Кнопка для отправки данных
submit_button = tk.Button(root, text="Отправить", command=submit)
submit_button.grid(row=6, columnspan=2)

# Запуск основного цикла
root.mainloop()
