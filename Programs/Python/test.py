# CISC 233 LAB 3 Self-Balancing Binary Search Trees
# Author        : Umangkumar Patel
# Date Created  : March 21, 2022
# Date Modified : March 21, 2022
# Instructor    : Professor Eugene
# Description   : Perform a series of empirical tests on two different self-balancing search tree implementations,
#                 counting the number of comparisons and rotations used when adding elements.
# GitHub        : https://github.com/ukpatell/Python.git
# Sources       : https://github.com/sphinxyun/algorithm-in-python/blob/b69b5641d0457f5dcfe824755d9c302340980114/dataStructure/redBlackTree.py
import random
from functools import total_ordering
from colorama import init, Fore, Back, Style

# Initializes Colorama
init(autoreset=True)

# Color Prefix
pref = "\033["
reset = f'{pref}0m'
red = "31m"


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
    rbtree = redBlackTree()
    for i in nums:
        rbtree.insert(node(i))
        if x == 1: print(rbtree)  # Enable to print each step
        # print(rbtree)
        if visitor:
            visitor(rbtree, i)

    if y == 1: print(rbtree)  # Only prints the final resultant R-B tree
    print(f'Built Red-Black Tree Using: {nums}')
    print('Root Value                 : ', rbtree.root)
    print('Height of Binary Tree      : ', get_height(rbtree.root))
    if order == 1:
        print('In-Order Traversal         : ')
        print(inorder(rbtree.root),'\n')  # Only prints in-order traversal if enabled

    return rbtree, nums


def intro32():
    print(Style.NORMAL + Back.WHITE + Fore.BLACK + "NOTE:")
    print(Style.NORMAL + Back.WHITE + Fore.BLACK + "THIS SECTION OF TEST WILL BE CONDUCTING WITH 32 DISTINCT")
    print(Style.NORMAL + Back.WHITE + Fore.BLACK + "ELEMENTS WHERE THEY WILL BE IN THE FOLLOWING ORDERS:")
    print(Style.NORMAL + Back.YELLOW + Fore.BLACK + "IN-ORDER,REVERSE-ORDER, RANDOM-ORDER")
    print(Style.NORMAL + Back.WHITE + Fore.BLACK + "TO PRINT EACH STEP ON HOW TREE IS BUILT")
    print(Style.NORMAL + Back.WHITE + Fore.BLACK + "PLEASE ENTER X = 1 WHEN CALLING FUNCTION")
    print(Style.NORMAL + Back.WHITE + Fore.BLACK + "PLEASE ENTER order = 1 WHEN CALLING FUNCTION")
    print(Style.NORMAL + Back.WHITE + Fore.BLACK + "TO PRINT IN-ORDER TRAVERSAL")
    print('\n')


def intro256():
    print('\n\n')
    print(Style.NORMAL + Back.WHITE + Fore.BLACK + "NOTE:")
    print(Style.NORMAL + Back.WHITE + Fore.BLACK + "THIS SECTION OF TEST WILL BE CONDUCTING WITH 256 DISTINCT")
    print(Style.NORMAL + Back.WHITE + Fore.BLACK + "ELEMENTS WHERE THEY WILL BE IN THE FOLLOWING ORDERS:")
    print(Style.NORMAL + Back.YELLOW + Fore.BLACK + "IN-ORDER,REVERSE-ORDER, RANDOM-ORDER")
    print(Style.NORMAL + Back.WHITE + Fore.BLACK + "TO PRINT EACH STEP ON HOW TREE IS BUILT")
    print(Style.NORMAL + Back.WHITE + Fore.BLACK + "PLEASE ENTER X = 1 WHEN CALLING FUNCTION")
    print(Style.NORMAL + Back.WHITE + Fore.BLACK + "NOT PRINTING OUTPUT BECAUSE OF LENGTH")
    print(Style.NORMAL + Back.WHITE + Fore.BLACK + "PLEASE ENTER order = 1 WHEN CALLING FUNCTION")
    print(Style.NORMAL + Back.WHITE + Fore.BLACK + "TO PRINT IN-ORDER TRAVERSAL")

    print('\n')


# Same data expressed in different order, will impact the overall structure of tree, thus affecting the performance
# RED - BAD TREE              GREEN - GOOD TREE (BALANCED)

# Include x = 1 in the buildtree() function to print construction of tree
# Include y = 0 in the buildtree() function to avoid printing for length or other purpose(s)
# Include order = 1 in the buildtree() function to print in-order traversal of the tree

inOrderData32 = [5,10,15,20,25]
reverseData32 = [25,20,15,10,5]
randomData32 = random.sample(inOrderData32, len(inOrderData32))

intro32()

buildTree(inOrderData32)
print(Style.NORMAL + Back.LIGHTRED_EX + Fore.BLACK + "IN-ORDER")
buildTree(reverseData32)
print(Style.NORMAL + Back.LIGHTRED_EX + Fore.BLACK + "REVERSE-ORDER")
buildTree(randomData32)
print(Style.NORMAL + Back.LIGHTGREEN_EX + Fore.BLACK + "RANDOM-ORDER")

# Same data expressed in different order, will impact the overall structure of tree, thus affecting the performance
# RED - BAD TREE              GREEN - GOOD TREE (BALANCED)
inOrderData256 = [1, 3, 7, 10, 12, 14, 15, 18, 21, 22, 27, 30, 32, 33, 35]
reverseData256 = [35, 33, 32, 30, 27, 22, 21, 18, 15, 14, 12, 10, 7, 3, 1]
randomData256 = random.sample(inOrderData256, len(inOrderData256))

intro256()

buildTree(inOrderData256, y=0,order=1)
print(Style.NORMAL + Back.LIGHTRED_EX + Fore.BLACK + "IN-ORDER")
buildTree(reverseData256, y=0,order=1)
print(Style.NORMAL + Back.LIGHTRED_EX + Fore.BLACK + "REVERSE-ORDER")
buildTree(randomData256, y=0,order=1)
print(Style.NORMAL + Back.LIGHTGREEN_EX + Fore.BLACK + "RANDOM-ORDER")
