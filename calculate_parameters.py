import random
from genetic import genetic
from exhaustive_search import exhaustive_search
from openpyxl import Workbook

def generate_base_population(n):
    list_of_segments = []
    for i in range(n):
        a = random.randint(1,40)
        b = random.randint(1,40)
        p = random.randint(1,40)
        name = i
        list_of_segments.append((a, b, p, name))
    return list_of_segments

def calculate_length(list_of_segments):
    length = 0
    for i in range(len(list_of_segments)):
        length += list_of_segments[i][0] + list_of_segments[i][1]
    return length

def tuner( c, h1):
    wb = Workbook()
    ws = wb.active
    row = 1
    glob_res = []
    for k in range(1, 20):
        for g in range(1, 20):
            res = []
            for i in range(5, 8):
                list_of_segments = generate_base_population(i)
                h2 = calculate_length(list_of_segments)
                print(f'k = {k}, g = {g}')
                gen_dev = genetic(list_of_segments, k, g, c, h1, h2)
                ex_dev = exhaustive_search(list_of_segments, c, h1, h2)
                # print(f'Отклонение результата генетического от полного перебора {abs(gen_dev-ex_dev)}')
                res.append(abs(gen_dev-ex_dev))
            glob_res.append((k, g, '{:.3f}'.format(sum(res) / len(res))))
            ws[f'A{row}'] = k
            ws[f'B{row}'] = g
            ws[f'C{row}'] = '{:.3f}'.format(sum(res) / len(res))
            row += 1
    wb.save("tuner.xlsx")
    return glob_res


c = 37 # целевой центр тяжести
h1 = 0
print(tuner(c, h1))
