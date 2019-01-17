'''
        BSP Test
    Test file for binary
    space partitioning
'''
class BinaryTree:
    def __init__(self, node=None):
        self.root = node
    def setRootNode(self, node):
        self.root = node
    def getRootNode(self):
        return self.root

# Need to decide what attributes the node object should have
class Node:
    # Idk if parsing in the parent node is necessary
    def __init__(self, val, leftChild=None, rightChild=None, parent=None):
        self.val = val
        self.leftChild = leftChild
        self.rightChild = rightChild
        self.parentNode = parent

    def setleftChild(self, node):
        self.leftChild = node

    def setrightChild(self, node):
        self.rightChild = node

    def setParent(self, node):
        self.parentNode = node

    def getleftChild(self):
        try:
            return self.leftChild
        except AttributeError:
            return None

    def getrightChild(self):
        try:
            return self.rightChild
        except AttributeError:
            return None

    def getParent(self):
        return self.parentNode

#Traversals that print the value, doesn't store anything, idk why I added them
def inOrder(root):
    if root:
        # First recur on leftChild child
        inOrder(root.getleftChild())
        # then print the data of node
        print(root.val)
        # now recur on rightChild child
        inOrder(root.getrightChild())

# A function to do postorder tree traversal
def postOrder(root):
    if root:
        # First recur on leftChild child
        postOrder(root.getleftChild())
        # the recur on rightChild child
        postOrder(root.getrightChild())
        # now print the data of node
        print(root.val)

# A function to do preorder tree traversal
def preOrder(root):
    if root:
        # First print the data of node
        print(root.val)
        # Then recur on leftChild child
        preOrder(root.getleftChild())
        # Finally recur on rightChild child
        preOrder(root.getrightChild())
def testTree():
    '''
      A
     / \
    B   C
         \
          D
    '''
    A = Node('A')
    B = Node('B')
    C = Node('C')
    D = Node('D')
    A.setleftChild(B)
    A.setrightChild(C)
    C.setrightChild(D)
    bt = BinaryTree(A)
    print(bt)
    inOrder(bt.getRootNode())

def produce2DArray(M: int, N: int):
    return [[0]*10 for i in range(10)]
produce2DArray(10, 10)