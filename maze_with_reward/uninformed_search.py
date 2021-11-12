from os import stat
import create_and_visualize as support_func
from queue import Empty, Queue
from numpy import inf

'''
    Create a class Node to store Node's information(state, parent, path, reward)
'''


class Cell():
    def __init__(self, parent, path, reward):
        self.parent = parent
        self.path = path
        self.reward = reward


# Check if the cell is valid to get it
def isValid(i, j):
    if not(0 <= i < row and 0 <= j < col):
        return False
    elif maze[i][j] == 'x':
        return False

    return True

# Assign value to a cell


def assignCellValue(i, j):
    cell_value = 0
    if maze[i][j] == ' ' and not((i == 0) or (i == len(maze) - 1) or (j == 0) or (j == len(maze[0]) - 1)):
        cell_value = 0

    for point in bonus:
        if (i, j) == (point[0], point[1]):
            cell_value = point[2]
            break

    return cell_value


def BFS(start_cell):
    Q.put((start_cell[0], start_cell[1]))

    while not Q.empty():
        curr_point = Q.get()

        # check for the neighbor of the visited node
        for neighbor in [[-1, 0], [1, 0], [0, 1], [0, -1]]:
            next_i, next_j = curr_point[0] + \
                neighbor[0], curr_point[1] + neighbor[1]

            if isValid(next_i, next_j):
                cell_path = graph[curr_point[0]][curr_point[1]].path
                cell_reward = graph[curr_point[0]][curr_point[1]].reward

                if (cell_path + 1 < graph[next_i][next_j].path):
                    graph[next_i][next_j].path = cell_path + 1
                    graph[next_i][next_j].reward = cell_reward + \
                        assignCellValue(curr_point[0], curr_point[1])
                    graph[next_i][next_j].parent = curr_point

                elif (cell_path + 1 > graph[next_i][next_j].path):
                    pass

                else:
                    if cell_reward + assignCellValue(curr_point[0], curr_point[1]) > graph[next_i][next_j].reward:
                        graph[next_i][next_j].path = cell_path + 1
                        graph[next_i][next_j].reward = cell_reward + \
                            assignCellValue(curr_point[0], curr_point[1])
                        graph[next_i][next_j].parent = curr_point

                if (is_push[next_i][next_j] == False):
                    is_push[next_i][next_j] = True
                    Q.put((next_i, next_j))


def findPath(S, E):
    states = [E]
    temp = graph[E[0]][E[1]].parent

    while temp:
        states.append((temp[0], temp[1]))
        temp = graph[temp[0]][temp[1]].parent

    states.reverse()
    return states, len(states) - 1 + graph[E[0]][E[1]].reward


Q = Queue()  # create queue contains coordinates of nodes in BFS function


'''Calling functions in support_func

    writeFile: create maze from text file
    readFile: return bonus_points and maze read from file
    findStartAndExitPosition: return coordinate of start and exit point in the maze 

'''
support_func.writeFile('maze_with_reward.txt')
bonus, maze = support_func.readFile('./maze_with_reward.txt')
(start, end) = support_func.findStartAndExitPosition(maze)
row = len(maze)
col = len(maze[0])


# Create graph contains Node in the maze
graph = [[Cell(None, inf, 0) for j in range(col)] for i in range(row)]
graph[start[0]][start[1]] = Cell(None, 0, 0)

# Check node cell if it is pushed into the queue
is_push = [[False for j in range(col)] for i in range(row)]

# BFS from start point
BFS(start)

# Return path and cost from starting point to exit point
states, cost = findPath(start, end)

# Visualize the path
support_func.visualize_maze(maze, bonus, start, end, states)

# Print the cost to console
print('The path cost: ', cost)
