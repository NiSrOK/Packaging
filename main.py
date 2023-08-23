# Код начинается с определения данных задачи размещения, включая размещаемые сегменты, количество перестановок в начальной популяции (k), количество поколений (g) 
# и максимальное отклонение для идеального решения (max_deviation).
# Начальная популяция генерируется случайным образом с помощью функции numpy.random.permutation. Это создает k перестановок сегментов в случайном порядке.
# Затем начинается цикл генетического алгоритма. Для каждого поколения центроид и отклонение рассчитываются для каждой перестановки в популяции. 
# Центроид — это среднее положение всех сегментов в перестановке, а отклонение — это евклидово расстояние между каждым сегментом и центроидом. 
# Эти значения хранятся в массивах центроидов и отклонений соответственно.
# Затем наиболее эффективная перестановка и ее отклонение копируются из текущей популяции. Это будет использоваться позже для сравнения с перестановками потомков.

import random
from classes import Connection, create_list_of_connections, approve_length

# Параметры
k = 4 # количесвто перестановок в начальной популяции
g = 5 # количество поколений
c = 15 # целевой центр тяжести
h1 = 2 # минимальная длина
h2 = 100 # максимальная длина

# Вспомогательная функция для выполнения кроссовера
def perform_crossover(perm1, perm2):
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

# def perform_crossover(perm1, perm2):
#     n = len(perm1.list_of_segments)
#     a = random.randint(1, n-2)
#     b = a  # change here
#     child = Connection(list_of_segments=[None] * n)
#     for i in range(0, a+1):
#         child.list_of_segments[i] = perm1.list_of_segments[i]
#     j = 0
#     for i in range(n):
#         if j == a:
#             j = b+1
#         if perm2.list_of_segments[i] not in child.list_of_segments:
#             child.list_of_segments[j] = perm2.list_of_segments[i]
#             j += 1
#     return child


# Генерация начальной популяции
# segments = [(1,2,3), (4,5,6), (7,8,9), (10,11,12), (13,14,15)]
# population = [random.sample(segments, len(segments)) for _ in range(k)]
# s0 = (a, b, p, name)
s1 = (1, 8, 5, 1)
s2 = (5, 9, 5, 2)
s3 = (4, 7, 5, 3)
s4 = (2, 8, 5, 4)
# s5 = (1, 6, 5, 5)
# s6 = (5, 3, 5, 6)
# s7 = (5, 8, 15, 7)


# list_of_segments = [s1, s2, s3, s4, s5, s6, s7]
list_of_segments = [s1, s2, s3, s4]
print(f'Изначальный список всех сегментов: {list_of_segments}')

population = create_list_of_connections(list_of_segments, k, c, h1, h2)

for gen in range(1, g+1):
    # Рассчет пригодности для каждой перестановки
    fitness = []
    for perm in population:
        print(perm.list_of_segments)
        fitness.append((perm, perm.deviation))
    fitness.sort(key=lambda x: x[1])
    best_perm, best_dev = fitness[0]
    print(best_perm)
    print(best_dev)

    # Проверка на оптимальное решение
    if best_dev == 0:
        break

    # Генерация потомков
    num_children = k - 1
    children = []
    while num_children > 0:
        perm1, perm2 = random.sample(population, 2)
        child = perform_crossover(perm1, perm2)
        child = approve_length(child, list_of_segments, h1, h2)
        child.calculate_connection()
        child.calculate_deviation(c)
        # Обмен двумя случайными сегментами в потомке
        i, j = random.sample(range(len(list_of_segments)), 2)
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

# Вывод наилучшей перестановки и ее значение пригодности
find = False
for res in fitness:
    if (res[0].a + res[0].b > h1) and (res[0].a + res[0].b < h2):
        print("Лучшая расстановка:", res[0].list_of_segments)
        print("Лучшее значение отклонения от центра тяжести:", res[1])
        find = True
        break

if find == False:
    print('Не удалось найти расстановку удовлетворяющую заданным параметрам.')

# print("Best permutation:", best_perm)
# print("Fitness value:", best_dev)
