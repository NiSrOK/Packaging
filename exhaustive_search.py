import itertools
from classes import create_list_of_connections

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
    return best_dev



# exhaustive_search(list_of_segments, c, h1, h2)