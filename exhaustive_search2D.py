import itertools
from classes2D import create_list_of_connections
from classes2D import Package, Connection

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

def exhaustive_search(list_of_segments, c_x, c_y, h1, h2, type = 'work'):
    
    permutations = list(itertools.permutations(list_of_segments))
    # print(len(permutations))
    population = []
    for perm in permutations:
        columns = divide_segments(perm, h1, h2, c_x)
        individual = Package(columns)
        individual.calculate_deviation(c_x, c_y, h2)
        population.append(individual)
    
    res = []
    for ind in population:
        res.append((ind.list_of_columns, ind.deviation, ind.deviation_x, ind.deviation_y, ind.deviation_proc, ind.deviation_x_proc, ind.deviation_y_proc))
    res.sort(key=lambda x: x[1])
    best_perm, best_dev, best_dev_x, best_dev_y, best_dev_proc, best_dev_x_proc, best_dev_y_proc = res[0]
    worst_perm, worst_dev, worst_dev_x, worst_dev_y, worst_dev_proc, worst_dev_x_proc, worst_dev_y_proc = res[-1]

    if type == 'calculate':
        # print(f'Лучшая расстановка полным перебором:')
        # for column in best_perm:
        #     print(column.list_of_segments)
        return best_dev, worst_dev
    elif type == 'work':
        print(f'Лучшая перестановка:')
        for column in best_perm:
            print(column.list_of_segments)
        print(f'Минимальное отклонение: {best_dev}')
        print(f'Минимальное отклонение x: {best_dev_x}')
        print(f'Минимальное отклонение y: {best_dev_y}')
        print(f'Минимальное отклонение %: {best_dev_proc}')
        print(f'Минимальное отклонение x %: {best_dev_x_proc}')
        print(f'Минимальное отклонение y %: {best_dev_y_proc}')

        print(f'Худшая перестановка:')
        for column in worst_perm:
            print(column.list_of_segments)
        print(f'Максимальное отклонение: {worst_dev}')
        print(f'Максимальное отклонение x: {worst_dev_x}')
        print(f'Максимальное отклонение y: {worst_dev_y}')
        print(f'Максимальное отклонение %: {worst_dev_proc}')
        print(f'Максимальное отклонение x %: {worst_dev_x_proc}')
        print(f'Максимальное отклонение y %: {worst_dev_y_proc}')
    elif type == 'json':
        return best_dev, best_dev_proc, worst_dev


# # s0 = (a, b, p, name)
# s1 = (2, 7, 6, 1)
# s2 = (1, 9, 3, 2)
# s3 = (4, 6, 4, 3)
# s4 = (2, 8, 5, 4)
# s5 = (5, 5, 5, 5)
# s6 = (7, 3, 5, 6)
# s7 = (8, 2, 1, 7)
# s8 = (4, 6, 6, 8)
# s9 = (6, 4, 3, 9)
# s10 = (2, 8, 3, 10)


# list_of_segments = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]

# k = 20 # количесвто перестановок в начальной популяции
# g = 20 # количество поколений
# c_x = 20 # целевой центр тяжести по оси x
# c_y = 1.5 # целевой центр тяжести по оси y
# h1 = 19 # минимальная длина
# h2 = 41 # максимальная длина
# columns = 5 # количество столбцов для загрузки

# exhaustive_search(list_of_segments, c_x, c_y, h1, h2)