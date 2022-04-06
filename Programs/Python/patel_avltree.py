"""
# CISC 233 LAB 3 Self-Balancing Binary Search Trees
# Author        : Umangkumar Patel
# Date Created  : April 4, 2022,
# Date Modified : April 5, 2022,
# Instructor    : Professor Eugene
# Description   : Perform a series of empirical tests on two different self-balancing search tree implementations,
#                 counting the number of comparisons and rotations used when adding elements.
# GitHub        : https://github.com/ukpatell/Python.git
# Sources       : https://github.com/davidtweinberger/avl_tree/blob/master/tree.py
                  https://github.com/sphinxyun/algorithm-in-python/blob/b69b5641d0457f5dcfe824755d9c302340980114/dataStructure/redBlackTree.py
# Important Note:
#                 This file contains (modified) implementation from "patel_bst_balancing.py" OR lab1 task in order to compare the rotation
#                 counts between AVL Tree and Red-Black Tree. It displays on 32 SIZE tree as per requirement from Lab Task #2
"""
import random
from functools import total_ordering
from colorama import init, Fore, Back, Style

# Initializes Colorama
init(autoreset=True)

# Color Prefix
pref = "\033["
reset = f'{pref}0m'
red = "31m"

SIZE = [32, 256, 1024, 2048]

# Rotate Counts based independently
COUNTER = 0  # AVL Counter
R_COUNTER = 0  # Red Tree Counter
ROTATE = [0, 0, 0, 0]  # AVL Rotator
R_ROTATE = [0, 0, 0, 0]  # Red Tree Rotator

"""
Red Tree Implementation
"""


@total_ordering
class node:
    def __init__(self, val, left=None, right=None, isBlack=False):
        self.val = val
        self.left = left
        self.right = right
        self.parent = None
        self.isBlack = isBlack

    def __lt__(self, nd):
        return self.val < nd.val

    def __eq__(self, nd):
        return nd is not None and self.val == nd.val

    def setChild(self, nd, isLeft):
        if isLeft:
            self.left = nd
        else:
            self.right = nd
        if nd is not None: nd.parent = self

    def getChild(self, isLeft):
        if isLeft:
            return self.left
        else:
            return self.right

    def __bool__(self):
        return self.val is not None

    def __str__(self):
        val = '-' if self.parent is None else self.parent.val
        color = 'B' if self.isBlack else 'R'
        if color == 'R':
            return f'{pref}{red}{color}-{self.val}' + reset
        return f'{color}-{self.val}'

    def __repr__(self):
        return f'node({self.val},isBlack={self.isBlack})'


def get_height(root):
    # Check if the binary tree is empty
    if root is None:
        # If TRUE return 0
        return 0
        # Recursively call height of each node
    leftAns = get_height(root.left)
    rightAns = get_height(root.right)

    # Return max(leftHeight, rightHeight) at each iteration
    return max(leftAns, rightAns) + 1


def inorder(root):
    if not root:
        return

    inorder(root.left)
    print(root.val, end=" ")
    inorder(root.right)


class redBlackTree:
    def __init__(self, unique=False):
        '''if unique is True, all node'vals are unique, else there may be equal vals'''
        self.root = None
        self.unique = unique

    @staticmethod
    def checkBlack(nd):
        return nd is None or nd.isBlack

    @staticmethod
    def setBlack(nd, isBlack):
        if nd is not None:
            if isBlack is None or isBlack:
                nd.isBlack = True
            else:
                nd.isBlack = False

    def setRoot(self, nd):
        if nd is not None: nd.parent = None
        self.root = nd

    def find(self, val):
        nd = self.root
        while nd:
            if nd.val == val:
                return nd
            else:
                nd = nd.getChild(nd.val > val)

    def rotate(self, prt, chd):
        '''rotate prt with the center of chd'''
        counter(r=1)
        if self.root is prt:
            self.setRoot(chd)
        else:
            prt.parent.setChild(chd, prt.parent.left is prt)
        isLeftChd = prt.left is chd
        prt.setChild(chd.getChild(not isLeftChd), isLeftChd)
        chd.setChild(prt, not isLeftChd)

    def insert(self, nd):
        if nd.isBlack: nd.isBlack = False

        if self.root is None:
            self.setRoot(nd)
            self.root.isBlack = True
        else:
            parent = self.root
            while parent:
                if parent == nd: return None
                isLeft = parent > nd
                chd = parent.getChild(isLeft)
                if chd is None:
                    parent.setChild(nd, isLeft)
                    break
                else:
                    parent = chd
            self.fixUpInsert(parent, nd)

    def fixUpInsert(self, parent, nd):
        ''' adjust color and level,  there are two red nodes: the new one and its parent'''
        while not self.checkBlack(parent):
            grand = parent.parent
            isLeftPrt = grand.left is parent
            uncle = grand.getChild(not isLeftPrt)
            if not self.checkBlack(uncle):
                # case 1:  new node's uncle is red
                self.setBlack(grand, False)
                self.setBlack(grand.left, True)
                self.setBlack(grand.right, True)
                nd = grand
                parent = nd.parent
            else:
                # case 2: new node's uncle is black(including nil leaf)
                isLeftNode = parent.left is nd
                if isLeftNode ^ isLeftPrt:
                    # case 2.1 the new node is inserted in left-right or right-left form
                    #         grand               grand
                    #     parent        or            parent
                    #          nd                   nd
                    self.rotate(parent, nd)  # parent rotate
                    nd, parent = parent, nd
                # case 3  (case 2.2) the new node is inserted in left-left or right-right form
                #         grand               grand
                #      parent        or            parent
                #     nd                                nd

                self.setBlack(grand, False)
                self.setBlack(parent, True)
                self.rotate(grand, parent)
        self.setBlack(self.root, True)

    def display(self):
        def getHeight(nd):
            if nd is None:
                return 0
            return max(getHeight(nd.left), getHeight(nd.right)) + 1

        def levelVisit(root):
            from collections import deque
            lst = deque([root])
            level = []
            h = getHeight(root)
            ct = lv = 0
            while 1:
                ct += 1
                nd = lst.popleft()
                if ct >= 2 ** lv:
                    lv += 1
                    if lv > h: break
                    level.append([])
                level[-1].append(str(nd))
                if nd is not None:
                    lst += [nd.left, nd.right]
                else:
                    lst += [None, None]
            return level

        def addBlank(lines):
            width = 1 + len(str(self.root))
            sep = ' ' * width
            n = len(lines)
            for i, oneline in enumerate(lines):
                k = 2 ** (n - i) - 1
                new = [sep * ((k - 1) // 2)]
                for s in oneline:
                    new.append(s.ljust(width))
                    new.append(sep * k)
                lines[i] = new
            return lines

        lines = levelVisit(self.root)
        lines = addBlank(lines)
        li = [''.join(line) for line in lines]
        length = 10 if li == [] else max(len(i) for i in li) // 2
        begin = '\n' + 'red-black-tree'.rjust(length + 14, '-') + '-' * length
        end = '-' * (length * 2 + 14) + '\n'
        return '\n'.join([begin, *li, end])

    def __str__(self):
        return self.display()


# Builds the tree (Function) : Defaults to print, unless specified
def buildTree(nums, visitor=None, y=1, x=0, order=0):
    global R_COUNTER
    rbtree = redBlackTree()
    for i in nums:
        rbtree.insert(node(i))
        if x == 1: print(rbtree)  # Enable to print each step
        # print(rbtree)
        if visitor:
            visitor(rbtree, i)

    if y == 1: print(rbtree)  # Only prints the final resultant R-B tree
    if order == 1:
        print('In-Order Traversal         : ')
        print(inorder(rbtree.root), '\n')  # Only prints in-order traversal if enabled

    R_COUNTER += 1
    return rbtree, nums


"""
AVL Tree Implementation
"""


class AVL_tree:
    # Inner node class
    class AVL_node:
        """
        Node class to be used in the tree.
        Each node has a balance factor attribute representing
        the longest downward path rooted at the node.
        """

        def __init__(self, data=None, left=None, right=None, balance=0, parent=None):
            self.data = data
            self.left = left
            self.right = right
            self.parent = parent

            # used to balance the tree: balance = height(left subtree) - height(right subtree)
            # tree at node is balanced if the value is in [-1, 0, 1], else it is unbalanced
            self.balance = balance
            return

    def __init__(self):
        self._root = None
        self._depth = None
        self._max_chars = None
        return

    def __str__(self):
        """
        Traverses and prints the binary tree in an organized and pretty way.
        Uses a BFS (level-order) traversal.
        """
        self.synchronizeFields()
        if self._depth == 0:
            return ""
        s = ""
        queue = []
        level = 0
        queue.append((1, self._root))
        while len(queue):
            nodelev, node = queue.pop(0)
            if (not node):
                if (self._depth - nodelev + 1) <= 0:
                    continue
                if nodelev != level:
                    s += "\n"
                    s += " " * int(self._max_chars * (2 ** (self._depth - nodelev) - 1))
                    level = nodelev
                s += " " * self._max_chars * (2 ** (self._depth - nodelev + 1) - 1)
                s += " " * self._max_chars
                queue.append((nodelev + 1, None))
                queue.append((nodelev + 1, None))
                continue
            if nodelev != level:
                s += "\n"
                s += " " * self._max_chars * (2 ** (self._depth - nodelev) - 1)
                level = nodelev
            for i in range(int(self._max_chars - len(str(node.data)))):
                s += " "
            s += str(node.data)
            s += " " * self._max_chars * (2 ** (self._depth - nodelev + 1) - 1)
            if node.left:
                queue.append((nodelev + 1, node.left))
            else:
                queue.append((nodelev + 1, None))
            if node.right:
                queue.append((nodelev + 1, node.right))
            else:
                queue.append((nodelev + 1, None))
        s += "\n\n"
        return s

    def synchronizeFields(self):
        """
        Calculates depth and max_chars of the tree
        """
        if not self.getRoot():
            self._depth = 0
            self._max_chars = 1
            return
        self._depth = 0
        self._max_chars = 1
        Q = []
        Q.append((self.getRoot(), 1, len(str(self.getRoot().data))))
        while len(Q):
            node, depth, chars = Q.pop(0)
            self._depth = max(self._depth, depth)
            self._max_chars = max(self._max_chars, chars)
            if node.left:
                Q.append((node.left, depth + 1, len(str(node.left.data))))
            if node.right:
                Q.append((node.right, depth + 1, len(str(node.right.data))))
        return

    def getRoot(self):
        return self._root

    def setRoot(self, node):
        self._root = node

    def contains(self, data):
        """
        External method used to search the tree for a data element.
        """
        return True if self.recursiveContains(data, self.getRoot()) else False

    def recursiveContains(self, data, node):
        """
        Internal method used to recursively search for data elements
        """
        if not node:
            return None
        elif node.data == data:
            return node
        elif data > node.data:
            return self.recursiveContains(data, node.right)
        elif data < node.data:
            return self.recursiveContains(data, node.right)

    def insertList(self, l):
        """
        Builds the tree by inserting elements from a list in order.
        """
        global COUNTER
        if l is None:
            return
        try:
            for ele in l:
                self.insert(ele)
        except TypeError:
            return

        COUNTER += 1
        return

    def insert(self, data):
        """
        This is the external insert method for the data structure.
        Args:
            data: a data object to be inserted into the tree
        """
        if data is None:
            return
        if not self.getRoot():
            self.setRoot(AVL_tree.AVL_node(data=data))
            return
        else:
            self._done = 0
            self.recursiveInsert(self.getRoot(), data)
            delattr(self, "_done")
            return

    def recursiveInsert(self, node, data):
        # This is an internal method used to insert data elements
        # recursively into the tree.

        # no duplicates in the tree
        if data == node.data:
            return

        if data < node.data:
            if node.left:
                self.recursiveInsert(node.left, data)
            else:
                node.left = AVL_tree.AVL_node(data=data, parent=node)
                self.updateBalance(node.left)
        else:
            if node.right:
                self.recursiveInsert(node.right, data)
            else:
                node.right = AVL_tree.AVL_node(data=data, parent=node)
                self.updateBalance(node.right)
        return

    def updateBalance(self, node):
        # Balances the tree starting with a newly inserted node (node)
        if node.balance > 1 or node.balance < -1:
            self.rebalance(node)
            return
        if node.parent:
            if node.parent.left is node:  # lchild
                node.parent.balance += 1
            elif node.parent.right is node:  # rchild
                node.parent.balance -= 1

            # recurse to the parent
            if node.parent.balance != 0:
                self.updateBalance(node.parent)

    def rotateLeft(self, node):
        # Performs a left rotation.
        # print("rotating left around: " + str(node.data))
        counter()
        newRootNode = node.right
        node.right = newRootNode.left
        if (newRootNode.left):
            newRootNode.left.parent = node
        newRootNode.parent = node.parent
        if node is self.getRoot():
            self.setRoot(newRootNode)
        else:
            if node.parent.left is node:
                node.parent.left = newRootNode
            else:
                node.parent.right = newRootNode
        newRootNode.left = node
        node.parent = newRootNode
        node.balance = node.balance + 1 - min(newRootNode.balance, 0)
        newRootNode.balance = newRootNode.balance + 1 + max(node.balance, 0)

    def rotateRight(self, node):
        # Performs a right rotation.
        # print("rotating right around: " + str(node.data))
        counter()
        newRootNode = node.left
        node.left = newRootNode.right
        if (newRootNode.right):
            newRootNode.right.parent = node
        newRootNode.parent = node.parent
        if node is self.getRoot():
            self.setRoot(newRootNode)
        else:
            if node.parent.right is node:
                node.parent.right = newRootNode
            else:
                node.parent.left = newRootNode
        newRootNode.right = node
        node.parent = newRootNode
        node.balance = node.balance - 1 - max(newRootNode.balance, 0)
        newRootNode.balance = newRootNode.balance - 1 + min(node.balance, 0)

    def rebalance(self, node):
        # Performs the tree rotations to rebalance the tree.
        if node.balance < 0:
            if node.right.balance > 0:
                self.rotateRight(node.right)
                self.rotateLeft(node)
            else:
                self.rotateLeft(node)
        elif node.balance > 0:
            if node.left.balance < 0:
                self.rotateLeft(node.left)
                self.rotateRight(node)
            else:
                self.rotateRight(node)


def list_maker(size):
    # create a list of size elements with values ranging 0..2*size
    # Random List
    randomList = random.sample(range(0, int(size * 2)), size)

    # In - Order
    inOrderList = random.sample(range(0, int(size * 2)), size)
    inOrderList.sort()

    # Reverse - Order
    reversList = random.sample(range(0, int(size * 2)), size)
    reversList.sort(reverse=True)

    # Create Tree Objects
    rand_tree = AVL_tree()
    sort_tree = AVL_tree()
    reve_tree = AVL_tree()

    # Generate AVL Tree from provided lists
    rand_tree.insertList(randomList)
    sort_tree.insertList(inOrderList)
    reve_tree.insertList(reversList)

    buildTree(randomList,y=0)
    buildTree(inOrderList,y=0)
    buildTree(reversList,y=0)

    # Only display tree(s) on these sizes
    # 1- Random 2- In-Order 3- Reverse-Order
    if size == 32:
        output(0, size)
        print(rand_tree)
        output(1, size)
        print(sort_tree)
        output(2, size)
        print(reve_tree)

    else:
        output(0, size)
        output(1, size)
        output(2, size)


def counter(r=0):
    global COUNTER, ROTATE, R_COUNTER, R_ROTATE
    # Increase Red-Tree Counter
    if r == 1:
        R_ROTATE[R_COUNTER] = R_ROTATE[R_COUNTER] + 1
    ROTATE[COUNTER] = ROTATE[COUNTER] + 1

    if COUNTER == 3 and R_COUNTER == 3:
        COUNTER, R_COUNTER = 0, 0
        ROTATE[0], R_ROTATE[0] = 0, 0
        ROTATE[1], R_ROTATE[1] = 0, 0
        ROTATE[2], R_ROTATE[2] = 0, 0


def output(i, size):
    global ROTATE, R_ROTATE
    order = ['Random-Order', 'In-Order', 'Reverse-Order']
    s = ""
    s += "Algorithm       : AVL Tree       |||   Red-Black Tree\n"
    s += "Rotation  Count : " + str(ROTATE[i]) + "           |||   " + str(R_ROTATE[i]) + "\n"
    s += "Data Size       : " + str(size) + "\n"
    s += "Insertion Order : " + order[i] + "\n"

    print(s)


def main():
    # global SIZE
    for i in SIZE:
        list_maker(i)


if __name__ == '__main__':
    main()
