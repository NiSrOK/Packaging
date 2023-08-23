import itertools
from classes import Connection, create_list_of_connections, approve_length

# Параметры
# k = 4 # количесвто перестановок в начальной популяции
# g = 5 # количество поколений
# c = 21 # целевой центр тяжести
# h1 = 2 # минимальная длина
# h2 = 47.45 # максимальная длина

# s1 = (1, 8, 5, 1)
# s2 = (5, 9, 5, 2)
# s3 = (4, 7, 5, 3)
# s4 = (2, 8, 5, 4)

# list_of_segments = [s1, s2, s3, s4]
# list_of_segments = [s1, s2]

def exhaustive_search(list_of_segments, c, h1, h2):
    
    permutations = list(itertools.permutations(list_of_segments))
    # print(len(permutations))
    population = []
    for perm in permutations:
        ind = create_list_of_connections(perm, 1, c, h1, h2, random=False)
        # print(f'ind = {ind[0].list_of_segments}')
        # print(f'a = {ind[0].a}')
        # print(f'indent = {ind[0].indent}')
        # print(f'Отклонение: {ind[0].deviation}')
        population.append(ind)
    
    res = []
    for ind in population:
        res.append((ind[0], ind[0].deviation))
    # print(f'len population {len(population)}')
    res.sort(key=lambda x: x[1])
    best_perm, best_dev = res[0]
    print(f'Лучшая перестановка: {best_perm.list_of_segments}')
    print(f'Минимальное отклонение: {best_dev}')
    if best_perm.indent != None:
        print("Отступ от левого края для соединения:", best_perm.indent)



# exhaustive_search(list_of_segments, c, h1, h2)