import timeit
from genetic2D import genetic
from exhaustive_search2D import exhaustive_search

for _ in range(1):

    # Параметры
    k = 100 # количесвто перестановок в начальной популяции
    g = 100 # количество поколений
    c_x = 20 # целевой центр тяжести по оси x
    c_y = 1.5 # целевой центр тяжести по оси y
    h1 = 19 # минимальная длина
    h2 = 41 # максимальная длина
    columns = 5 # количество столбцов для загрузки

    # # s0 = (a, b, p, name)
    # s1 = (2, 40, 6, 1)
    # s2 = (1, 9, 3, 2)
    # s3 = (4, 6, 4, 3)
    # s4 = (2, 8, 5, 4)
    # s5 = (5, 5, 5, 5)
    # s6 = (7, 3, 5, 6)
    # s7 = (8, 2, 1, 7)
    # s8 = (2, 40, 6, 8)
    # s9 = (1, 9, 3, 9)
    # s10 = (4, 6, 4, 10)
    # s11 = (2, 8, 5, 11)
    # s12 = (5, 5, 5, 12)
    # s13 = (7, 3, 5, 13)
    # s14 = (8, 2, 1, 14)
    # s15 = (2, 40, 6, 15)
    # s16 = (1, 9, 3, 16)
    # s17 = (4, 6, 4, 17)
    # s18 = (2, 8, 5, 18)
    # s19 = (5, 5, 5, 19)
    # s20 = (7, 3, 5, 20)
    # s21 = (8, 2, 1, 21)
    # s22 = (2, 40, 6, 22)
    # s23 = (1, 9, 3, 23)
    # s24 = (4, 6, 4, 24)
    # s25 = (2, 8, 5, 25)
    # s26 = (5, 5, 5, 26)
    # s27 = (7, 3, 5, 27)
    # s28 = (8, 2, 1, 28)


    # list_of_segments = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27, s28]
    s1 = (2, 7, 6, 1)
    s2 = (1, 9, 3, 2)
    s3 = (4, 6, 4, 3)
    s4 = (2, 8, 5, 4)
    s5 = (5, 5, 5, 5)
    s6 = (7, 3, 5, 6)
    s7 = (8, 2, 1, 7)
    s8 = (4, 6, 6, 8)
    s9 = (6, 4, 3, 9)
    s10 = (2, 8, 3, 10)


    list_of_segments = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
    print(f'Изначальный список всех сегментов: {list_of_segments}\n')


    # генетический метод
    print('Генетический метод:')
    start_time_genetic = timeit.default_timer()
    genetic(list_of_segments, k, g, c_x, c_y, h1, h2, columns)
    end_time_genetic = timeit.default_timer()
    print(f'Время поиска лучшей расстановки генетическим методом: {end_time_genetic - start_time_genetic}')

    # метод полного перебора
    print('Метод полного перебора:')
    start_time_exhaustive = timeit.default_timer()
    exhaustive_search(list_of_segments, c_x, c_y, h1, h2)
    end_time_exhaustive = timeit.default_timer()
    print(f'Время поиска лучшей расстановки полным перебором: {end_time_exhaustive - start_time_exhaustive} \n')