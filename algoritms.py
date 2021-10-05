import time
from queue import PriorityQueue


def bfs(map, start, finish, aster):
    times = time.time()
    queue = [start]
    parents = {start: None}
    algorithmicTime(times)
    while len(queue) != 0:
        present_node = queue.pop(0)
        for i in range(len(aster)):
            if present_node == aster[i]:
                continue
        if present_node == finish:
            return getPath(parents, finish)
        for node in map[present_node]:
            if node not in parents:
                parents[node] = present_node
                queue.append(node)


def dfs(map, start, finish, aster):
    times = time.time()
    visited_nodes = []
    path = []
    List = PriorityQueue()
    List.put((0, start, path, visited_nodes))
    algorithmicTime(times)
    while not List.empty():
        depth, present_node, path, visited_nodes = List.get()
        for i in range(len(aster)):

            if present_node == aster[i]:
                continue
        if present_node == finish:
            return path + [present_node]

        visited_nodes = visited_nodes + [present_node]
        for node in map[present_node]:
            if node not in visited_nodes:
                if node == finish:
                    return path + [node]
                nodeDepth = len(path)
                List.put((-nodeDepth, node, path + [node], visited_nodes))
    return path


def ucs(map, start, finish):
    times = time.time()
    queue = [start]
    parents = {start: None}
    algorithmicTime(times)
    while len(queue) != 0:
        present_node = queue.pop(0)
        if present_node == finish:
            return getPath(parents, finish)

        neighbors = map[present_node]

        for node in neighbors:
            if node not in parents:
                parents[node] = present_node
                queue.append(node)


def algorithmicTime(startTime):
    result = time.time() - startTime
    if result != 0.0:
        print(result)


def getPath(parents, finish_nodes):
    arr = []
    current = finish_nodes
    while current is not None:
        arr.insert(0, current)
        current = parents[current]

    return arr
