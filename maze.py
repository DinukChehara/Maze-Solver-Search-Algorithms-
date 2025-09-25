import sys
import PIL
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

if len(sys.argv) != 3:
    print("Usage: python maze.py <file> <algorithm: DFS | BFS>")
    sys.exit(1)

filename = sys.argv[1]
algorithm = sys.argv[2].upper()
print(filename)
print(algorithm)

if algorithm not in ["DFS", "BFS"]:
    print("Invlaid algorithm. Algorithms: DFS, BFS")
    sys.exit(1)

class Node:
    def __init__(self,state, parent, action, posX, posY, is_goal):
        self.state = state
        self.parent = parent
        self.action = action
        self.posX = posX
        self.posY = posY
        self.is_goal = is_goal

    def __str__(self):
        return f"parent: {self.parent} action: {self.action}"
    
    def __repr__(self):
        return f"Node(action={self.action}, pos=({self.posX}, {self.posY}), goal={self.is_goal})"
    
class StackFrontier:
    def __init__(self):
        self.frontier = []
        self.explored = []
        self.actions = []

    def add(self, node):
        self.frontier.append(node)
    
    def hasNode(self, node):
        return node in self.frontier
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty")
        node = self.frontier[-1]
        self.frontier.pop(-1)
        return node

    def solve(self, file):
        state = file.readlines()
        state = [line.strip("\n") for line in state]
    
        startX = 0
        startY = 0

        for row in state:
            try: startX = row.index("A")
            except: continue
            if startX == None:
                raise "Start position now found"
            startY = state.index(row)
            break

        """
        1. check if empty -> no sols
        2. remove a node
        3. check if node is goal -> solved
        4. add children nodes to frontier
        """

        startNode = Node(state, None, None, startX, startY, False)
        self.add(startNode)

        iterations = 0
        while True:
            print(f"iteration: {iterations}")
            print("frontier: ", self.frontier)
            print("\nstate:")
            [print(line) for line in state] 
            print("\n"*4)

            # checks if the frontier is empty
            if self.empty():
                print("no solution")
                break
            
            # remove a node
            node = self.remove()
            state = node.state

            # checks if the node is the goal
            if node.is_goal:
                print("solved")
                print(f"iteration: {iterations}")
                print("\nstate:")
                [print(line) for line in state] 
                break
            
            self.explored.append(node)

            up = None
            down = None
            left = None
            right = None
            
            try:
                up = state[node.posY - 1][node.posX]
                if up == "B":
                    up = "goal"
                    
                elif up != " ":
                    up = None
            except:pass
            
            try:
                down = state[node.posY + 1][node.posX]
                if down == "B":
                    down = "goal"
                elif down != " ":
                    down = None
            except:pass
            
            try:
                right = state[node.posY][node.posX + 1]
                if right == "B":
                    right = "goal"
                elif right != " ":
                    right = None
            except:pass
            
            try: 
                left = state[node.posY][node.posX - 1]
                if left == "B":
                    left = "goal"
                elif left != " ":
                    left = None
            except: pass

            # adding the child nodes to the frontier
            if up is not None:
                new_state = state.copy()
                is_goal = up == "goal"
                if up == " ":
                    new_state[node.posY - 1] = new_state[node.posY - 1][:node.posX] + "*" + new_state[node.posY - 1][node.posX + 1:]

                self.add(Node(new_state, node, "up", node.posX, node.posY - 1, is_goal))

            if down is not None:
                new_state = state.copy()
                is_goal = down == "goal"
                if down == " ":
                    new_state[node.posY + 1] = new_state[node.posY + 1][:node.posX] + "*" + new_state[node.posY + 1][node.posX + 1:]

                self.add(Node(new_state, node, "down", node.posX, node.posY + 1, is_goal))

            if left is not None:
                new_state = state.copy()
                is_goal = left == "goal"
                if left == " ":
                    new_state[node.posY] = new_state[node.posY][:node.posX - 1] + "*" + new_state[node.posY][node.posX:]
                self.add(Node(new_state, node, "left", node.posX - 1, node.posY, is_goal))

            if right is not None:
                new_state = state.copy()
                is_goal = right == "goal"
                if right == " ":
                    new_state[node.posY] = new_state[node.posY][:node.posX + 1] + "*" + new_state[node.posY][node.posX + 2:]
                self.add(Node(new_state, node, "right", node.posX + 1, node.posY, is_goal))
            
            iterations+=1


        return state

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty")
        node = self.frontier[0]
        self.frontier.pop(0)
        return node

def visualize_maze(maze, explored):
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


def main():
    try:
        file = open(filename, "r")
    except:
        print(f"File '{filename}' not found")
        sys.exit(1)

    frontier = StackFrontier()
    if sys.argv[2] == "BFS":
        frontier = QueueFrontier()

    print(" "*100)
    state = frontier.solve(file)
    file.close()
    visualize_maze(state, frontier.explored)

if __name__ == "__main__":
    main()