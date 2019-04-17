import pandas as pd
from collections import deque, namedtuple
import random
import math
from array import array

da = pd.read_csv('data.csv')

mylist = da.values.tolist()
# conver dataframe to list
# print(mylist)

#doc do thi tu file csv
trunggian = []
for ar in mylist:
    j = 0
    temp = []

    for i in ar:
        j = j + 1
        if j <= 2:
            temp.append(str(i))
        else:
            temp.append(i)
    trunggian.append(tuple(temp))

# print(len(trunggian))

# from collections import deque, namedtuple


# we'll use infinity as a default distance to nodes.
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')


def make_edge(start, end, cost=1):
    return Edge(start, end, cost)


class Graph:
    def __init__(self, edges):
        # let's check that the data is right
        # lay nhung canh ma khong co 2 hoac 3 phan tu nhet vao mang wrong_edges
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        # neu ma co canh loi thi in canh do ra
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))
        # dat ten cho tung thuoc tinh cua  edge
        self.edges = [make_edge(*edge) for edge in edges]

    # thuoc tinh
    @property
    def vertices(self):
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        # print(distances[dest])
        return path, distances[dest]


graph = Graph(trunggian)
PIN = 57

# print(graph.dijkstra('c', 'h'))

def get_fitness(gen):
    pre_step = gen[0]
    path = []
    dis = 0
    for i in range(1, len(gen)):
        path_temp, dis_temp = graph.dijkstra(pre_step, gen[i])
        path.append(path_temp)
        dis = dis + dis_temp
        pre_step = gen[i]
    return dis, path


def mutate(parent):
    temp = parent[1: len(parent) - 1]
    random.shuffle(temp)
    parent[1:len(parent) - 1] = temp
    return parent


def sac_pin(gen):
    pre_step = gen[0]
    path = []
    dis = 0
    is_sac = True
    for i in range(1, len(gen)):
        path_temp, dis_temp = graph.dijkstra(pre_step, gen[i])
        dis = dis + dis_temp
        try:
            val = int(gen[i])
            is_sac = True
            return False
        except ValueError:
            is_sac = False
        if dis > PIN:
            return True
        #path.append(path_temp)
        #dis = dis + dis_temp
        pre_step = gen[i]
    return False


# di, path_all = get_fitness(['a', 'c', 'h'])
# print('khoanh cach bang= ', di)
# print('quang duong la=')
# print(path_all)

def display(gen):
    print('\n________________\n')
    print('gen: ', gen)
    dis_p, path = get_fitness(gen)
    #print('duong di: ', path)
    print('chi phi: ', dis_p)
    # print(dir(path))

def add_tram_sac(gen, tram_sac):
    pre_step = gen[0]
    path = []
    dis = 0
    is_sac = True
    for i in range(1, len(gen)):
        path_temp, dis_temp = graph.dijkstra(pre_step, gen[i])
        dis = dis + dis_temp
        if dis > PIN:
            gen.insert(i-1,tram_sac.pop())
            return gen
        #path.append(path_temp)
        #dis = dis + dis_temp
    return gen


# khoi tao quan parent
#tap khach hang
bestParent = ['a', 'c', 'b', 'h', 'e', 'a']
sac = ['1', '2', '3']
parent_temp = bestParent[1:len(bestParent) - 1]

bestFitness, _ = get_fitness(bestParent)
so_gen = 0
gen_list_123 = []
gt = math.factorial(len(bestParent) - 2)

pre_dis = mutate(bestParent)
while True:
    child = mutate(bestParent)
    new = []
    for it in child:
        new.append(it)

    if so_gen > 1000000:
        print('out do so gen > 1000000')
        break

    if new not in gen_list_123:
        gen_list_123.append(new)
        so_gen = so_gen + 1
        # break
    else:
        continue

    # so_gen = so_gen + 1
    # print(len(gen_list))
    if so_gen >= gt and len(parent_temp) > 0:
        # gt = math.factorial(len(bestParent)-2)
        last_parent = parent_temp.pop()
        # print('last=', last_parent)
        bestParent.insert(len(bestParent) - 1, last_parent)
        gt = math.factorial(len(bestParent) - 2)

    if len(parent_temp) == 0:
        break
    childFitness, my_p = get_fitness(new)
    if childFitness > bestFitness:
        continue
    if deque([]) in my_p:
        pass
    else:
        display(new)
    pre_dis = childFitness
    
    if sac_pin(new):
        new = add_tram_sac(new, sac)
        
    # if so_gen > 10:
    #    break
    bestFitness = childFitness
    bestParent = new
