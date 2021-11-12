import create_and_visualize as support


class Node():
    def __init__(self, state, action, parent, h=0, g=0):
        self.state = state
        self.action = action
        self.parent = parent
        self.h = h
        self.g = g


class PriorQueueForA():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        dem = 0
        for i in range(len(self.frontier)):
            if node.h+node.g <= self.frontier[i].h+self.frontier[i].g:
                dem = i
                break
        self.frontier.insert(dem, node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class PriorQueueForGBFS(PriorQueueForA):
    def add(self, node):
        dem = 0
        for i in range(len(self.frontier)):
            if node.h <= self.frontier[i].h:
                dem = i
                break
        self.frontier.insert(dem, node)


def makeWall(maze):
    height = len(maze)
    width = len(maze[0])
    wall = []
    for i in range(height):
        row = []
        for j in range(width):
            if maze[i][j] == 'x':
                row.append(True)
            else:
                row.append(False)
        wall.append(row)
    return wall


def neighbor(node):
    row, col = node.state
    candidates = [
        ("up", (row - 1, col)),
        ("down", (row + 1, col)),
        ("left", (row, col - 1)),
        ("right", (row, col + 1))
    ]
    res = []
    for action, (r, c) in candidates:
        if 0 <= r < row and 0 <= c < col and not walls[r][c]:
            distanct = abs(end[0]-r)+abs(end[1]-c)
            temp = Node((r, c), action, node, distanct, node.g+1)
            res.append(temp)
    return res


def neighbor_for_gbfs(node):
    row, col = node.state
    candidates = [
        ("up", (row - 1, col)),
        ("down", (row + 1, col)),
        ("left", (row, col - 1)),
        ("right", (row, col + 1))
    ]
    res = []
    for action, (r, c) in candidates:
        if 0 <= r < row and 0 <= c < col and not wall[r][c]:
            distanct = abs(end[0]-r)+abs(end[1]-c)
            temp = Node((r, c), action, node, distanct)
            res.append(temp)
    return res

# type=0 -> Greedy best first search
# type=1 -> A* search


def solve_maze(maze, start, end, type):
    num_explored = 0
    distanct = abs(end[0]-start[0])+abs(end[1]-start[1])
    start_node = Node(start, None, None, distanct, 0)
    if type == 0:
        fringe = PriorQueueForGBFS()
    else:
        fringe = PriorQueueForA()
    fringe.add(start_node)
    explored = set()
    while True:
        if fringe.empty():
            raise Exception("No path")
        node = fringe.remove()
        num_explored += 1
        states = []
        actions = []
        if node.state == end:
            while node is not None:
                states.append(node.state)
                actions.append(node.action)
                node = node.parent
            states.reverse()
            return states, num_explored
        explored.add(node.state)
        if type == 0:
            for node_neighbor in neighbor_for_gbfs(node):
                if node_neighbor.state not in explored and not fringe.contains_state(node_neighbor.state):
                    fringe.add(node_neighbor)
        else:
            for node_neighbor in neighbor(node):
                if node_neighbor.state not in explored and not fringe.contains_state(node_neighbor.state):
                    fringe.add(node_neighbor)


support.writeFile('maze_without_reward.txt')
bonus, maze = support.readFile('./maze_without_reward.txt')
(start, end) = support.findStartAndExitPosition(maze)
wall = makeWall(maze)
row = len(maze)
col = len(maze[0])


# type=0 -> Greedy best first search
# states,num_explored=solve_maze(maze,start,end,0)

# type=1 -> A* search
states, num_explored = solve_maze(maze, start, end, 1)

# print(states)
support.visualize_maze(maze, bonus, start, end, states)
