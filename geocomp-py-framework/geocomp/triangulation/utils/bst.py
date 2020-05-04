# Splay tree implementation in Java
# Author: AlgorithmTutor
# Tutorial URL: http://algorithmtutor.com/Data-Structures/Tree/Splay-Trees/
#
# Adapted by Ygor Tavela for polygon y-monotone partitioning algorithm

from geocomp.common import segment
from geocomp.common.prim import left, left_on


class Trap():
    def __init__(self, leftEdge, topSuppVertex, rightEdge):
        self.leftEdge = leftEdge
        self.topSuppVertex = topSuppVertex
        self.rightEdge = rightEdge

    def __eq__(self, other):
        if self is other:
            return True

        if type(self) != type(other):
            return False

        return (self.leftEdge == other.leftEdge) and (self.topSuppVertex == other.topSuppVertex) and (self.rightEdge == other.rightEdge)

    def __lt__(self, other):
        # if left(other.leftEdge[0].coordinates, other.leftEdge[1].coordinates, self.topSuppVertex.coordinates):
        if self.topSuppVertex.x < other.topSuppVertex.x:
            return True

        return False

    def __le__(self, other):
        return self < other and self == other

    def __gt__(self, other):
        # if not left(other.rightEdge[0].coordinates, other.rightEdge[1].coordinates, self.topSuppVertex.coordinates):
        if self.topSuppVertex.x >= other.topSuppVertex.x:
            return True

        return False

    def __repr__(self):
        return '\nTrapezoid: [ leftEdgeInit: ' + repr(self.leftEdge[0]) +\
            '\n leftEdgeTo: ' + repr(self.leftEdge[1]) +\
            '\n rightEdgeInit : ' + repr(self.rightEdge[0]) +\
            '\n rightEdgeTo: ' + repr(self.rightEdge[1]) +\
            '\n topSuppVertex: ' + repr(self.topSuppVertex) + ' ]'

    def trapContainsVertex(self, vertexPoint, testOnlyEdgesAndSupp=False):
        if (self.topSuppVertex == vertexPoint):
            return True
        elif (vertexPoint == self.leftEdge[0]) or (vertexPoint == self.leftEdge[1]) or \
             (vertexPoint == self.rightEdge[0]) or (vertexPoint == self.rightEdge[1]):
            return True

        if not testOnlyEdgesAndSupp and\
            (vertexPoint.x >= self.leftEdge[1].x) and (vertexPoint.x <= self.rightEdge[1].x) and \
            (vertexPoint.y >= self.leftEdge[1].y) and (vertexPoint.y >= self.rightEdge[1].y) and \
                (vertexPoint.y <= self.leftEdge[0].y) and (vertexPoint.y <= self.rightEdge[0].y):
            return True

        return False


class Node:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.left = None
        self.right = None


class SplayTree:
    def __init__(self):
        self.root = None

    # insert the key to the tree in its appropriate position
    def insert(self, key):
        node = Node(key)
        y = None
        x = self.root

        while x != None:
            y = x
            if node.data < x.data:
                x = x.left
            else:
                x = x.right

        # y is parent of x
        node.parent = y
        if y == None:
            self.root = node
        elif node.data < y.data:
            y.left = node
        else:
            y.right = node
        # splay the node
        self.__splay(node)
    # delete the node from the tree

    def getTrapAndRemove(self, vertexPoint, isCaseThree=False):
        if isCaseThree:
            trap = self.get(vertexPoint, True)
            if trap is None:
                trap = self.get(vertexPoint)
        else:
            trap = self.get(vertexPoint)

        if (trap != None):
            self.delete_node(trap)

        return trap

    def delete_node(self, data):
        self.__delete_node_helper(self.root, data)

    def __delete_node_helper(self, node, key):
        x = None
        t = None
        s = None
        while node != None:
            if node.data == key:
                x = node
                break

            if node.data < key:
                node = node.right
            else:
                node = node.left

        if x == None:
            return

        # split operation
        self.__splay(x)
        if x.right != None:
            t = x.right
            t.parent = None
        else:
            t = None

        s = x
        s.right = None
        x = None

        # join operation
        if s.left != None:
            s.left.parent = None

        self.root = self.__join(s.left, t)
        s = None

    def get(self, vertexPoint, testOnlyEdgesAndSupp=False):
        return self.__get_helper(self.root, vertexPoint, testOnlyEdgesAndSupp)

    def __get_helper(self, node, vertexPoint, testOnlyEdgesAndSupp):
        if node is None:
            return

        if (not testOnlyEdgesAndSupp and node.data.trapContainsVertex(vertexPoint)) or\
                (testOnlyEdgesAndSupp and node.data.trapContainsVertex(vertexPoint, True)):
            return node.data
        elif vertexPoint.x < node.data.topSuppVertex.x:
            return self.__get_helper(node.left, vertexPoint, testOnlyEdgesAndSupp)
        elif vertexPoint.x > node.data.topSuppVertex.x:
            return self.__get_helper(node.right, vertexPoint, testOnlyEdgesAndSupp)

    # rotate left at node x

    def __left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != None:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # rotate right at node x
    def __right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != None:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    # Splaying operation. It moves x to the root of the tree
    def __splay(self, x):
        while x.parent != None:
            if x.parent.parent == None:
                if x == x.parent.left:
                    # zig rotation
                    self.__right_rotate(x.parent)
                else:
                    # zag rotation
                    self.__left_rotate(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.left:
                # zig-zig rotation
                self.__right_rotate(x.parent.parent)
                self.__right_rotate(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.right:
                # zag-zag rotation
                self.__left_rotate(x.parent.parent)
                self.__left_rotate(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.left:
                # zig-zag rotation
                self.__left_rotate(x.parent)
                self.__right_rotate(x.parent)
            else:
                # zag-zig rotation
                self.__right_rotate(x.parent)
                self.__left_rotate(x.parent)

    # joins two trees s and t
    def __join(self, s, t):
        if s == None:
            return t

        if t == None:
            return s

        x = self.maximum(s)
        self.__splay(x)
        x.right = t
        t.parent = x
        return x

    # find the node with the minimum key

    def minimum(self, node):
        while node.left != None:
            node = node.left
        return node

    # find the node with the maximum key
    def maximum(self, node):
        while node.right != None:
            node = node.right
        return node

    # find the successor of a given node
    def successor(self, x):
        # if the right subtree is not null,
        # the successor is the leftmost node in the
        # right subtree
        if x.right != None:
            return self.minimum(x.right)

        # else it is the lowest ancestor of x whose
        # left child is also an ancestor of x.
        y = x.parent
        while y != None and x == y.right:
            x = y
            y = y.parent
        return y

    # find the predecessor of a given node
    def predecessor(self, x):
        # if the left subtree is not null,
        # the predecessor is the rightmost node in the
        # left subtree
        if x.left != None:
            return self.maximum(x.left)

        y = x.parent
        while y != None and x == y.left:
            x = y
            y = y.parent
        return y

    def inorder(self, node):
        if node is None:
            return

        self.inorder(node.left)
        print(node.data)
        self.inorder(node.right)
