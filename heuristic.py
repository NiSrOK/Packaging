from classes import Connection, create_list_of_connections, approve_length

# Параметры
k = 4 # количесвто перестановок в начальной популяции
g = 5 # количество поколений
c = 21 # целевой центр тяжести
h1 = 2 # минимальная длина
h2 = 47.45 # максимальная длина
# c = 30 # целевой центр тяжести
# h1 = 2 # минимальная длина
# h2 = 85 # максимальная длина

# s0 = (a, b, p, name)
s1 = (1, 8, 5, 1)
s2 = (5, 9, 5, 2)
s3 = (4, 7, 5, 3)
s4 = (2, 8, 5, 4)
# s1 = (4, 4, 1, 1)
# s2 = (4, 4, 2, 2)
# s3 = (4, 4, 3, 3)
# s4 = (4, 4, 4, 4)
# s5 = (4, 4, 5, 5)
# s6 = (4, 4, 6, 6)
# s7 = (4, 4, 7, 7)
# s8 = (4, 4, 8, 8)
# s9 = (4, 4, 9, 9)
# s10 = (4, 4, 10, 10)

# list_of_segments = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10]
list_of_segments = [s1, s2, s3, s4]
print(f'Изначальный список всех сегментов: {list_of_segments}')

def get_density(element):
    # for num in element:
    #     print(num)
    # print(element[2]/(element[0]+element[1]))
    return element[2]/(element[0]+element[1])

def heuristic(list_of_segments, c, h1, h2):
    # сортировка по убыванию плотности сегментов
    list_of_segments.sort(key=get_density, reverse=True)
    print(list_of_segments)

    # самывй тяжелый элемент устанавливается на целевой центр тяжести
    left = list_of_segments[0][0]
    right = list_of_segments[0][1]

    heuristic_list = [list_of_segments[0]]

    for seg in list_of_segments[1:]:
        if (c - left > 0) and (h2 - c - right > 0): 
            # и слева и справа есть место, ставим туда, где его меньше
            if (c - left > h2 - c - right):
                heuristic_list.append(seg)
                right += seg[0] + seg[1] 
            else:
                heuristic_list.insert(0, seg)
                left += seg[0] + seg[1] 
        elif (c - left > 0):
            # место есть только слева, устанавливается только туда
            heuristic_list.insert(0, seg)
            left += seg[0] + seg[1] 
        else:
            # место есть только справа, устанавливается только туда
            heuristic_list.append(seg)
            right += seg[0] + seg[1] 
        
    print(f'heuristic_list = {heuristic_list}')
    con = create_list_of_connections(heuristic_list, 1, c, h1, h2, random=False)

    print(f'Итоговая перестановка: {con[0].list_of_segments}')
    print(f'Отклонение: {con[0].deviation}')
    if con[0].indent != None:
        print("Отступ от левого края для соединения:", con[0].indent)

