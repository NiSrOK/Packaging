import timeit
import random
from genetic2D import genetic
from exhaustive_search2D import exhaustive_search
from db import create_and_connect, add_objects, get_all_objects

def generate_base_population(n):
    list_of_segments = []
    for i in range(n):
        a = random.randint(1,20)
        b = random.randint(1,20)
        p = random.randint(1,20)
        name = i
        list_of_segments.append((a, b, p, name))
    return list_of_segments

for _ in range(1):

    # Параметры
    # k = 100 # количесвто перестановок в начальной популяции
    g = 100 # количество поколений
    c_x = 20 # целевой центр тяжести по оси x
    c_y = 1.5 # целевой центр тяжести по оси y
    h1 = 19 # минимальная длина
    h2 = 41 # максимальная длина
    columns = 5 # количество столбцов для загрузки


    # db_name = input("Введите название базы данных: ")
    # c_x = float(input("Введите целевой центр тяжести по оси x: "))
    # c_y = float(input("Введите целевой центр тяжести по оси y: "))
    # h1 = float(input("Введите минимальную длину ряда: "))
    # h2 = float(input("Введите максимальную длину ряда: "))
    # columns = int(input("Введите количество столбцов для загрузки: "))





    # list_of_segments_base = generate_base_population(10)
    # print(f'Изначальный список всех отрезков: {list_of_segments_base}\n')

    # # создаем новую базу данных или подключаемся к существующей
    db_name = 'base.db'
    create_and_connect(db_name)

    # # записываем в базу данных все отрезки
    # add_objects(list_of_segments_base, db_name)

    #считываем из бд все отрезки
    list_of_segments = get_all_objects(db_name)
    print(f'\nСписок всех отрезков из бд: {list_of_segments}\n')

    k = int(len(list_of_segments)/7)


    # генетический метод
    # print('Генетический метод:')
    start_time_genetic = timeit.default_timer()
    genetic(list_of_segments, k, g, c_x, c_y, h1, h2, columns, type='None')
    end_time_genetic = timeit.default_timer()
    print(f'Время поиска упаковки генетическим методом: {end_time_genetic - start_time_genetic} сек')

    # метод полного перебора
    # print('Метод полного перебора:')
    # start_time_exhaustive = timeit.default_timer()
    # exhaustive_search(list_of_segments, c_x, c_y, h1, h2)
    # end_time_exhaustive = timeit.default_timer()
    # print(f'Время поиска лучшей расстановки полным перебором: {end_time_exhaustive - start_time_exhaustive} \n')