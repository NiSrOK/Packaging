from classes2D import Package, Connection, create_list_of_connections
import random
import tkinter as tk
from tkinter import ttk

# Вспомогательная функция для выполнения кроссовера
def perform_crossover_columns(perm1, perm2):
    n = len(perm1.list_of_segments)
    a = random.randint(0, n-1)
    b = random.randint(0, n-1)
    if a > b:
        a, b = b, a
    child = Connection(list_of_segments=[None] * n)
    for i in range(a, b+1):
        child.list_of_segments[i] = perm1.list_of_segments[i]
    j = 0
    for i in range(n):
        if j == a:
            j = b+1
        if perm2.list_of_segments[i] not in child.list_of_segments:
            child.list_of_segments[j] = perm2.list_of_segments[i]
            j += 1

    return child


def genetic_columns(list_of_segments, k, g, c, h1, h2):
    list_of_columns = []
    # Разделение отрезков на наборы
    sets = list_of_segments
    #для каждого столбца из набора
    for set in sets:
        #создадим популяцию из объектов в одном столбце 
        population = create_list_of_connections(set, k, c, h1, h2)

        for gen in range(1, g+1):
            # Рассчет пригодности для каждой перестановки
            fitness = []
            for perm in population:
                fitness.append((perm, perm.deviation))
            fitness.sort(key=lambda x: x[1])
            best_perm, best_dev = fitness[0]

            # Проверка на оптимальное решение
            if best_dev == 0:
                break

            # Генерация потомков
            num_children = k - 1
            children = []
            while num_children > 0:
                perm1, perm2 = random.sample(population, 2)
                child = perform_crossover_columns(perm1, perm2)
                child.calculate_connection()
                child.calculate_deviation(c, h1, h2)
                # Обмен двумя случайными сегментами в потомке
                if len(set) > 1:
                    i, j = random.sample(range(len(set)), 2)
                    child.list_of_segments[i], child.list_of_segments[j] = child.list_of_segments[j], child.list_of_segments[i]
                children.append(child)
                num_children -= 1

            # Объединение родительской и дочерней популяции
            combined_pop = fitness + [(child, child.deviation) for child in children]
            combined_pop.sort(key=lambda x: x[1])
            new_population = [combined_pop[i][0] for i in range(k)]
            
            population = new_population

        # Вывод наилучшей перестановки, ее значение пригодности, начального отступа
        find = False
        for res in fitness:
            if (res[0].a + res[0].b >= h1) and (res[0].a + res[0].b <= h2):
                find = True
                list_of_columns.append(res[0])
                break

        if find == False:
            print('Не удалось найти расстановку удовлетворяющую заданным параметрам.')
        
        if len(sets) == len(list_of_columns):
            return list_of_columns

# функция для разделения всех отрезков на наборы соответствующие ограничениям по длине
def divide_segments(segments, h1, h2):
    random.shuffle(segments)

    result_sets = []
    current_set = []
    current_length = 0
    not_in_any_set = []

    for segment in segments:
        length = segment[0] + segment[1]  # Длина отрезка
        if length > h2:
            not_in_any_set.append(segment)
            continue
        if current_length + length <= h2:
            current_set.append(segment)
            current_length += length
        elif current_length >= h1:
            result_sets.append(current_set)
            current_set = [segment]
            current_length = length
        else:
            not_in_any_set.append(segment)
    
    if current_length >= h1 and current_length <= h2:
        result_sets.append(current_set)
    elif current_length != 0:
        not_in_any_set.append(current_set)

    return result_sets

def get_best_columns(base_list_columns, count_columns):
    list_len_column = []

    for column in base_list_columns:
        len_column = 0
        for segment in column:
            len_column += segment[0] + segment[1]
        list_len_column.append((len_column, column))  # Сохраняем пару (длина столбца, столбец)

    # Сортируем столбцы по длине в убывающем порядке
    sorted_columns = sorted(list_len_column, reverse=True)

    # Возвращаем первые count_columns самых длинных столбцов
    return [column for length, column in sorted_columns[:count_columns]]

def population_preparation(list_of_segments, k, g, c_x, c_y, h1, h2, count_columns_base):
    # Разделение отрезков на наборы соответствующие ограничениям по длине
    base_list_columns = divide_segments(list_of_segments, h1, h2)
    if len(base_list_columns) > count_columns_base:
        # Возьмем нужное количество столбцов, приоритет - максимальная длина
        best_list_columns = get_best_columns(base_list_columns, count_columns_base)
    else:
        # Если нужное количество столбцов уже соответствует - берем все 
        best_list_columns = base_list_columns
    # Получаем список списков с лучшими расстановками объектов внутри столбцов 
    connections = genetic_columns(best_list_columns, k, g, c_x, h1, h2)
    population = []
    for _ in range(k):
        count_columns = len(connections)
        list_of_columns = random.sample(connections, count_columns)
        individual = Package(list_of_columns, count_columns_base)
        individual.calculate_deviation(c_x, c_y, h2)
        population.append(individual)

    return population

# Вспомогательная функция для выполнения кроссовера
def perform_crossover(perm1, perm2, count_columns_base):
    list_of_columns = []
    count_columns = len(perm1.list_of_columns)
    column = random.sample(perm1.list_of_columns, 1)
    column = column[0]
    list_of_columns.append(column)

    while len(list_of_columns) < count_columns:
        for i in range(count_columns):
            column = perm2.list_of_columns[i]
            if column not in list_of_columns:
                list_of_columns.append(column)
                break
            if i == count_columns - 1:
                print("Невозможно выполнить кроссовер")
                a = input()
        
        if len(list_of_columns) < count_columns:
            for i in range(count_columns):
                column = perm1.list_of_columns[i]
                if column not in list_of_columns:
                    list_of_columns.append(column)
                    break
                if i == count_columns - 1:
                    print("Невозможно выполнить кроссовер")
                    a = input()

    child = Package(list_of_columns, count_columns_base)
    return child

class FitnessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Информация об упаковке")

        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.info_label = ttk.Label(self.main_frame, text="Упаковка:")
        self.info_label.grid(row=0, column=0, sticky=tk.W)
        self.row = 1

    def display_fitness_info(self, fitness_data):
        for widget in self.main_frame.winfo_children()[1:]:
            widget.destroy()  # Удаляем предыдущие виджеты, кроме главной метки

        row = 1
        for fit in fitness_data:
            for i, col in enumerate(fit[0].list_of_columns, start=1):
                col_label = ttk.Label(self.main_frame, text=f'{i}-ый столбец:')
                col_label.grid(row=row, column=0, sticky=tk.W)
                row += 1

                seg_label = ttk.Label(self.main_frame, text=f'Отрезки: {col.list_of_segments}')
                seg_label.grid(row=row, column=1, sticky=tk.W)
                row += 1

                indent_label = ttk.Label(self.main_frame, text=f'Смещение внутри столбца: {"%.3f" % col.indent}')
                indent_label.grid(row=row, column=1, sticky=tk.W)
                row += 1

            indent_y_label = ttk.Label(self.main_frame, text=f'Смещение упаковки: {"%.3f" % fit[0].indent_y}')
            indent_y_label.grid(row=row, column=0, sticky=tk.W)
            row += 1

            deviation_label = ttk.Label(self.main_frame, text=f'Минимальное отклонение упаковки: {"%.3f" % fit[0].deviation}')
            deviation_label.grid(row=row, column=0, sticky=tk.W)
            row += 1

def genetic(list_of_segments, k, g, c_x, c_y, h1, h2, count_columns, type):
    # получение начальной популяции
    population = population_preparation(list_of_segments, k, g, c_x, c_y, h1, h2, count_columns)

    for gen in range(1, g+1):
        # Рассчет пригодности для каждой перестановки
        fitness = []
        for perm in population:
            fitness.append((perm, perm.deviation))
        fitness.sort(key=lambda x: x[1])
        best_perm, best_dev = fitness[0]

        # Проверка на оптимальное решение
        if best_dev == 0:
            break

        # Генерация потомков
        num_children = k - 1
        children = []
        while num_children > 0:
            perm1, perm2 = random.sample(population, 2)
            child = perform_crossover(perm1, perm2, count_columns)
            for con in child.list_of_columns:
                con.calculate_connection()
                con.calculate_deviation(c_x, h1, h2)
            child.calculate_deviation(c_x, c_y, h2)
            children.append(child)
            num_children -= 1

        # Объединение родительской и дочерней популяции
        combined_pop = fitness + [(child, child.deviation) for child in children]
        combined_pop.sort(key=lambda x: x[1])
        new_population = [combined_pop[i][0] for i in range(k)]
        
        population = new_population
    
    if type == 'calculate':
        return fitness[0][0].deviation
    elif type == 'multyple':
        return fitness[0][0]
    else:
        root = tk.Tk()
        app = FitnessApp(root)
        app.display_fitness_info(fitness)
        root.mainloop()
        # print("Упаковка:")
        # i = 1
        # for col in fitness[0][0].list_of_columns:
        #     print(f'{i}-ый столбец')
        #     print(col.list_of_segments)
        #     print(f'Смещение внутри столбца = {col.indent}')
        #     i += 1
        # print(f'Смещение упаковки = {fitness[0][0].indent_y}')
        # print(f'Минимальное отклонение упаковки: {fitness[0][0].deviation}')
