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
h2 = 80 # максимальная длина
count_columns = 20

population = generate_base_population(20)
list_of_segments = population

genetic(list_of_segments, 30, 30, c_x, c_y, h1, h2, count_columns, type='None')


    # # s0 = (a, b, p, name)
    # s1 = (2, 40, 6, 1)
    # s2 = (1, 9, 3, 2)
    # s3 = (4, 6, 4, 3)
    # s4 = (2, 8, 5, 4)
    # s5 = (5, 5, 5, 5)
    # s6 = (7, 3, 5, 6)
    # s7 = (8, 2, 1, 7)
    # s8 = (2, 40, 6, 8)
    # s9 = (1, 9, 3, 9)
    # s10 = (4, 6, 4, 10)
    # s11 = (2, 8, 5, 11)
    # s12 = (5, 5, 5, 12)
    # s13 = (7, 3, 5, 13)
    # s14 = (8, 2, 1, 14)
    # s15 = (2, 40, 6, 15)
    # s16 = (1, 9, 3, 16)
    # s17 = (4, 6, 4, 17)
    # s18 = (2, 8, 5, 18)
    # s19 = (5, 5, 5, 19)
    # s20 = (7, 3, 5, 20)
    # s21 = (8, 2, 1, 21)
    # s22 = (2, 40, 6, 22)
    # s23 = (1, 9, 3, 23)
    # s24 = (4, 6, 4, 24)
    # s25 = (2, 8, 5, 25)
    # s26 = (5, 5, 5, 26)
    # s27 = (7, 3, 5, 27)
    # s28 = (8, 2, 1, 28)


    # list_of_segments = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27, s28]
    # s1 = (2, 7, 6, 1)
    # s2 = (1, 9, 3, 2)
    # s3 = (4, 6, 4, 3)
    # s4 = (2, 8, 5, 4)
    # s5 = (5, 5, 5, 5)
    # s6 = (7, 3, 5, 6)
    # s7 = (8, 2, 1, 7)
    # s8 = (4, 6, 6, 8)
    # s9 = (6, 4, 3, 9)
    # s10 = (2, 8, 3, 10)