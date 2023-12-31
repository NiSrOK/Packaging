# Код начинается с определения данных задачи размещения, включая размещаемые сегменты, количество перестановок в начальной популяции (k), количество поколений (g) 
# и максимальное отклонение для идеального решения (max_deviation).
# Начальная популяция генерируется случайным образом с помощью функции numpy.random.permutation. Это создает k перестановок сегментов в случайном порядке.
# Затем начинается цикл генетического алгоритма. Для каждого поколения центроид и отклонение рассчитываются для каждой перестановки в популяции. 
# Центроид — это среднее положение всех сегментов в перестановке, а отклонение — это евклидово расстояние между каждым сегментом и центроидом. 
# Эти значения хранятся в массивах центроидов и отклонений соответственно.
# Затем наиболее эффективная перестановка и ее отклонение копируются из текущей популяции. Это будет использоваться позже для сравнения с перестановками потомков.

import timeit
from exhaustive_search import exhaustive_search
from heuristic import heuristic
from genetic import genetic
from classes import approve_length

for _ in range(1):
    # Параметры
    # k = 4 # количесвто перестановок в начальной популяции
    # g = 5 # количество поколений
    # c = 15 # целевой центр тяжести
    # h1 = 2 # минимальная длина
    # h2 = 100 # максимальная длина

    # Параметры
    k = 4 # количесвто перестановок в начальной популяции
    g = 5 # количество поколений
    c = 37 # целевой центр тяжести
    h1 = 19 # минимальная длина
    h2 = 41 # максимальная длина

    # Генерация начальной популяции
    # s0 = (a, b, p, name)
    # s1 = (2, 8, 6, 1)
    # s2 = (1, 9, 3, 2)
    # s3 = (4, 6, 4, 3)
    # s4 = (2, 8, 5, 4)
    # s5 = (5, 5, 5, 5)
    # s6 = (7, 3, 5, 6)
    # s7 = (8, 2, 1, 7)

    s1 = (2, 40, 6, 1)
    s2 = (1, 9, 3, 2)
    s3 = (4, 6, 4, 3)
    s4 = (2, 8, 5, 4)
    s5 = (5, 5, 5, 5)
    s6 = (7, 3, 5, 6)
    s7 = (8, 2, 1, 7)
    s8 = (2, 40, 6, 8)
    s9 = (1, 9, 3, 9)
    s10 = (4, 6, 4, 10)
    s11 = (2, 8, 5, 11)
    s12 = (5, 5, 5, 12)
    s13 = (7, 3, 5, 13)
    s14 = (8, 2, 1, 14)


    list_of_segments = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14]
    print(f'Изначальный список всех сегментов: {list_of_segments}\n')

    # print(f'Проверка суммарной длины сегментов:')
    # status, list_of_segments = approve_length(list_of_segments, h1, h2)
    # if status == 'LengthIsTooShort':
    #     print(f'Суммарная длина сегментов меньше {h1}.\n')
    #     break
    # elif status == 'LengthIsTooLong':
    #     print(f'Суммарная длина сегментов больше {h2}. Алгоритму не удалось исключить лишние сегменты.\n')
    #     break
    # elif status == 'WrongLength':
    #     print(f'Некорректная длина одного из сегментов.\n')
    #     break
    # elif status == 'LengthIsTooShortAfterAlg':
    #     print(f'После работы алгоритма суммарная длина сегментов меньше {h1}.\n')
    #     break
    # elif status == 'LengthIsAcceptable':
    #     print(f'Суммарная длина сегментов в заданном списке корректна.\n')
    # elif status == 'SegmentListChanged':
    #     print(f'Список сегментов был изменен для соблюдения суммарной длины.')
    #     print(f'Новый список сегментов: {list_of_segments}\n')

    # # метод полного перебора
    # print('Метод полного перебора:')
    # start_time_exhaustive = timeit.default_timer()
    # exhaustive_search(list_of_segments, c, h1, h2)
    # end_time_exhaustive = timeit.default_timer()
    # print(f'Время поиска лучшей расстановки полным перебором: {end_time_exhaustive - start_time_exhaustive} \n')

    # # эвристический метод
    # print('Эвристический метод:')
    # start_time_heuristic = timeit.default_timer()
    # heuristic(list_of_segments, c, h1, h2)
    # end_time_heuristic = timeit.default_timer()
    # print(f'Время поиска расстановки эвристическим методом: {end_time_heuristic - start_time_heuristic} \n')


    # генетический метод
    print('Генетический метод:')
    start_time_genetic = timeit.default_timer()
    genetic(list_of_segments, k, g, c, h1, h2)
    end_time_genetic = timeit.default_timer()
    print(f'Время поиска лучшей расстановки генетическим методом: {end_time_genetic - start_time_genetic}')
