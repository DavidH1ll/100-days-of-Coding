from collections import deque

class Node:
    def __init__(self, key):
        self.data = key
        self.left = None
        self.right = None

def printLevelOrder(root):
    if root is None:
        return

    nodes = deque([root])
    while(len(nodes) > 0):
        currLevel = []
        for _ in range(len(nodes)):
            curr = nodes.popleft()
            currLevel.append(curr.data)

            if curr.left is not None:
                nodes.append(curr.left)

            if curr.right is not None:
                nodes.append(curr.right)

        print(' '.join(map(str, currLevel)))


root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)
root.right.right = Node(6)

printLevelOrder(root)