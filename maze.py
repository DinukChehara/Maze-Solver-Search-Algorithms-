import sys
import time

if len(sys.argv) < 3:
    print(
    "Usage:\n"
    "  python maze.py <maze_file> <algorithm> [options]\n\n"
    "Arguments:\n"
    "  <maze_file>     Path to the maze input file\n"
    "  <algorithm>     One of: DFS | BFS | A*\n"
    "  [options]       Optional flags: show_info | show_frontier | show_image\n"
    )

    input("You have to run this via a terminal")
    sys.exit(1)

filename = sys.argv[1]
algorithm = sys.argv[2].upper()
display_maze = False
showInfo = False
showImage = False
showFrontier = False

for arg in sys.argv:
    if arg == "show_info":
        showInfo = True
    
    if arg == "show_image":
        showImage = True
    
    if arg == "show_frontier":
        showFrontier = True

    if arg == "display_maze":
        display_maze = True

print(filename)
print(algorithm)

if algorithm not in ["DFS", "BFS", "A*"]:
    print("Invlaid algorithm. Algorithms: DFS, BFS, A*")
    sys.exit(1)

class Node:
    def __init__(self,state, parent, action, posX, posY, is_goal, goalX = None, goalY = None, step = None):
        self.state = state
        self.parent = parent
        self.action = action
        self.posX = posX
        self.posY = posY
        self.is_goal = is_goal
        self.step = step
        self.manhattan_distance = None
        self.cost = None
        if goalY != None and goalX != None and step != None:
            self.manhattan_distance = abs(goalX - posX) + abs(goalY - posY)
            self.cost = self.manhattan_distance + step
    
    def __repr__(self):
        return f"Node(action={self.action}, pos=({self.posX}, {self.posY}), goal={self.is_goal}, step={self.step}, manhattan_distance={self.manhattan_distance}, cost={self.cost})"

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def hasNode(self, node):
        return node in self.frontier
    
    def empty(self):
        return len(self.frontier) == 0
    
    def removeNode(self, node):
        self.frontier.remove(node)
        return node

    def remove(self):
        node = self.frontier[-1]
        self.frontier.pop(-1)
        return node

class QueueFrontier(StackFrontier):
    def __init__(self):
        super().__init__()
    def remove(self):
        node = self.frontier[0]
        self.frontier.pop(0)
        return node

class DepthFirstSearch():
    def __init__(self):
        self.frontier = StackFrontier()
        self.explored = []
        self.actions = []

    def solve(self, file):
        startTime = time.time()
        state = file.readlines()
        state = [line.strip("\n") for line in state]
    
        startX = 0
        startY = 0

        for row in state:
            try: startX = row.index("A")
            except: continue
            if startX == None:
                raise "Start position not found"
            startY = state.index(row)
            break

        """
        1. check if empty -> no sols
        2. remove a node
        3. check if node is goal -> solved
        4. add children nodes to frontier
        """

        startNode = Node(state, None, None, startX, startY, False)
        self.frontier.add(startNode)
        posX = startX
        posY = startY

        iterations = 0
        while True:
            if showFrontier:
                print("frontier: ", self.frontier.frontier)
            if showInfo:
                print(f"iterations: {iterations}")
                print(f"currentPos:{posX, posY}")
            if display_maze:
                print("\nstate:")
                [print(line) for line in state] 
                print("\n"*4)

            # checks if the frontier is empty
            if self.frontier.empty():
                [print(line) for line in state] 
                print("no solution")
                return state
            
            # remove a node
            node = self.frontier.remove()

            if node in self.explored:
                continue

            state = node.state
            posX = node.posX
            posY = node.posY

            # checks if the node is the goal
            if node.is_goal:
                [print(line) for line in state] 
                print(f"Solved in {'{:.3f}'.format((time.time()-startTime) * 1000)}ms / {iterations} iterations")
                return state

            self.explored.append(node)

            up = None
            down = None
            left = None
            right = None
            
            if node.posY > 0:
                up = state[node.posY - 1][node.posX]
                if up == "B":
                    up = "goal"
                    
                elif up != " ":
                    up = None
            
            if node.posY < len(state)-1:
                down = state[node.posY + 1][node.posX]
                if down == "B":
                    down = "goal"
                elif down != " ":
                    down = None
            
            if node.posX < len(state[node.posY]) -1:
                right = state[node.posY][node.posX + 1]
                if right == "B":
                    right = "goal"
                elif right != " ":
                    right = None
            
            if node.posX > 0:
                left = state[node.posY][node.posX - 1]
                if left == "B":
                    left = "goal"
                elif left != " ":
                    left = None

            # adding the child nodes to the frontier
            if up is not None:
                new_state = state.copy()
                is_goal = up == "goal"
                if up == " ":
                    new_state[node.posY - 1] = new_state[node.posY - 1][:node.posX] + "*" + new_state[node.posY - 1][node.posX + 1:]

                self.frontier.add(Node(new_state, node, "up", node.posX, node.posY - 1, is_goal))

            if down is not None:
                new_state = state.copy()
                is_goal = down == "goal"
                if down == " ":
                    new_state[node.posY + 1] = new_state[node.posY + 1][:node.posX] + "*" + new_state[node.posY + 1][node.posX + 1:]

                self.frontier.add(Node(new_state, node, "down", node.posX, node.posY + 1, is_goal))

            if left is not None:
                new_state = state.copy()
                is_goal = left == "goal"
                if left == " ":
                    new_state[node.posY] = new_state[node.posY][:node.posX - 1] + "*" + new_state[node.posY][node.posX:]
                self.frontier.add(Node(new_state, node, "left", node.posX - 1, node.posY, is_goal))

            if right is not None:
                new_state = state.copy()
                is_goal = right == "goal"
                if right == " ":
                    new_state[node.posY] = new_state[node.posY][:node.posX + 1] + "*" + new_state[node.posY][node.posX + 2:]
                self.frontier.add(Node(new_state, node, "right", node.posX + 1, node.posY, is_goal))
            
            self.actions.append(node.action)
            iterations+=1

class BreadthFirstSearch(DepthFirstSearch):
    def __init__(self):
        super().__init__()
        self.frontier = QueueFrontier()


class AStarSearch:
    def __init__(self):
        self.frontier = StackFrontier()
        self.explored = []
        self.actions = []
    
    def solve(self, file):
        startTime = time.time()
        
        state = file.readlines()
        state = [line.strip('\n') for line in state]
        
        startX = 0
        startY = 0
        goalX = 0
        goalY = 0

        for row in state:
            try: 
                startX = row.index("A") 
            except: continue
            if startX == None:
                raise "Start position not found"
            startY = state.index(row)
            break
        
        for row in state:
            try:
                goalX = row.index("B")
            except: continue
            if goalX == None:
                raise "Goal position not found"
            goalY = state.index(row)
            break
        

        startNode = Node(state, None, None,startX, startY, False, goalX, goalY, 0)
        self.frontier.add(startNode)
        posX = startX
        posY = startY

        """ 
        check if frontier is empty
        remove a node
        check if node = goal
        check if fronteir has any node with low cost -> remove that node
        add child nodes to frontier 
        """
        
        iterations = 0
        while True:
            if showFrontier:
                print("frontier: ", self.frontier.frontier)
            if showInfo:
                print(f"iterations: {iterations}")
                print(f"currentPos:{posX, posY}")
                print(f"goalPos:{goalX, goalY}")
            if display_maze:
                print("\nstate:")
                [print(line) for line in state] 
                print("\n"*4)
            
            # check if frontier is empty
            if len(self.frontier.frontier) == 0:
                [print(line) for line in state] 
                print("no solutions")
                return state
            
            costs = {}
            # add costs of nodes in frontier
            for n in self.frontier.frontier:
                if n.cost!=None:
                    costs[n.cost] = n
            
            # remove a node 
            node = self.frontier.removeNode(costs.get(min(costs.keys())))
            if node in self.explored:
                continue

            self.explored.append(node)
            self.addChildNodes(node, goalX, goalY)

            state = node.state
            cost = node.cost
            posX = node.posX
            posY = node.posY

            # check if node is the goal
            if node.is_goal:
                [print(line) for line in state] 
                print(f"Solved in {'{:.3f}'.format((time.time()-startTime) * 1000)}ms / {iterations} iterations")
                return state
            
            iterations+=1

    def addChildNodes(self, node, goalX, goalY):
            state = node.state

            up = None
            down = None
            left = None
            right = None
            
            if node.posY > 0:
                up = state[node.posY - 1][node.posX]
                if up == "B":
                    up = "goal"
                    
                elif up != " ":
                    up = None
            
            if node.posY < len(state)-1:
                down = state[node.posY + 1][node.posX]
                if down == "B":
                    down = "goal"
                elif down != " ":
                    down = None
            
            if node.posX < len(state[node.posY]) -1:
                right = state[node.posY][node.posX + 1]
                if right == "B":
                    right = "goal"
                elif right != " ":
                    right = None
            
            if node.posX > 0:
                left = state[node.posY][node.posX - 1]
                if left == "B":
                    left = "goal"
                elif left != " ":
                    left = None

            # adding the child nodes to the frontier
            if up is not None:
                new_state = state.copy()
                is_goal = up == "goal"
                if up == " ":
                    new_state[node.posY - 1] = new_state[node.posY - 1][:node.posX] + "*" + new_state[node.posY - 1][node.posX + 1:]
                
                parentStep = node.step if node.step != None else 0
                self.frontier.add(Node(new_state, node, "up", node.posX, node.posY - 1, is_goal, goalX, goalY, parentStep + 1))

            if down is not None:
                new_state = state.copy()
                is_goal = down == "goal"
                if down == " ":
                    new_state[node.posY + 1] = new_state[node.posY + 1][:node.posX] + "*" + new_state[node.posY + 1][node.posX + 1:]

                parentStep = node.step if node.step != None else 0
                self.frontier.add(Node(new_state, node, "down", node.posX, node.posY + 1, is_goal, goalX, goalY, parentStep+1))

            if left is not None:
                new_state = state.copy()
                is_goal = left == "goal"
                if left == " ":
                    new_state[node.posY] = new_state[node.posY][:node.posX - 1] + "*" + new_state[node.posY][node.posX:]
                    
                parentStep = node.step if node.step != None else 0
                self.frontier.add(Node(new_state, node, "left", node.posX - 1, node.posY, is_goal, goalX, goalY, parentStep+1))

            if right is not None:
                new_state = state.copy()
                is_goal = right == "goal"
                if right == " ":
                    new_state[node.posY] = new_state[node.posY][:node.posX + 1] + "*" + new_state[node.posY][node.posX + 2:]
                    
                parentStep = node.step if node.step != None else 0
                self.frontier.add(Node(new_state, node, "right", node.posX + 1, node.posY, is_goal, goalX, goalY, parentStep+1))


# made by chatgpt i dont wanna learn this shi
def visualize_maze(maze, explored):
    try:
        import matplotlib.pyplot as plt
        import matplotlib.colors as mcolors
        import numpy as np
    
        cols = max(len(row) for row in maze)
        rows = len(maze)

        # Pad rows with spaces
        maze = [row.ljust(cols) for row in maze]

        # Find start ('A') and goal ('B')
        start = None
        goal = None
        for y, row in enumerate(maze):
            for x, char in enumerate(row):
                if char == 'A':
                    start = (x, y)
                elif char == 'B':
                    goal = (x, y)

        # Build path from '*' characters in maze
        path = []
        for y, row in enumerate(maze):
            for x, char in enumerate(row):
                if char == '*':
                    node = type('Node', (), {})()
                    node.posX = x
                    node.posY = y
                    path.append(node)
        
        # Base grid: unexplored = gray (2), wall = black (0)
        grid = np.zeros((rows, cols))
        for y in range(rows):
            for x in range(cols):
                char = maze[y][x]
                if char == '#':
                    grid[y][x] = 0  # wall
                else:
                    grid[y][x] = 2  # unexplored

        # Mark explored = yellow (3)
        for node in explored:
            grid[node.posY][node.posX] = 3
        
        # Mark path = green (4)
        for node in path:
            grid[node.posY][node.posX] = 4

        # Mark start = blue (5), goal = red (6)
        if start:
            grid[start[1]][start[0]] = 5
        if goal:
            grid[goal[1]][goal[0]] = 6

        # Colormap
        cmap = mcolors.ListedColormap(["black", "white", "gray", "yellow", "green", "blue", "red"])
        bounds = [0, 1, 2, 3, 4, 5, 6, 7]
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        # Plot
        fig, ax = plt.subplots(figsize=(cols/2, rows/2))  # make bigger
        im = ax.imshow(grid, cmap=cmap, norm=norm, origin='upper')

        # Add small gaps between blocks
        ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
        ax.grid(which='minor', color='black', linestyle='-', linewidth=1)

        ax.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False)
        plt.show()
    except:
        print("matplotlib not found, couldn't generate image")


def main():
    try:
        file = open(filename, "r")
    except:
        print(f"File '{filename}' not found")
        sys.exit(1)

    frontier = DepthFirstSearch()
    if algorithm == "DFS":
        pass
    elif algorithm == "BFS":
        frontier = BreadthFirstSearch()
    elif algorithm == "A*":
        frontier = AStarSearch()

    print(" "*100)
    state = frontier.solve(file)
    file.close()
    if showImage:
        visualize_maze(state, frontier.explored)

if __name__ == "__main__":
    main()