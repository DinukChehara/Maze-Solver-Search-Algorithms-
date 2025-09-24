class Node:
    def __init__(self,state, parent, action, posX, posY):
        self.state = state
        self.parent = parent
        self.action = action
        self.posX = posX
        self.posY = posY

    def __str__(self):
        return f"parent: {self.parent} action: {self.action}"
    
    def __repr__(self):
        return f"Node(action={self.action}, pos={self.posX}, {self.posY})"
    
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

        startNode = Node(state, None, None, startX, startY)
        self.add(startNode)

        iterations = 0
        while True:
            print(f"iteration: {iterations}")
            print(self.frontier)
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
            if node.action == "goal":
                print("solved")
                print(f"iteration: {iterations}")
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
                action = "goal"
                if up == " ":
                    new_state[node.posY - 1] = new_state[node.posY - 1][:node.posX] + "*" + new_state[node.posY - 1][node.posX + 1:]
                    action = "up"

                self.add(Node(new_state, node, action, node.posX, node.posY - 1))

            if down is not None:
                new_state = state.copy()
                action = "goal"
                if down == " ":
                    new_state[node.posY + 1] = new_state[node.posY + 1][:node.posX] + "*" + new_state[node.posY + 1][node.posX + 1:]
                    action = "down"

                self.add(Node(new_state, node, action, node.posX, node.posY + 1))

            if left is not None:
                new_state = state.copy()
                action = "goal"
                if left == " ":
                    new_state[node.posY] = new_state[node.posY][:node.posX - 1] + "*" + new_state[node.posY][node.posX:]
                    action = "left"
                self.add(Node(new_state, node, action, node.posX - 1, node.posY))

            if right is not None:
                new_state = state.copy()
                action = "goal"
                if right == " ":
                    new_state[node.posY] = new_state[node.posY][:node.posX + 1] + "*" + new_state[node.posY][node.posX + 2:]
                    action = "right"
                self.add(Node(new_state, node, action, node.posX + 1, node.posY))
            
            iterations+=1


        return state

class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty")
        node = self.frontier[0]
        self.frontier.pop(0)
        return node

            
file = open("maze1.txt", "r")
frontier = StackFrontier()
print(" "*100)
state = frontier.solve(file)
input()