import itertools
from classes2D import create_list_of_connections
from classes2D import Connection
import random

def generate_base_population(n):
    list_of_segments = []
    for i in range(n):
        a = random.randint(1,20)
        b = random.randint(1,20)
        p = random.randint(1,20)
        name = i
        list_of_segments.append((a, b, p, name))
    return list_of_segments

def divide_segments(segments, h1, h2, c_x):

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

    # Выводим отрезки, которые не попали ни в один набор
    # if not_in_any_set:
    #     print("Отрезки, которые не попали ни в один набор:")
    #     for segment in not_in_any_set:
    #         print(segment)
    
    result_connections = []
    for set in result_sets:
        con = Connection(list_of_segments=set)
        con.calculate_connection()
        con.calculate_deviation(c_x, h1, h2)
        result_connections.append(con)

    return result_connections

def exhaustive_search(list_of_segments, c, h1, h2):
    
    permutations = list(itertools.permutations(list_of_segments))
    # print(len(permutations))
    population = []
    for perm in permutations:
        columns = divide_segments(perm, h1, h2, c)
        for col in columns:
            # ind = create_list_of_connections(col, 1, c, h1, h2, rand=False)
            # print(f'ind = {ind[0].list_of_segments}')
            # print(f'a = {ind[0].a}')
            # print(f'indent = {ind[0].indent}')
            # print(f'Отклонение: {ind[0].deviation}')
            population.append(col)
    
    # res = []
    # for ind in population:
    #     res.append((ind[0], ind[0].deviation))
    res = []
    for ind in population:
        res.append((ind.list_of_segments, ind.deviation, ind.indent))
    res.sort(key=lambda x: x[1])
    best_perm, best_dev, indent = res[0]
    worst_perm, worst_dev, indent = res[-1]
    # res.sort(key=lambda x: x[1])
    # best_perm, best_dev = res[0]
    # print(f'Лучшая перестановка: {best_perm}')
    # print(f'Минимальное отклонение: {best_dev}')
    # if indent != None:
    #     print("Отступ от левого края для соединения:", indent)
    return best_dev, worst_dev


# c = 50
# h1 = 1 # минимальная длина
# # h2 = 120 # максимальная длина
# h2 = 80 # максимальная длина
# exhaustive_search(generate_base_population(10), c, h1, h2)