from random import shuffle, sample
from math import sqrt
import copy
import random

class Package:
    def __init__(self, list_of_columns: list, count_of_columns: int):
        self.list_of_columns = list_of_columns
        self.deviation_x = None
        self.deviation_y = None
        self.deviation = None
        self.row_width = 1
        self.indent_y = 0
        self.count_of_columns = count_of_columns

        self.deviation_proc = None
        self.deviation_x_proc = None
        self.deviation_y_proc = None
    
    def calculate_deviation(self, c_x, c_y, h2):
        sum_p = 0
        sum_px = 0
        sum_py = 0
        num = 0
        # h2 = 41
        for column in self.list_of_columns:
            num += 1
            sum_p += column.p
            sum_px += column.p*(column.a + column.indent)
            sum_py += column.p*(self.row_width*num - self.row_width/2)
            
        # self.deviation_x = abs(sum_px / (sum_p*c_x) - 1)*100
        # self.deviation_y = abs(sum_py / (sum_p*c_y) - 1)*100

        self.deviation_x = abs(sum_px / (sum_p) - c_x)
        self.deviation_y = abs(sum_py / (sum_p) - c_y)

        free_columns = self.count_of_columns - num
        if (c_y > sum_py/sum_p) and (free_columns > 0):
            if free_columns > (c_y - sum_py/sum_p):
                self.deviation_y = 0
                self.indent_y = c_y - sum_py/sum_p
            else:
                self.deviation_y = (c_y - sum_py/sum_p) - free_columns
                self.indent_y = free_columns

        self.deviation = sqrt(self.deviation_x**2 + self.deviation_y**2)
        self.deviation_x_proc = abs(sum_px / (sum_p) - c_x) / h2 * 100
        self.deviation_y_proc = abs(sum_py / (sum_p) - c_y) / (num*self.row_width) * 100
        self.deviation_proc = sqrt(self.deviation_x_proc**2 + self.deviation_y_proc**2)

class Connection:
    def __init__(self, list_of_segments: list):
        self.a = None
        self.b = None
        self.p = None
        self.list_of_segments = list_of_segments
        self.deviation = None
        self.indent = 0
    
    def calculate_connection(self):
        # s0 = (a, b, p, name)
        if len(self.list_of_segments) == 1:
            self.a = self.list_of_segments[0][0]
            self.b = self.list_of_segments[0][1]
            self.p = self.list_of_segments[0][2]
            return self
        else:
            self.p = self.list_of_segments[0][2] + self.list_of_segments[1][2]
            self.a = (self.list_of_segments[0][2]*self.list_of_segments[0][0] + self.list_of_segments[1][2]*(self.list_of_segments[0][0] + self.list_of_segments[0][1] + self.list_of_segments[1][0]))/self.p
            self.b = self.list_of_segments[0][0] + self.list_of_segments[1][0] + self.list_of_segments[0][1] + self.list_of_segments[1][1] - self.a
            for i in range(2, len(self.list_of_segments)):
                old_a = self.a
                self.a = (self.p*self.a + self.list_of_segments[i][2]*(self.a + self.b + self.list_of_segments[i][0]))/(self.p+self.list_of_segments[i][2])
                self.b = old_a + self.list_of_segments[i][0] + self.b + self.list_of_segments[i][1] - self.a
                self.p += self.list_of_segments[i][2]
            return self
    
    def calculate_deviation(self, c, h1, h2):
        if self.a < c:
            if c > h2 - self.b:
                self.indent = h2 - self.b - self.a
                self.deviation = c - h2 + self.b
            else:
                self.indent = c - self.a
                self.deviation = 0
        else:
            self.deviation = abs(self.a - c)

def create_list_of_connections(list_of_segments, k, c, h1, h2, rand = True):
    list_of_connections = []
    for _ in range(k):
        copy_list_of_segments = copy.deepcopy(list_of_segments)
        random.shuffle(copy_list_of_segments)
        con = Connection(list_of_segments=copy_list_of_segments)
        # con = approve_length(con, list_of_segments, h1, h2)
        # if random:
        #     con.randomize_connection()
        con.calculate_connection()
        con.calculate_deviation(c, h1, h2)
        list_of_connections.append(con)
    return list_of_connections

# def create_list_of_packages(list_of_columns, c, random = True):
#     list_of_packages = []
#     pack = Package(list_of_columns=list_of_columns)
#     if random:
#         pack.randomize_package()
#     pack.calculate_deviation(list_of_columns, c)
#     list_of_packages.append(pack)
#     return list_of_packages