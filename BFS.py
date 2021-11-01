from collections import deque

# create file maze without point reward
with open('maze_without_reward.txt', 'w') as outfile:
    outfile.write('xxxxxx\n')
    outfile.write('xxx  x\n')
    outfile.write('    xx\n')
    outfile.write('x x Sx\n')
    outfile.write('xxx  x\n')
    outfile.write('xxxxxx\n')


def readFile(file_name):
    f = open(file_name, 'r')

    text = f.read()
    maze = [list(i) for i in text.splitlines()]
    f.close()

    return maze


def findStartAndExitPosition(maze):
    row, col = len(maze), len(maze[0])
    start = (0, 0)
    end = ''

    for i in range(row):
        for j in range(col):
            if (maze[i][j] == 'S'):
                start = (i, j)

            elif (maze[i][j] == ' '):
                if (i == 0) or (i == len(maze) - 1) or (j == 0) or (j == len(maze[0]) - 1):
                    end = (i, j)

            else:
                pass

    return (start, end)


def isValid(maze, i, j):
    if not(0 <= i < len(maze) and 0 <= j < len(maze[0])):
        return False
    elif maze[i][j] == 'x':
        return False

    return True


def solveMaze(maze, start, end):
    row, col = len(maze), len(maze[0])
    directionss = [[0, -1], [0, 1], [1, 0], [-1, 0]]
    visited = [[False] * col for _ in range(row)]

    if start == end:
        return [start]

    queue = deque([(start, [])])

    while len(queue):
        coord, path = queue.popleft()
        visited[coord[0]][coord[1]] = True

        for move in directionss:
            move_x, move_y = coord[0] + move[0], coord[1] + move[1]

            if not((isValid(maze, move_x, move_y))):
                continue
            elif visited[move_x][move_y] == True:
                continue
            elif (move_x, move_y) == end:
                return path + [coord, (move_x, move_y)]
            else:
                queue.append(((move_x, move_y), path+[(move_x, move_y)]))
                visited[move_x][move_y] = True


def printByDirections(path):
    directions = {}

    for i in range(0, len(path) - 1):
        if path[i + 1][0]-path[i][0] > 0:
            directions.update({path[i]: 'v'})
        elif path[i + 1][0]-path[i][0] < 0:
            directions.update({path[i]: '^'})
        elif path[i + 1][1]-path[i][1] > 0:
            directions.update({path[i]: '>'})
        else:
            directions.update({path[i]: '<'})

    return directions


def printPath(maze, path):
    directions = printByDirections(path)

    for i, row_val in enumerate(maze):
        for j, col_val in enumerate(row_val):
            if (i, j) in directions.keys():
                print(directions[(i, j)], end='')
            else:
                print(col_val, end='')
        print()


maze = readFile('./maze_without_reward.txt')
(start, end) = findStartAndExitPosition(maze)
path = solveMaze(maze, start, end)
printPath(maze, path)
