import random
import sys
from matplotlib import pyplot as plt
from settings import *

matrix = [[0 for i in range(HEIGHT)] for j in range(WIDTH)]
sys.setrecursionlimit(99999999)


def check(matrix, ship_mask_with_pos):
    for point in ship_mask_with_pos:
        try:
            if matrix[point[1]][point[0]] == 5:
                return 1
            elif matrix[point[1]][point[0]] == 1:
                return 2
        except IndexError:
            return 2


visited = []
found = False


def bfs(matrix, current, player):
    print("seaching for bfs")
    global found, path, visited, queue
    queue.append(current)
    while len(queue) != 0 and not found:
        curr = queue[0]
        visited.append(curr)
        if found:
            queue.append(curr)
            return poped_queue
        visited.append(curr)
        WIN.set_at(curr, (0, 255, 255))
        pygame.display.update()
        for i in [(0, -accur), (-accur, 0), (accur, 0),
                  (0, accur)]:
            new_curr = (curr[0] + i[0], curr[1] + i[1])
            new_ship_mask_with_pos = [(int(h[0] + i[0] + new_curr[0] - YELLOW_SPACE_SHIP.get_width() / 2),
                                       int(h[1] + i[1] + new_curr[1] - YELLOW_SPACE_SHIP.get_height() / 2)) for h in
                                      player.mask.outline()]

            check_res = check(matrix, new_ship_mask_with_pos)
            if check_res == 'back':
                visited.append(new_curr)
            elif check(matrix, new_ship_mask_with_pos) == 'found':
                poped_queue.append(curr)
                poped_queue.append(new_curr)
                found = True
                return poped_queue
            elif new_curr not in visited:
                queue.append(new_curr)

        poped_queue.append(queue.pop(0))

    return []


def dfs(WIN, matrix, ship_mask_with_pos, path, curr):
    global found
    global visited
    if found:
        return path
    path = path
    curr = curr
    visited.append(curr)
    check_res = check(matrix, ship_mask_with_pos)
    if check_res == 'found':
        found = True
        return path
    elif not check_res:

        path.append(curr)
        for i in [(0, -accur), (-accur, 0), (accur, 0),
                  (0, accur), ]:
            new_curr = (curr[0] + i[0], curr[1] + i[1])
            new_ship_mask_with_pos = [(h[0] + i[0], h[1] + i[1]) for h in ship_mask_with_pos]
            if min(new_ship_mask_with_pos, key=lambda x: x[0])[0] < 0 or \
                    min(new_ship_mask_with_pos, key=lambda x: x[1])[1] < 0:
                continue
            elif found:
                break
            elif check(matrix, new_ship_mask_with_pos) == 'out':
                continue
            elif new_curr not in visited:
                path = dfs(WIN, matrix, new_ship_mask_with_pos, path, new_curr)
            else:
                continue
    return path


queue = []
poped_queue = []

path = []

matrix_uni = [[[] for i in range(WIDTH)] for j in range(HEIGHT)]


def uniform(matrix, current, player):
    print("searching ucs")
    global found, path, visited, queue
    queue.append(current)
    curr = current
    while len(queue) != 0 and not found:
        curr = queue[0]
        visited.append(curr)

        visited.append(curr)
        for i in [(0, -accur), (-accur, 0), (accur, 0),
                  (0, accur)]:
            new_curr = (curr[0] + i[0], curr[1] + i[1])
            new_ship_mask_with_pos = [(int(h[0] + i[0] + new_curr[0] - YELLOW_SPACE_SHIP.get_width() / 2),
                                       int(h[1] + i[1] + new_curr[1] - YELLOW_SPACE_SHIP.get_height() / 2)) for h in
                                      player.mask.outline()]

            check_res = check(matrix, new_ship_mask_with_pos)
            if check_res == 'back':
                visited.append(new_curr)
            elif check(matrix, new_ship_mask_with_pos) == 'found':
                poped_queue.append(curr)
                poped_queue.append(new_curr)
                found = True
                try:
                    matrix_uni[new_curr[1]][new_curr[0]] = curr
                except IndexError:
                    pass
                return find_way(matrix_uni, new_curr)
            elif new_curr not in visited:
                queue.append(new_curr)
                try:
                    matrix_uni[new_curr[1]][new_curr[0]] = curr
                except IndexError:
                    pass
        poped_queue.append(queue.pop(0))

    return []


class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(WIN, maze, start, end_center, mask, pl):
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    open_list = []
    closed_list = []
    open_list.append(start_node)
    counter = 750
    while len(open_list) > 0 and counter > 0:
        counter -= 1
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        open_list.pop(current_index)
        closed_list.append(current_node)
        if check(maze, [(h[0] + current_node.position[0] - int(YELLOW_SPACE_SHIP.get_width() / 2),
                         h[1] + current_node.position[1] - int(YELLOW_SPACE_SHIP.get_height() / 2)) for h in
                        mask]) == 1:

            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]


        children = []
        for new_position in [(0, -16), (0, 16), (-16, 0), (16, 0), (-16, -16), (-16, 16), (16, -16),
                             (16, 16)]:

            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if node_position[0] > WIDTH - 1 or node_position[0] < 1 or node_position[1] > HEIGHT - 1 or node_position[
                1] < 1:
                continue
            new_node = Node(current_node, node_position)
            children.append(new_node)
        for child in children:
            new_ship_mask_with_pos = [
                (h[0] + child.position[0] - int(YELLOW_SPACE_SHIP.get_width() / 2),
                 h[1] + child.position[1] - int(YELLOW_SPACE_SHIP.get_height() / 2)) for h in mask]
            if check(maze, new_ship_mask_with_pos) == 2:
                continue
            if min(new_ship_mask_with_pos, key=lambda x: x[0])[0] < 0 or \
                    min(new_ship_mask_with_pos, key=lambda x: x[1])[1] < 0:
                continue
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            child.g = current_node.g + 1
            child.h = (abs((child.position[0] - end_center[0])) + (abs(child.position[1] - end_center[1]))) ** 1 / 2
            child.f = child.g + child.h
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue


            for to_visit_node in open_list:
                if to_visit_node == child and to_visit_node.g < child.g:
                    continue

            open_list.append(child)
    if counter <= 0:
        pl.x += 20 * random.choice([-1, 1])


def find_way(uni_matrix, point):
    way = [point]
    while point:
        print('way', way)
        point = uni_matrix[point[1]][point[0]]
        if point:
            print('point not empty')
            way.append(point)
        elif point == []:
            print('returning way')
            return way


def search(player, invaders, bunkers, method):
    global matrix
    global visited, queue, path, found, line, poped_queue, matrix_uni
    lines = []

    for GOAL in invaders:
        matrix = [[0 for i in range(HEIGHT)] for j in range(WIDTH)]
        for inv in invaders:
            for invpoint in inv.mask.outline():
                try:
                    matrix[invpoint[1] + inv.y][invpoint[0] + inv.x] = 1
                except IndexError:
                    continue
            for laser in inv.lasers:
                for point in laser.mask.outline():
                    try:
                        matrix[point[1] + laser.y][point[0] + laser.x] = 1
                    except IndexError:
                        continue
        for i in GOAL.mask.outline():
            try:
                matrix[i[1] + GOAL.y][i[0] + GOAL.x] = 5
            except IndexError:
                continue

        pos = []
        for i in player.mask.outline():
            if method == 'dfs':
                pos.append((int(i[0]) + int(player.x), int(i[1]) + int(player.y)))
            elif method == 'bfs' or method == 'ucs' or method == 'star':
                pos.append((int(i[0]), int(i[1])))

        for bunker in bunkers:
            for point in bunker.mask.outline():
                try:
                    matrix[point[1] + bunker.y][point[0] + bunker.x] = 1
                except IndexError:
                    continue

        line = astar(WIN, matrix,
                     (
                     int(player.x + player.ship_img.get_width() / 2), int(player.y + player.ship_img.get_height() / 2)),
                     (int(GOAL.x + GOAL.ship_img.get_width() / 2), int(GOAL.y + GOAL.ship_img.get_height() / 2)), pos,
                     player)

        poped_queue = []
        matrix_uni = [[[] for i in range(WIDTH)] for j in range(HEIGHT)]
        if line:
            lines.append(line)
        found = False
        visited = []
        queue = []
        path = []
    found = False
    return lines

def draw_matrix(field):
    x = [0, WIDTH]
    y = [0, HEIGHT]
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j] > 0:
                x.append(int(j))
                y.append(int(HEIGHT - i))
    plt.scatter(x, y)
    plt.show()
