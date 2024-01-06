from classes import Connection, create_list_of_connections, create_list_of_packages
import random

def divide_segments(segments, h1, h2):
    segments.sort(key=lambda x: x[0])  # Сортируем отрезки по начальным точкам

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

    if current_length >= h1:
        result_sets.append(current_set)

    # Выводим отрезки, которые не попали ни в один набор
    if not_in_any_set:
        print("Отрезки, которые не попали ни в один набор:")
        for segment in not_in_any_set:
            print(segment)

    return result_sets

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

def genetic_levels(list_of_levels, c, k):
    population = create_list_of_packages(list_of_levels, c)
    # for p in population:
    #     print(p.deviation)


def genetic(list_of_segments, k, g, c, h1, h2):
    list_of_levels = []
    # Разделение отрезков на наборы
    sets = divide_segments(list_of_segments, h1, h2)
    print(sets)
    # Создание начальной популяции
    for set in sets:
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
                child = perform_crossover(perm1, perm2)
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
                print("Лучшая расстановка:", res[0].list_of_segments)
                print("Лучшее значение отклонения от целевого центра тяжести:", res[1])
                if res[0].indent != None:
                    print("Отступ от левого края для соединения:", res[0].indent)
                find = True
                list_of_levels.append(res)
                break
                # return res[1]


        if find == False:
            print('Не удалось найти расстановку удовлетворяющую заданным параметрам.')
        
        if len(sets) == len(list_of_levels):
            genetic_levels(list_of_levels, c, k)


if __name__ == "__main__":

    h1 = 11 # минимальная длина
    h2 = 21 # максимальная длина

    s1 = (2, 40, 6, 1)
    s2 = (1, 9, 3, 2)
    s3 = (4, 6, 4, 3)
    s4 = (2, 8, 5, 4)
    s5 = (5, 5, 5, 5)
    s6 = (7, 3, 5, 6)
    s7 = (8, 2, 1, 7)
    list_of_segments = [s1, s2, s3, s4, s5, s6, s7]
    print(divide_segments(list_of_segments, h1, h2))