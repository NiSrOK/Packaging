import json
import os
from exhaustive_search2D import exhaustive_search
import random
import timeit

class JsonObj:
    def __init__(self, count, list_of_segments, best_dev, best_dev_proc, c_x, c_y, h1, h2, worst_dev):
        self.count = count
        self.list_of_segments = list_of_segments
        self.best_dev = best_dev
        self.best_dev_proc = best_dev_proc
        self.c_x = c_x
        self.c_y = c_y
        self.h1 = h1
        self.h2 = h2
        self. worst_dev = worst_dev


def generate_base_population(n):
    list_of_segments = []
    for i in range(n):
        a = random.randint(1,20)
        b = random.randint(1,20)
        p = random.randint(1,20)
        name = i
        list_of_segments.append((a, b, p, name))
    return list_of_segments

# Функция для чтения JSON из файла
def read_json(filename):
    try:
        objects = []
        with open(filename, 'r') as file:
            data = json.load(file)
            for obj in data:
                calc = JsonObj(obj['count'], obj['list_of_segments'], obj['best_dev'], obj['best_dev_proc'], obj['c_x'], obj['c_y'], obj['h1'], obj['h2'], obj['worst_dev'])
                objects.append(calc)
        return objects
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON from file '{filename}': {e}")
        return None

def write_to_json(data, filename):
    # Проверяем, существует ли файл
    if os.path.exists(filename):
        # Если файл существует, считываем уже имеющиеся данные
        with open(filename, 'r') as file:
            try:
                existing_data = json.load(file)
            except json.decoder.JSONDecodeError:
                existing_data = []
    else:
        # Если файл не существует, создаем пустой список для данных
        existing_data = []

    # Добавляем новые данные к уже имеющимся
    existing_data.extend(data)

    # Записываем все данные в файл
    with open(filename, 'w') as file:
        json.dump(existing_data, file, indent=4)

def save_exhaustive(c_x, c_y, h1, h2, filename, sizeMin, sizeMax):
    for i in range(sizeMin, sizeMax+1):
        list_of_segments = generate_base_population(i)

        best_dev, best_dev_proc, worst_dev = exhaustive_search(list_of_segments, c_x, c_y, h1, h2, type='json')

        data = [
        {
            "count": i,
            "list_of_segments": list_of_segments,
            "best_dev": best_dev,
            "best_dev_proc": best_dev_proc,
            "c_x": c_x,
            "c_y": c_y,
            "h1": h1,
            "h2": h2,
            "worst_dev": worst_dev
        }
        ]
        write_to_json(data, filename)

    return read_json(filename)

# start_time_exhaustive = timeit.default_timer()
# save_exhaustive(100, 1.5, 1, 120, 'data.json', 20, 20)
# end_time_exhaustive = timeit.default_timer()
# total_time_exhaustive = end_time_exhaustive - start_time_exhaustive
# print("Total time for exhaustive search: ", total_time_exhaustive)


# c_x = 20
# c_y = 1.5
# h1 = 1 # минимальная длина
# h2 = 100 # максимальная длина
# filename = 'data.json'
# for i in range(3, 5):
#     list_of_segments = generate_base_population(i)

#     best_dev, best_dev_proc = exhaustive_search(list_of_segments, c_x, c_y, h1, h2, type='json')

#     data = [
#     {
#         "count": i,
#         "list_of_segments": list_of_segments,
#         "best_dev": best_dev,
#         "best_dev_proc": best_dev_proc,
#         "c_x": c_x,
#         "c_y": c_y,
#         "h1": h1,
#         "h2": h2
#     }
#     ]
#     write_to_json(data, filename)

# data = read_json(filename)
# print(data)
# if data:
#     for item in data:
#         print("count:", item["count"])
#         print("list_of_segments:", item["list_of_segments"])
#         print("best_dev:", item["best_dev"])
#         print("best_dev_proc:", item["best_dev_proc"])
#         print("c_x:", item["c_x"])
#         print("c_y:", item["c_y"])
#         print("h1:", item["h1"])
#         print("h2:", item["h2"])
#         print("\n")