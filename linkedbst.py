"""
File: linkedbst.py
Author: Ken Lambert
"""

from random import choices
from secrets import choice
from time import time
from timeit import timeit
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree." "")

        # Helper function to adjust placement of an item
        def liftmaxinleftsubtreetotop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = "L"
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = "L"
                current_node = current_node.left
            else:
                direction = "R"
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None and not current_node.right == None:
            liftmaxinleftsubtreetotop(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == "L":
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def is_leaf(self, node):
        """Returns True if node is leaf"""
        return node.left is None and node.right is None

    def height(self):
        """
        Return the height of tree
        :return: int
        """

        def height1(top):
            """
            Helper function
            :param top:
            :return:
            """
            if self.is_leaf(top):
                return 0
            else:
                children = []
                if top.left is not None:
                    children.append(top.left)
                if top.right is not None:
                    children.append(top.right)
                return 1 + max(height1(child) for child in children)

        return height1(self._root)

    def is_balanced(self):
        """
        Return True if tree is balanced
        :return:
        """
        if self.height() < 2 * log(len(self) + 1) - 1:
            return True
        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        ordered_tree = self.inorder()
        lst = []
        for i in ordered_tree:
            if i in range(low, high + 1):
                lst.append(i)
        return lst

    def rebalance(self):
        """
        Rebalances the tree.
        :return:
        """
        ordered_tree = self.inorder()
        lst = []
        for i in ordered_tree:
            lst.append(i)
        self.clear()

        def sorted_array(arr):
            mid = len(arr) // 2
            if arr:
                self.add(arr[mid])
                sorted_array(arr[:mid])
                sorted_array(arr[mid + 1 :])

        sorted_array(lst)
        return self

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        ordered_tree = self.inorder()
        lst = []
        for i in ordered_tree:
            lst.append(i)
        if item == lst[-1]:
            return None
        elif item not in lst:
            if item < lst[-1]:
                lst.append(item)
                lst = sorted(lst)
                return lst[lst.index(item) + 1]
            return None
        else:
            return lst[lst.index(item) + 1]

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        ordered_tree = self.inorder()
        lst = []
        for i in ordered_tree:
            lst.append(i)
        if item == lst[0]:
            return None
        elif item not in lst:
            if item > lst[0]:
                lst.append(item)
                lst = sorted(lst)
                return lst[lst.index(item) - 1]
            return None
        else:
            return lst[lst.index(item) - 1]

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, mode="r") as file:
            lst = file.read().split("\n")

        def find_in_list(lst):
            words = choices(lst, k=10000)
            lst = lst[:65000]
            result_of_seraching = []
            for word in words:
                if word in lst:
                    result_of_seraching.append(word)

        result = timeit("find_in_list(lst)", globals=locals(), number=1)
        print(f"Result of searching 10,000 words in a list: {result}")

        def finding_2(lst):
            lbst1 = LinkedBST()
            for word in lst[:1100]:
                lbst1.add(word)
            words = choices(lst, k=10000)
            lst1 = []
            for word in words:
                if lbst1.find(word):
                    lst1.append(word)

        result = timeit("finding_2(lst)", globals=locals(), number=1)
        print(f"Result of searching 10,000 words in a sorted BST: {result}")

        def finding_3(lst):
            lbst2 = LinkedBST()
            words = choices(lst, k=60000)
            for word in words:
                lbst2.add(word)
            lst2 = []
            searching_words = choices(lst, k=10000)
            for word in searching_words:
                if lbst2.find(word):
                    lst2.append(word)

        result = timeit("finding_3(lst)", globals=locals(), number=1)
        print(f"Result of searching 10,000 words in BST from random words: {result}")

        def finding_4(lst):
            lbst3 = LinkedBST()
            words = choices(lst, k=60000)
            for word in words:
                lbst3.add(word)
            lbst3 = lbst3.rebalance()
            print(lbst3.is_balanced())
            lst3 = []
            searching_words = choices(lst, k=10000)
            for word in searching_words:
                if lbst3.find(word):
                    lst3.append(word)

        result = timeit("finding_4(lst)", globals=locals(), number=1)
        print(f"Result of searching 10,000 words in a balanced BST: {result}")


lbst = LinkedBST([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
lbst.rebalance()
print(lbst.is_balanced())
print(lbst)
lbst.demo_bst("D:\\УКУ\\ОП\\2022\\Lab13\\binary_search_tree\\words (2).txt")
