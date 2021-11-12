import os
import matplotlib.pyplot as plt


'''
    Create file maze without point reward
'''


def writeFile(filename):
    with open(filename, 'w') as outfile:
        outfile.write('5\n')
        outfile.write('1 21 -1\n')
        outfile.write('4 7 -3\n')
        outfile.write('6 13 -2\n')
        outfile.write('8 3 -3\n')
        outfile.write('9 19 -2\n')
        outfile.write('xxxxxxxxxxxxxxxxxxxxxxxxx\n')
        outfile.write('x  xxxx xxxx         +   \n')
        outfile.write('x x  xxxxxxx  xxxx      x\n')
        outfile.write('x    xxxxx      xxxx    x\n')
        outfile.write('x      +   xx xxxx      x\n')
        outfile.write('xxx xxxxx xxx xx   xx   x\n')
        outfile.write('x    xxxxxxx +          x\n')
        outfile.write('x         xx xxx xx  xxxx\n')
        outfile.write('x  +    xxxx xxxxxxx   xx\n')
        outfile.write('x xx               +    x\n')
        outfile.write('x  x   xxxx  xx         x\n')
        outfile.write('x    S xxxxxx  xxxxxxxxxx\n')
        outfile.write('xxxxxxxxxxxxxxxxxxxxxxxxx')


'''
    Read file maze to store maze and bonus points
'''


def readFile(filename):
    f = open(filename, 'r')
    n_bonus_points = int(next(f)[:-1])
    bonus_points = []

    for i in range(n_bonus_points):
        x, y, reward = map(int, next(f)[:-1].split(' '))
        bonus_points.append((x, y, reward))

    text = f.read()
    maze = [list(i) for i in text.splitlines()]
    f.close()

    return bonus_points, maze


'''
    Find start and exit point in the maze
'''


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


def visualize_maze(maze, bonus, start, end, route=None):
    """
    Args:
      1. maze: The maze read from the input file,
      2. bonus: The array of bonus points,
      3. start, end: The starting and ending points,
      4. route: The route from the starting point to the ending one, defined by an array of (x, y), e.g. route = [(1, 2), (1, 3), (1, 4)]
    """
    # 1. Define walls and array of direction based on the route
    walls = [(i, j) for i in range(len(maze))
             for j in range(len(maze[0])) if maze[i][j] == 'x']

    if route:
        direction = []
        for i in range(1, len(route)):
            if route[i][0]-route[i-1][0] > 0:
                direction.append('v')  # ^
            elif route[i][0]-route[i-1][0] < 0:
                direction.append('^')  # v
            elif route[i][1]-route[i-1][1] > 0:
                direction.append('>')
            else:
                direction.append('<')

        # direction.pop(0)

    # 2. Drawing the map
    ax = plt.figure(dpi=100).add_subplot(111)

    for i in ['top', 'bottom', 'right', 'left']:
        ax.spines[i].set_visible(False)

    plt.scatter([i[1] for i in walls], [-i[0] for i in walls],
                marker='X', s=100, color='black')

    plt.scatter([i[1] for i in bonus], [-i[0] for i in bonus],
                marker='P', s=100, color='green')

    plt.scatter(start[1], -start[0], marker='*',
                s=100, color='gold')

    if route:
        for i in range(len(route)-2):
            plt.scatter(route[i+1][1], -route[i+1][0],
                        marker=direction[i], color='silver')

    plt.text(end[1], -end[0], 'EXIT', color='red',
             horizontalalignment='center', verticalalignment='center')
    plt.xticks([])
    plt.yticks([])
    plt.show()

    print(f'Starting point (x, y) = {start[0], start[1]}')
    print(f'Ending point (x, y) = {end[0], end[1]}')

    for _, point in enumerate(bonus):
        print(
            f'Bonus point at position (x, y) = {point[0], point[1]} with point {point[2]}')
