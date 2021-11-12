import create_and_visualize as support


# Create a class Node to store Node's information(state, parent, action)
class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


# Create class Stack to use find path by DFS
class Stack():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception('Frontier is empty!')
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


# Create class Queue inheritance to use find path by BFS
class Queue(Stack):
    def remove(self):
        if self.empty():
            raise Exception('Frontier is empty!')
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


# Make wall from cell equal "x"
def makeWall(maze):
    wall = []
    row, col = len(maze), len(maze[0])

    for i in range(row):
        row_val = []
        for j in range(col):
            if maze[i][j] == 'x':
                row_val.append(True)
            else:
                row_val.append(False)
        wall.append(row_val)

    return wall


# Get neighbors around the node is visited
def neighbors(node):
    x, y = node.state

    neighbors = [
        ('right', (x, y+1)),
        ('up', (x-1, y)),
        ('left', (x, y-1)),
        ('down', (x+1, y))
    ]

    res = []
    for action, (r, c) in neighbors:
        if (0 <= r < row and 0 <= c < col and wall[r][c] == False):
            temp = Node((r, c), node, action)
            res.append(temp)

    return res


def solveMaze(maze, start, end, type):
    num_explored = 0  # get the numbers of cell have visited
    start_node = Node(state=start, parent=None, action=None)

    fringe = Stack()
    if type == 1:
        fringe = Queue()
    elif type == 2:
        fringe = Stack()
    fringe.add(start_node)
    visited = set()

    while True:
        if fringe.empty():
            raise Exception('No solution')
        node = fringe.remove()
        num_explored += 1

        if node.state == end:
            actions = []
            states = []
            while node is not None:
                actions.append(node.action)
                states.append(node.state)
                node = node.parent
            states.reverse()
            return states, num_explored

        visited.add(node.state)

        for neighbor_node in neighbors(node):
            if neighbor_node.state not in visited and not fringe.contains_state(neighbor_node.state):
                fringe.add(neighbor_node)


'''Calling functions in support functions
    writeFile: create maze from text file
    readFile: return bonus_points and maze read from file (can change filename to get another maze)
    findStartAndExitPosition: return coordinate of start and exit point in the maze 
'''
bonus, maze = support.readFile('maze_without_reward1.txt')
(start, end) = support.findStartAndExitPosition(maze)
wall = makeWall(maze)
row = len(maze)
col = len(maze[0])

# Choose 1 or 2 in order to perform BFS or DFS algorithm
type_solve = int((input('BFS-->1 or DFS-->2 ? ')))

# Solution
path, num_explored = solveMaze(maze, start, end, type_solve)

# visualize maze and path (change type = 1 or 2 to be suitable for map size)
support.visualize_maze(maze, bonus, start, end, path, 2)

print('Tong so cac trang thai da di: ', num_explored)
print('Chi phi duong di: ', len(path))
