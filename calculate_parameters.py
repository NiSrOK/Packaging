import random
from genetic import genetic
from exhaustive_search import exhaustive_search
from openpyxl import Workbook, load_workbook
import plotly.graph_objects as go
import timeit

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
    ws[f'A1'] = 'k'
    ws[f'B1'] = 'g'
    ws[f'C1'] = 'Среднее отклонение от наилучшего ц.т.'
    row = 2
    glob_res = []
    for k in range(1, 30):
        for g in range(1, 30):
            res = []
            for i in range(3, 10):
                list_of_segments = generate_base_population(i)
                h2 = calculate_length(list_of_segments)
                print(f'k = {k}, g = {g}')
                # start_time_genetic = timeit.default_timer()
                gen_dev = genetic(list_of_segments, k, g, c, h1, h2)
                # end_time_genetic = timeit.default_timer()
                # print(f'Время поиска лучшей расстановки генетическим методом: {end_time_genetic - start_time_genetic}')
                # start_time_exhaustive = timeit.default_timer()
                ex_dev = exhaustive_search(list_of_segments, c, h1, h2)
                # end_time_exhaustive = timeit.default_timer()
                # print(f'Время поиска лучшей расстановки полным перебором: {end_time_exhaustive - start_time_exhaustive} \n')
                # print(f'Отклонение результата генетического от полного перебора {abs(gen_dev-ex_dev)}')
                res.append(abs(gen_dev-ex_dev))
            dev = float('{:.3f}'.format(sum(res) / len(res)))
            if dev == 0:
                dev = 0.001
            glob_res.append((int(k), int(g), dev))
            ws[f'A{row}'] = k
            ws[f'B{row}'] = g
            ws[f'C{row}'] = dev
            row += 1
    wb.save("tuner.xlsx")
    return glob_res

def plot_3d_graph(data):
    # Разделение данных на отдельные списки для каждой координаты
    x_data, y_data, z_data = zip(*data)

    # Создание трехмерного графика
    fig = go.Figure(data=[go.Scatter3d(x=x_data, y=y_data, z=z_data, mode='markers', marker=dict(color='red', size=8))])

    # Настройка меток осей и установка логарифмической шкалы для оси Z
    fig.update_layout(scene=dict(xaxis_title='k', yaxis_title='g', zaxis_title='Среднее арифмитическое отклонения', zaxis=dict(type='log')))

    # Отображение графика
    fig.show()

def read_data(file_path):
    # Открываем Excel-файл
    wb = load_workbook(file_path)
    ws = wb.active
    data = []
    # Проходим по строкам и считываем данные
    for row in range(2, ws.max_row + 1):
        # Получаем значения из столбцов A, B, и C для текущей строки
        a_value = int(ws[f'A{row}'].value)
        b_value = int(ws[f'B{row}'].value)
        c_value = float(ws[f'C{row}'].value)

        data.append((a_value, b_value, c_value))

    # Закрываем Excel-файл
    wb.close()

    return data


c = 37 # целевой центр тяжести
h1 = 0
#res = tuner(c, h1)
res = read_data('tuner.xlsx')
# data_points = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
plot_3d_graph(res)
