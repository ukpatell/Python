"""
# Author        : Umangkumar Patel
# Date Created  : April 4, 2022,
# Date Modified : April 5, 2022,
# Instructor    : Professor Eugene
# Description   : Perform a series of empirical tests on two different self-balancing search tree implementations,
#                 counting the number of comparisons and rotations used when adding elements.
# GitHub        : https://github.com/ukpatell/Python.git
# Sources       : https://github.com/davidtweinberger/avl_tree/blob/master/tree.py
"""
import random

SIZE = [32, 256, 1024, 2048]
ROTATE_COUNT = 0


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

        # def __str__(self):
        #     """
        #     Traverses and prints the binary tree in an organized and pretty way.
        #     Uses a BFS (level-order) traversal.
        #     """
        #     global ROTATE_COUNT
        #     self.synchronizeFields()
        #     if self._depth == 0:
        #         return ""
        #     s = ""
        #     queue = []
        #     level = 0
        #     queue.append((1, self._root))
        #     while len(queue):
        #         nodelev, node = queue.pop(0)
        #         if (not node):
        #             if (self._depth - nodelev + 1) <= 0:
        #                 continue
        #             if nodelev != level:
        #                 s += "\n"
        #                 s += " " * int(self._max_chars * (2 ** (self._depth - nodelev) - 1))
        #                 level = nodelev
        #             s += " " * self._max_chars * (2 ** (self._depth - nodelev + 1) - 1)
        #             s += " " * self._max_chars
        #             queue.append((nodelev + 1, None))
        #             queue.append((nodelev + 1, None))
        #             continue
        #         if nodelev != level:
        #             s += "\n"
        #             s += " " * self._max_chars * (2 ** (self._depth - nodelev) - 1)
        #             level = nodelev
        #         for i in range(int(self._max_chars - len(str(node.data)))):
        #             s += " "
        #         s += str(node.data)
        #         s += " " * self._max_chars * (2 ** (self._depth - nodelev + 1) - 1)
        #         if node.left:
        #             queue.append((nodelev + 1, node.left))
        #         else:
        #             queue.append((nodelev + 1, None))
        #         if node.right:
        #             queue.append((nodelev + 1, node.right))
        #         else:
        #             queue.append((nodelev + 1, None))
        #     s += "\n"
        #     order = ['Random-Order\n','In-Order\n','Reverse-Order\n']
        #
        #     # s += "Algorithm       : AVL Tree"
        #     # s += "Data Size       : " + str(s) + "\n"
        #     # s += "Insertion Order : " + order[i]
        #     # s += "Rotation  Count : " + str(ROTATE_COUNT)
        #     # s += "\n"
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
        global ROTATE_COUNT
        ROTATE_COUNT = 0

        if l is None:
            return
        try:
            for ele in l:
                self.insert(ele)
        except TypeError:
            return

    def insert(self, data):
        """
        This is the external insert method for the data structure.
        Args:
            data: a data object to be inserted into the tree
        """
        if data == None:
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
        global ROTATE_COUNT
        ROTATE_COUNT += 1
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
        global ROTATE_COUNT
        ROTATE_COUNT += 1
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

    # Only display tree(s) on this sizes
    # 1- Random 2- In-Order 3- Reverse-Orderr
    if size == 32:
        # print(rand_tree, 0, size)
        # print(sort_tree, 1, size)
        # print(reve_tree, 2, size)
        display(rand_tree, 0, size)
        display(sort_tree, 1, size)
        display(reve_tree, 2, size)


def display(self, i, s):
    """
        Traverses and prints the binary tree in an organized and pretty way.
        Uses a BFS (level-order) traversal.
        """
    global ROTATE_COUNT
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
    s += "\n"
    order = ['Random-Order\n', 'In-Order\n', 'Reverse-Order\n']

    s += "Algorithm       : AVL Tree"
    s += "Data Size       : " + str(s) + "\n"
    s += "Insertion Order : " + order[i]
    s += "Rotation  Count : " + str(ROTATE_COUNT)
    s += "\n"


def main():
    # global SIZE
    for i in SIZE:
        list_maker(i)


if __name__ == '__main__':
    main()
