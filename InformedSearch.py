import os
import matplotlib.pyplot as plt
#Map 1
# with open('maze_without_reward.txt', 'w') as outfile:
#     outfile.write('2\n')
#     outfile.write('3 6 -3\n')
#     outfile.write('5 14 -7\n')
#     outfile.write('xxxxxxxxxxxxxxxxxxxxxx\n')
#     outfile.write('x   x   xx xx        x\n')
#     outfile.write('x     x     xxxxxxxxxx\n')
#     outfile.write('x x   +xx  xxxx xxx xx\n')
#     outfile.write('  x   x x xx   xxxx  x\n')
#     outfile.write('x          xx +xx  x x\n')
#     outfile.write('xxxxxxx x      xx  x x\n')
#     outfile.write('xxxxxxxxx  x x  xx   x\n')
#     outfile.write('x          x x Sx x  x\n')
#     outfile.write('xxxxx x  x x x     x x\n')
#     outfile.write('xxxxxxxxxxxxxxxxxxxxxx')

#Map 2(Map ma GBFS chay khong toi uu)
with open('maze_without_reward.txt', 'w') as outfile:
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

def visualize_maze(matrix, bonus, start, end, route=None):
    """
    Args:
      1. matrix: The matrix read from the input file,
      2. bonus: The array of bonus points,
      3. start, end: The starting and ending points,
      4. route: The route from the starting point to the ending one, defined by an array of (x, y), e.g. route = [(1, 2), (1, 3), (1, 4)]
    """
    #1. Define walls and array of direction based on the route
    walls=[(i,j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j]=='x']

    if route:
        direction=[]
        for i in range(1,len(route)):
            if route[i][0]-route[i-1][0]>0:
                direction.append('v') #^
            elif route[i][0]-route[i-1][0]<0:
                direction.append('^') #v        
            elif route[i][1]-route[i-1][1]>0:
                direction.append('>')
            else:
                direction.append('<')

        direction.pop(0)

    #2. Drawing the map
    ax=plt.figure(dpi=100).add_subplot(111)

    for i in ['top','bottom','right','left']:
        ax.spines[i].set_visible(False)

    plt.scatter([i[1] for i in walls],[-i[0] for i in walls],
                marker='X',s=100,color='black')
    
    plt.scatter([i[1] for i in bonus],[-i[0] for i in bonus],
                marker='P',s=100,color='green')

    plt.scatter(start[1],-start[0],marker='*',
                s=100,color='gold')

    if route:
        for i in range(len(route)-2):
            plt.scatter(route[i+1][1],-route[i+1][0],
                        marker=direction[i],color='silver')

    plt.text(end[1],-end[0],'EXIT',color='red',horizontalalignment='center',verticalalignment='center')
    plt.xticks([])
    plt.yticks([])
    plt.show()

    print(f'Starting point (x, y) = {start[0], start[1]}')
    print(f'Ending point (x, y) = {end[0], end[1]}')
    
    for _, point in enumerate(bonus):
        print(f'Bonus point at position (x, y) = {point[0], point[1]} with point {point[2]}')

def read_file(file_name: str = 'maze.txt'):
    f=open(file_name,'r')
    n_bonus_points = int(next(f)[:-1])
    bonus_points = []
    for i in range(n_bonus_points):
        x, y, reward = map(int, next(f)[:-1].split(' '))
        bonus_points.append((x, y, reward))

    text=f.read()
    matrix=[list(i) for i in text.splitlines()]
    f.close()

    return bonus_points, matrix


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

class Node():
    def __init__(self,state,action,parent,h=0,g=0):
        self.state=state
        self.action=action
        self.parent=parent
        self.h=h
        self.g=g

#Lớp hàng đợi ưu tiên cho thuật toán A*
class PriorQueueForA():
    def __init__(self):
        self.frontier = []

    # def add(self, node):
    #     dem=0
    #     for i in range(len(self.frontier)):
    #         if node.h+node.g<=self.frontier[i].h+self.frontier[i].g:
    #             dem=i
    #             break
    #     self.frontier.insert(dem,node)
    def add(self,node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    # def remove(self):
    #     if self.empty():
    #         raise Exception("empty frontier")
    #     else:
    #         node = self.frontier[0]
    #         self.frontier = self.frontier[1:]
    #         return node
    def remove(self):
        minn = 0
        for i in range(len(self.frontier)):
            if self.frontier[i].g+self.frontier[i].h< self.frontier[minn].g+self.frontier[minn].h:
                minn = i
        item = self.frontier[minn]
        del self.frontier[minn]
        return item

#Lớp hàng đợi ưu tiên cho thuật toán GBFS
class PriorQueueForGBFS(PriorQueueForA):
    def remove(self):
        minn = 0
        for i in range(len(self.frontier)):
            if self.frontier[i].h< self.frontier[minn].h:
                minn = i
        item = self.frontier[minn]
        del self.frontier[minn]
        return item

#Lớp hàng đợi ưu tiên cho thuật toán UCS
class PriorQueueForUCS(PriorQueueForA):
    def remove(self):
        minn = 0
        for i in range(len(self.frontier)):
            if self.frontier[i].g< self.frontier[minn].g:
                minn = i
        item = self.frontier[minn]
        del self.frontier[minn]
        return item
    

#Tạo ô tường với các ô có giá trị là 'x'
def makeWall(maze):
    height=len(maze)
    width=len(maze[0])
    walls=[]
    for i in range(height):
        row=[]
        for j in range(width):
            if maze[i][j]=='x':
                row.append(True)
            else:
                row.append(False)
        walls.append(row)
    return walls

#Tính toán các node con liền kề của thuật toán A*
def neighbor(node):
    row,col =node.state
    candidates = [
        ("up", (row - 1, col)),
        ("down", (row + 1, col)),
        ("left", (row, col - 1)),
        ("right", (row, col + 1))
    ]
    res=[]
    for action, (r,c) in candidates:
        if 0<=r<height and 0<=c<width and not walls[r][c]:
            distanct=abs(end[0]-r)+abs(end[1]-c)
            temp=Node((r,c),action,node,distanct,node.g+1)
            res.append(temp)
    return res

#Tính toán các node con liền kề của thuật toán GBFS
def neighbor_for_gbfs(node):
    row,col =node.state
    candidates = [
        ("up", (row - 1, col)),
        ("down", (row + 1, col)),
        ("left", (row, col - 1)),
        ("right", (row, col + 1))
    ]
    res=[]
    for action, (r,c) in candidates:
        if 0<=r<height and 0<=c<width and not walls[r][c]:
            distanct=abs(end[0]-r)+abs(end[1]-c)
            temp=Node((r,c),action,node,distanct)
            res.append(temp)
    return res

#Tính toán các node con liền kề của thuật toán UCS
def neighbor_for_ucs(node,points):
    row,col =node.state
    candidates = [
        ("up", (row - 1, col)),
        ("down", (row + 1, col)),
        ("left", (row, col - 1)),
        ("right", (row, col + 1))
    ]
    res=[]
    for action, (r,c) in candidates:
        if 0<=r<height and 0<=c<width and not walls[r][c]:
            point_at=0
            for point in points:
                if r==point[0] and c==point[1]:
                    point_at=point[2]
            gg=node.g+1+point_at
            temp=Node((r,c),action,node,0,gg)
            res.append(temp)
    return res

#type=0 -> Greedy best first search
#type=1 -> A* search 
def solve_maze(maze,start,end,type):
    num_explored=0
    distanct=abs(end[0]-start[0])+abs(end[1]-start[1])
    start_node=Node(start,None,None,distanct,0)
    if type==0:
        fringe=PriorQueueForGBFS()
    else:
        fringe=PriorQueueForA()
    fringe.add(start_node)
    explored=set()
    while True:
        if fringe.empty():
            raise Exception("No path")
        node=fringe.remove()
        num_explored+=1
        states=[]
        actions=[]
        if node.state==end:
            while node is not None:
                states.append(node.state)
                actions.append(node.action)
                node=node.parent
            states.reverse()
            return states,num_explored
        
        explored.add(node.state)
        if type==0:
            for node_neighbor in neighbor_for_gbfs(node):
                if node_neighbor.state not in explored and not fringe.contains_state(node_neighbor.state):
                    fringe.add(node_neighbor)
        else:
            for node_neighbor in neighbor(node):
                if node_neighbor.state not in explored and not fringe.contains_state(node_neighbor.state):
                    fringe.add(node_neighbor)

def solve_maze_with_points(maze,start,end,points):
    num_explored=0
    start_node=Node(start,None,None,0,0)
    fringe=PriorQueueForUCS()
    fringe.add(start_node)
    explored=set()
    while True:
        if fringe.empty():
            raise Exception("No path")
        node=fringe.remove()
        num_explored+=1
        states=[]
        actions=[]
        if node.state==end:
            for explore in explored:
                print(explore)
            while node is not None:
                states.append(node.state)
                actions.append(node.action)
                node=node.parent
            states.reverse()
            return states,num_explored
        explored.append(node.state)
        
        for node_neighbor in neighbor_for_ucs(node,points):
            if node_neighbor.state not in explored:
                if not fringe.contains_state(node_neighbor.state):
                    fringe.add(node_neighbor)
                else:
                    for i in range(len(fringe.frontier)):
                        if node_neighbor.state==fringe.frontier[i].state and node_neighbor.g<fringe.frontier[i].g:
                            del fringe.frontier[i]
                            fringe.add(node_neighbor)
                            print (node_neighbor.state)
                            break

            


points,maze = read_file('./maze_without_reward.txt')
(start, end) = findStartAndExitPosition(maze)
walls=makeWall(maze)
height=len(maze)
width=len(maze[0])

#type=0 -> Greedy best first search
#states,num_explored=solve_maze(maze,start,end,0)

#type=1 -> A* search 
states,num_explored=solve_maze(maze,start,end,1)

#states,num_explored=solve_maze_with_points(maze,start,end,points)

#print(states)
visualize_maze(maze,points,start,end,states)
print(f'Chi phi cua duong di den dich: {len(states)}')
print(f'So cac trang thai da xet: {num_explored}')
