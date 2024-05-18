import random
from genetic2D import genetic

def generate_base_population(n):
    list_of_segments = []
    for i in range(n):
        a = random.randint(1,20)
        b = random.randint(1,20)
        p = random.randint(1,20)
        name = i
        list_of_segments.append((a, b, p, name))
    return list_of_segments

c_x = 50 # целевой центр тяжести по x
c_y = 10.5 # целевой центр тяжести по y
h1 = 1 # минимальная длина
# h2 = 120 # максимальная длина
h2 = 80 # максимальная длина
count_columns = 20

population = generate_base_population(20)
list_of_segments = population

genetic(list_of_segments, 30, 30, c_x, c_y, h1, h2, count_columns, type='None')