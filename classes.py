from random import shuffle, sample

# class Segment:
#     def __init__(self, a, b, p, name):
#         self.a = int(a)
#         self.b = int(b)
#         self.p = int(p)
#         self.name = name
    
#     def get_info(self):
#         print(f'a = {self.a}, b = {self.b}, p = {self.p}, name = {self.name}')

class Connection:
    def __init__(self, list_of_segments: list):
        self.a = None
        self.b = None
        self.p = None
        self.list_of_segments = list_of_segments
        self.deviation = None
    
    def __str__(self):
        return f"list_of_segments: {self.list_of_segments}"
    
    def calculate_connection(self):
        # s0 = (a, b, p, name)
        self.p = self.list_of_segments[0][2] + self.list_of_segments[1][2]
        self.a = (self.list_of_segments[0][2]*self.list_of_segments[0][0] + self.list_of_segments[1][2]*(self.list_of_segments[0][0] + self.list_of_segments[0][1] + self.list_of_segments[1][0]))/self.p
        self.b = self.list_of_segments[0][0] + self.list_of_segments[1][0] + self.list_of_segments[0][1] + self.list_of_segments[1][1] - self.a
        for i in range(2, len(self.list_of_segments)):
            old_a = self.a
            self.a = (self.p*self.a + self.list_of_segments[i][2]*(self.a + self.b + self.list_of_segments[i][0]))/(self.p+self.list_of_segments[i][2])
            self.b = old_a + self.list_of_segments[i][0] + self.b + self.list_of_segments[i][1] - self.a
            self.p += self.list_of_segments[i][2]
        return self
    
    def calculate_deviation(self, c):
        self.deviation = abs(self.a - c)
        # return self

    def randomize_connection(self):
        self.list_of_segments = sample(self.list_of_segments, len(self.list_of_segments))
        # return self

def increase_length(con, list_of_segments, len, h1, h2):
    for seg in list_of_segments:
        if (seg not in con.list_of_segments) and (seg[0]+seg[1]+len > h1) and (seg[0]+seg[1]+len < h2):
            con.list_of_segments.append(seg)
    return con

def approve_length(con, list_of_segments, h1, h2):
    len = 0
    flag = True
    while(flag):
        for seg in con.list_of_segments:
            len += seg[0] + seg[1]
        if len > h2:
            con.list_of_segments.pop()
            len = 0
        elif len < h1:
            increase_length(con, list_of_segments, len, h1, h2)
            return con
        else:
            return con

def create_list_of_connections(list_of_segments, k, c, h1, h2):
    list_of_connections = []
    for _ in range(k):
        con = Connection(list_of_segments=list_of_segments)
        con = approve_length(con, list_of_segments, h1, h2)
        con.randomize_connection()
        con.calculate_connection()
        con.calculate_deviation(c)
        # print(f'a = {con.a}')
        # print(f'b = {con.b}')
        list_of_connections.append(con)
    return list_of_connections


# s0 = (a, b, p, name)
if __name__ == "__main__":

    # s1 = Segment(3, 3, 10, 0)
    # s2 = Segment(3, 3, 10, 1)
    # s3 = Segment(2, 2, 4, 2)
    c = 5
    k = 10
    s1 = (3, 3, 10, 0)
    s2 = (3, 3, 10, 1)
    s3 = (2, 2, 4, 2)

    list_of_segments = [s1, s2, s3]

    # con = Connection(list_of_segments=list_of_segments)
    # print(con)
    # con.randomize_connection()
    # print(con)
    # con.calculate_connection()
    # con.calculate_deviation(c)
    # print(con)
    list_of_connections = create_list_of_connections(list_of_segments, k, c)
    for con in list_of_connections:
        print(con)

    # segment_1 = Segment(1, 3, 4)
    # segment_1.get_info()

    # permutations = [1, 2, 3, 4]