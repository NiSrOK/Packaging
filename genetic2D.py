from classes2D import Package, Connection, create_list_of_connections
import random

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
    # print(f'Хромосома от первого родителя: {child.list_of_segments}')
    j = 0
    for i in range(n):
        if j == a:
            j = b+1
        if perm2.list_of_segments[i] not in child.list_of_segments:
            child.list_of_segments[j] = perm2.list_of_segments[i]
            j += 1
    # print(f'Хромосома от второго родителя: {child.list_of_segments}')
    return child


def genetic_columns(list_of_segments, k, g, c, h1, h2):
    list_of_columns = []
    # Разделение отрезков на наборы
    sets = list_of_segments
    # print(sets)
    #для каждого столбца из набора
    for set in sets:
        #создадим популяцию из объектов в одном столбце 
        population = create_list_of_connections(set, k, c, h1, h2)

        for gen in range(1, g+1):
            # Рассчет пригодности для каждой перестановки
            fitness = []
            for perm in population:
                # print(perm.list_of_segments)
                fitness.append((perm, perm.deviation))
            fitness.sort(key=lambda x: x[1])
            best_perm, best_dev = fitness[0]
            # print(f'best_perm: {best_perm}')
            # print(f'best_dev: {best_dev}')

            # Проверка на оптимальное решение
            if best_dev == 0:
                break

            # Генерация потомков
            num_children = k - 1
            children = []
            while num_children > 0:
                perm1, perm2 = random.sample(population, 2)
                child = perform_crossover_columns(perm1, perm2)
                # child = approve_length(child, list_of_segments, h1, h2)
                child.calculate_connection()
                child.calculate_deviation(c, h1, h2)
                # Обмен двумя случайными сегментами в потомке
                i, j = random.sample(range(len(set)), 2)
                child.list_of_segments[i], child.list_of_segments[j] = child.list_of_segments[j], child.list_of_segments[i]
                children.append(child)
                num_children -= 1

            # Объединение родительской и дочерней популяции
            combined_pop = fitness + [(child, child.deviation) for child in children]
            combined_pop.sort(key=lambda x: x[1])
            # for per in combined_pop:
            #     print(per[0])
            # Замена худших перестановок лучшими
            # new_population = [combined_pop[i][0] for i in range(k-1)] + [best_perm]
            new_population = [combined_pop[i][0] for i in range(k)]
            # print(len(new_population))
            
            population = new_population

        # Вывод наилучшей перестановки, ее значение пригодности, начального отступа
        find = False
        for res in fitness:
            if (res[0].a + res[0].b >= h1) and (res[0].a + res[0].b <= h2):
                # print("Лучшая расстановка:", res[0].list_of_segments)
                # print("Лучшее значение отклонения от целевого центра тяжести:", res[1])
                # if res[0].indent != None:
                #     print("Отступ от левого края для соединения:", res[0].indent)
                find = True
                list_of_columns.append(res[0])
                break
                # return res[1]


        if find == False:
            print('Не удалось найти расстановку удовлетворяющую заданным параметрам.')
        
        if len(sets) == len(list_of_columns):
            return list_of_columns

# функция для разделения всех отрезков на наборы соответствующие ограничениям по длине
def divide_segments(segments, h1, h2):
    # segments.sort(key=lambda x: x[0])  # Сортируем отрезки по начальным точкам
    random.shuffle(segments)

    result_sets = []
    current_set = []
    current_length = 0
    not_in_any_set = []

    # segments_in_use = []
    # flag = True

    # while flag:
    #     if len(segments) == len(segments_in_use) or len(segments) == (len(segments_in_use) + len(not_in_any_set)):
    #         break
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

    # if current_length >= h1:
    #     result_sets.append(current_set)
    
    if current_length >= h1 and current_length <= h2:
        result_sets.append(current_set)
    elif current_length != 0:
        not_in_any_set.append(current_set)

    # Выводим отрезки, которые не попали ни в один набор
    if not_in_any_set:
        print("Отрезки, которые не попали ни в один набор:")
        for segment in not_in_any_set:
            print(segment)
    
    # result_connections = []
    # for set in result_sets:
    #     con = Connection(list_of_segments=set)
    #     result_connections.append(con)

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
    print(sorted_columns)

    # Возвращаем первые count_columns самых длинных столбцов
    return [column for length, column in sorted_columns[:count_columns]]

def population_preparation(list_of_segments, k, g, c_x, c_y, h1, h2, count_columns):
    # Разделение отрезков на наборы соответствующие ограничениям по длине
    base_list_columns = divide_segments(list_of_segments, h1, h2)
    if count_columns is not None and len(base_list_columns) > count_columns:
        # Возьмем нужное количество столбцов, приоритет - максимальная длина
        best_list_columns = get_best_columns(base_list_columns, count_columns)
    else:
        # Если нужное количество столбцов уже соответствует - берем все 
        best_list_columns = base_list_columns
    # Получаем список списков с лучшими расстановками объектов внутри столбцов 
    connections = genetic_columns(best_list_columns, k, g, c_x, h1, h2)
    population = []
    # print(connections)
    for _ in range(k):
        # if columns > len(connections):
        count_columns = len(connections)
        list_of_columns = random.sample(connections, count_columns)
        # for col in list_of_columns:
        #     random.shuffle(col.list_of_segments)
        #     col.calculate_connection()
        #     col.calculate_deviation(c_x, h1, h2)
        individual = Package(list_of_columns)
        individual.calculate_deviation(c_x, c_y, h2)
        population.append(individual)

    return population

# Вспомогательная функция для выполнения кроссовера
def perform_crossover(perm1, perm2):
    list_of_columns = []
    count_columns = len(perm1.list_of_columns)
    column = random.sample(perm1.list_of_columns, 1)
    column = column[0]
    list_of_columns.append(column)

    while len(list_of_columns) < count_columns:
        for i in range(count_columns):
            column = perm2.list_of_columns[i]
            # column = column.list_of_segments
            if column not in list_of_columns:
                list_of_columns.append(column)
                break
            if i == count_columns - 1:
                print("Невозможно выполнить кроссовер")
                a = input()
        
        if len(list_of_columns) < count_columns:
            for i in range(count_columns):
                column = perm1.list_of_columns[i]
                # column = column.list_of_segments
                if column not in list_of_columns:
                    list_of_columns.append(column)
                    break
                if i == count_columns - 1:
                    print("Невозможно выполнить кроссовер")
                    a = input()


    # list_of_columns_obj = []
    # for column in list_of_columns:
    #     list_of_columns_obj.append(Connection(list_of_segments=column))
    child = Package(list_of_columns)
    return child

# # Вспомогательная функция для выполнения кроссовера
# def perform_crossover(perm1, perm2):
#     list_of_columns = []
#     count_columns = len(perm1.list_of_columns)
#     column = random.sample(perm1.list_of_columns, 1)
#     column = column[0].list_of_segments
#     list_of_columns.append(column)

#     while len(list_of_columns) < count_columns:
#         for i in range(count_columns):
#             column = perm2.list_of_columns[i]
#             column = column.list_of_segments
#             if column not in list_of_columns:
#                 list_of_columns.append(column)
#                 break
#             if i == count_columns - 1:
#                 print("Невозможно выполнить кроссовер")
#                 a = input()
        
#         if len(list_of_columns) < count_columns:
#             for i in range(count_columns):
#                 column = perm1.list_of_columns[i]
#                 column = column.list_of_segments
#                 if column not in list_of_columns:
#                     list_of_columns.append(column)
#                     break
#                 if i == count_columns - 1:
#                     print("Невозможно выполнить кроссовер")
#                     a = input()


#     list_of_columns_obj = []
#     for column in list_of_columns:
#         list_of_columns_obj.append(Connection(list_of_segments=column))
#     child = Package(list_of_columns_obj)
#     return child


def genetic(list_of_segments, k, g, c_x, c_y, h1, h2, count_columns = None, calculate = False):
    # получение начальной популяции
    population = population_preparation(list_of_segments, k, g, c_x, c_y, h1, h2, count_columns)
    # for p in population:
    #     print(p.list_of_columns)
        # print(p.deviation)
        # print(p.deviation_x)
        # print(p.deviation_y)
        # print('-----------')

    for gen in range(1, g+1):
        # Рассчет пригодности для каждой перестановки
        fitness = []
        for perm in population:
            fitness.append((perm, perm.deviation))
        fitness.sort(key=lambda x: x[1])
        best_perm, best_dev = fitness[0]
        # print(f'Best dev: {best_dev}')

        # Проверка на оптимальное решение
        if best_dev == 0:
            break

        # Генерация потомков
        num_children = k - 1
        children = []
        while num_children > 0:
            perm1, perm2 = random.sample(population, 2)
            child = perform_crossover(perm1, perm2)
            for con in child.list_of_columns:
                con.calculate_connection()
                con.calculate_deviation(c_x, h1, h2)
            child.calculate_deviation(c_x, c_y, h2)
            # Обмен двумя случайными сегментами в потомке
            # i, j = random.sample(range(len(set)), 2)
            # child.list_of_segments[i], child.list_of_segments[j] = child.list_of_segments[j], child.list_of_segments[i]
            children.append(child)
            num_children -= 1

        # Объединение родительской и дочерней популяции
        combined_pop = fitness + [(child, child.deviation) for child in children]
        combined_pop.sort(key=lambda x: x[1])
        # for per in combined_pop:
        #     print(per[0])
        # Замена худших перестановок лучшими
        # new_population = [combined_pop[i][0] for i in range(k-1)] + [best_perm]
        new_population = [combined_pop[i][0] for i in range(k)]
        # print(len(new_population))
        
        population = new_population

    # Вывод наилучшей перестановки, ее значение пригодности, начального отступа
    
    if calculate:
        # print("Лучшая расстановка генетическим:")
        # for col in fitness[0][0].list_of_columns:
        #     print(col.list_of_segments)
        return fitness[0][0].deviation
    else:
        print("Лучшая расстановка:")
        i = 1
        for col in fitness[0][0].list_of_columns:
            print(f'{i}-ый столбец')
            print(col.list_of_segments)
            print(f'Смещение = {col.indent}')
            i += 1
        print(f'Минимальное отклонение: {fitness[0][0].deviation}')
        # print(f'Минимальное отклонение x: {fitness[0][0].deviation_x}')
        # print(f'Минимальное отклонение y: {fitness[0][0].deviation_y}')
        # print(f'Минимальное отклонение %: {fitness[0][0].deviation_proc}')
        # print(f'Минимальное отклонение x %: {fitness[0][0].deviation_x_proc}')
        # print(f'Минимальное отклонение y %: {fitness[0][0].deviation_y_proc}')
        # if res[0].indent != None:
        #     print("Отступ от левого края для соединения:", res[0].indent)


    # if find == False:
    #     print('Не удалось найти расстановку удовлетворяющую заданным параметрам.')
