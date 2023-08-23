from classes import create_list_of_connections

def get_density(element):
    return element[2]/(element[0]+element[1])

def heuristic(list_of_segments, c, h1, h2):
    # сортировка по убыванию плотности сегментов
    list_of_segments.sort(key=get_density, reverse=True)

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

    con = create_list_of_connections(heuristic_list, 1, c, h1, h2, random=False)

    print(f'Итоговая перестановка: {con[0].list_of_segments}')
    print(f'Отклонение: {con[0].deviation}')
    if con[0].indent != None:
        print("Отступ от левого края для соединения:", con[0].indent)

