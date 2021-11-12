import os
import matplotlib.pyplot as plt


'''
    Create file maze without point reward
'''

# Map 1
with open('maze_without_reward1.txt', 'w') as outfile:
    outfile.write('0\n')
    outfile.write('xxxxxxxxxxxxxxxxxxxxxx\n')
    outfile.write('xxS                 xx\n')
    outfile.write('xxx x x   xx        xx\n')
    outfile.write('xxxx x xx x xxxxxxx xx\n')
    outfile.write('x    x xx   xx       x\n')
    outfile.write('xxx            x x   x\n')
    outfile.write('x     xxxxx   xxxxxxxx\n')
    outfile.write('xxxxx xxxxxxxxxxxxxxxx')

#Map 2(Map ma GBFS chay khong toi uu)
with open('maze_without_reward2.txt', 'w') as outfile:
    outfile.write('0\n')
    outfile.write('xxxxxxxxxxxxxxxxxxxxxx\n')
    outfile.write('x                     \n')
    outfile.write('x   xxxxxxxxxxxxxx xxx\n')
    outfile.write('xxx x           xx xxx\n')
    outfile.write('xxx   xxxxxxxxx xx xxx\n')
    outfile.write('xxxxx x         xx xxx\n')
    outfile.write('xS    x xxxxxxxxxx xxx\n')
    outfile.write('xxxxxxx            xxx\n')
    outfile.write('xxxxxxxxxxxxxxxxxxxxxx')

#Map 3(Map ma GBFS voi A* chay tuong tu nhau)
with open('maze_without_reward3.txt', 'w') as outfile:
    outfile.write('0\n')
    outfile.write('xxxxxxxxxxxxxxxxxxxxxx\n')
    outfile.write('x   xx    xxx    x    \n')
    outfile.write('x   xx xxxxxxxx xx xxx\n')
    outfile.write('xxx x           xx xxx\n')
    outfile.write('xxx   xxxxxxxxx xx xxx\n')
    outfile.write('xxxxx x            xxx\n')
    outfile.write('xS    x xxxxxxxxxxxxxx\n')
    outfile.write('xxxxxxx            xxx\n')
    outfile.write('xxxxxxxxxxxxxxxxxxxxxx')

#Map 4(Map cua thay)
with open('maze_without_reward4.txt', 'w') as outfile:
    outfile.write('0\n')
    outfile.write('xxxxxxxxxxxxxxxxxxxxxx\n')
    outfile.write('x   x   xx xx        x\n')
    outfile.write('x     x     xxxxxxxxxx\n')
    outfile.write('x x    xx  xxxx xxx xx\n')
    outfile.write('  x   x x xx   xxxx  x\n')
    outfile.write('x          xx  xx  x x\n')
    outfile.write('xxxxxxx x      xx  x x\n')
    outfile.write('xxxxxxxxx  x x  xx   x\n')
    outfile.write('x          x x Sx x  x\n')
    outfile.write('xxxxx x  x x x     x x\n')
    outfile.write('xxxxxxxxxxxxxxxxxxxxxx')

# Map 5 (big map)
with open('maze_without_reward5.txt', 'w') as outfile:
    outfile.write('0\n')
    outfile.write('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n')
    outfile.write('x      x                            x\n')
    outfile.write('x  x  xx  xxxxxxxxxxxxxxx x  xxxx x x\n')
    outfile.write('x     xx  xx  xxxxxxxx               \n')
    outfile.write('x  xxxxx  xxx x           x   xxxxxxx\n')
    outfile.write('x xxx      xxxx   xx    xx  xx      x\n')
    outfile.write('x xxx                           xxxxx\n')
    outfile.write('x                     xx      xxxxxxx\n')
    outfile.write('x xxxxxxxxxx      xxxxxx    xxx     x\n')
    outfile.write('x xxxxxxxxxxx       xxxxxxxxxxxxxxxxx\n')
    outfile.write('x xxxxxxxxx       xxxx           xxxx\n')
    outfile.write('x xxx   xxxxx       xxxxxxxxxx      x\n')
    outfile.write('x xx           xx  xxxxxxxxx       xx\n')
    outfile.write('xS    xxxxxxxxxxxxxxxx  xxxxx    xxxx\n')
    outfile.write('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

'''
    Read file maze to store maze and bonus points
'''


def readFile(file_name):
    f = open(file_name, 'r')
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


def visualize_maze(maze, bonus, start, end, route=None, type=1):
    """
    Args:
      1. maze: The maze read from the input file,
      2. bonus: The array of bonus points,
      3. start, end: The starting and ending points,
      4. route: The route from the starting point to the ending one, defined by an array of (x, y), e.g. route = [(1, 2), (1, 3), (1, 4)]
      5. type: Use to customize visualizing path clearer (1- normal size map, 2 - big size map)
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

        direction.pop(0)

    # 2. Drawing the map
    ax = ''
    if type == 1:
        ax = plt.figure(dpi=100).add_subplot(111)
    else:
        ax = plt.figure(figsize=(10, 6), dpi=100).add_subplot(111)

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
