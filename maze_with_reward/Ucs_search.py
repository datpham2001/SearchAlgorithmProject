from create_and_visualize import *
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
            path_cost=node.g
            while node is not None:
                states.append(node.state)
                actions.append(node.action)
                node=node.parent
            states.reverse()
            return states,num_explored,path_cost
        explored.add(node.state)
        
        for node_neighbor in neighbor_for_ucs(node,points):
            if node_neighbor.state not in explored:
                if not fringe.contains_state(node_neighbor.state):
                    fringe.add(node_neighbor)
                else:
                    for i in range(len(fringe.frontier)):
                        if node_neighbor.state==fringe.frontier[i].state and node_neighbor.g<fringe.frontier[i].g:
                            del fringe.frontier[i]
                            fringe.add(node_neighbor)
                            break


points,maze = readFile('./maze_with_reward3.txt')
(start, end) = findStartAndExitPosition(maze)
walls=makeWall(maze)
height=len(maze)
width=len(maze[0])

states,num_explored,path_cost=solve_maze_with_points(maze,start,end,points)
visualize_maze(maze,points,start,end,states)
print(f'Chi phi cua duong di den dich: {path_cost}')
print(f'So cac trang thai da xet: {num_explored}')