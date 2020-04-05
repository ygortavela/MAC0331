from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import control
from geocomp import config


class SegmentPoint():
    def __init__(self, segment, is_left):
        self.__segment = segment
        self.__is_left = is_left

    @property
    def segment(self):
        return self.__segment

    @property
    def is_left(self):
        return self.__is_left

    def compare_points(self, other, axis="x"):
        if axis == "x":
            self_point = self.__segment.init.x if self.__is_left else self.__segment.to.x
            other_point = other.__segment.init.x if other.__is_left else other.__segment.to.x
        else:
            self_point = self.__segment.init.y if self.__is_left else self.__segment.to.y
            other_point = other.__segment.init.y if other.__is_left else other.__segment.to.y

        if self_point > other_point:
            return 1
        elif self_point < other_point:
            return -1
        else:
            return 0


class EventQueue():
    def __init__(self, segments):
        self.__queue = []

        for i in range(len(segments)):
            if (segments[i].init.x > segments[i].to.x):
                segments[i].init, segments[i].to = segments[i].to, segments[i].init
            elif (segments[i].init.x == segments[i].to.x):
                if (segments[i].init.y > segments[i].to.y):
                    segments[i].init, segments[i].to = segments[i].to, segments[i].init

            self.__queue.append(SegmentPoint(segments[i], True))
            self.__queue.append(SegmentPoint(segments[i], False))

        self.__sort_queue(self.__queue)

    def __sort_queue(self, queue):
        if len(queue) > 1:
            mid = len(queue)//2
            L = queue[:mid]
            R = queue[mid:]

            self.__sort_queue(L)
            self.__sort_queue(R)

            i = j = k = 0

            while i < len(L) and j < len(R):
                if L[i].compare_points(R[j]) < 0:
                    queue[k] = L[i]
                    i += 1
                elif L[i].compare_points(R[j]) > 0:
                    queue[k] = R[j]
                    j += 1
                else:
                    if L[i].is_left and not (R[j].is_left):
                        queue[k] = L[i]
                        i += 1
                    elif not (L[i].is_left) and R[j].is_left:
                        queue[k] = R[j]
                        j += 1
                    else:
                        if L[i].compare_points(R[j], "y") <= 0:
                            queue[k] = L[i]
                            i += 1
                        else:
                            queue[k] = R[j]
                            j += 1
                k += 1

            while i < len(L):
                queue[k] = L[i]
                i += 1
                k += 1

            while j < len(R):
                queue[k] = R[j]
                j += 1
                k += 1

    def __iter__(self):
        self.iterator = 0
        return self

    def __next__(self):
        if self.iterator < len(self.__queue):
            element = self.__queue[self.iterator]
            self.iterator += 1
            return element
        else:
            raise StopIteration


class Node():
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None


class BinarySearchTree():
    def __init__(self):
        self.root = None
        self.above = None
        self.below = None

    def insert(self, segment):
        if self.root:
            self.__insert(self.root, segment)
        else:
            self.root = Node(segment)

    def __insert(self, current_node, segment):
        if current_node is not None:
            if current_node.data.has_left(segment.init):
                if current_node.left is not None:
                    self.__insert(current_node.left, segment)
                else:
                    current_node.left = Node(segment)
            else:
                if current_node.right is not None:
                    self.__insert(current_node.right, segment)
                else:
                    current_node.right = Node(segment)
        else:
            current_node = Node(segment)

    def delete(self, current_node, segment):
        if current_node is None:
            return current_node

        if current_node.data.has_left(segment.to):
            current_node.left = self.delete(current_node.left, segment)
        elif not current_node.data.has_left_on(segment.to):
            current_node.right = self.delete(current_node.right, segment)
        else:
            if current_node.left is None:
                temp = current_node.right
                current_node = None
                return temp
            elif current_node.right is None:
                temp = current_node.left
                current_node = None
                return temp

            temp = self.min_node(current_node.right)
            current_node = temp
            current_node.right = self.delete(current_node.right, segment)

        return current_node

    def min_node(self, root):
        current_node = root

        while current_node.left is not None:
            current_node = current_node.left

        return current_node

    def find_above_below(self, current_node, segment):
        if current_node is None:
            return

        if current_node.data == segment:
            if current_node.left is not None:
                tmp = current_node.left

                while tmp.right:
                    tmp = tmp.right

                self.above = tmp

            if current_node.right is not None:
                tmp = current_node.right

                while tmp.left:
                    tmp = tmp.left

                self.below = tmp

            return

        if current_node.data.has_left(segment.to):
            self.below = current_node
            self.find_above_below(current_node.left, segment)
        else:
            self.above = current_node
            self.find_above_below(current_node.right, segment)

    def reset_above_below_state(self):
        self.above = None
        self.below = None


def sweep_line(input_segments):
    bst = BinarySearchTree()
    event_queue = EventQueue(input_segments)

    for event_point in event_queue:
        sweep_line_id = control.plot_vert_line(
            event_point.segment.init.x if event_point.is_left else event_point.segment.to.x, color="cyan")
        bst.reset_above_below_state()

        if event_point.is_left:
            event_point.segment.hilight(color_line="blue", color_point="blue")
            control.sleep()
            bst.insert(event_point.segment)
            bst.find_above_below(bst.root, event_point.segment)
            intersect_above = event_point.segment.intersects(
                bst.above.data) if bst.above is not None else False
            intersect_below = event_point.segment.intersects(
                bst.below.data) if bst.below is not None else False

            if (intersect_above or intersect_below):
                event_point.segment.hilight(
                    color_line="yellow", color_point="yellow")

                if intersect_above:
                    bst.above.data.hilight(
                        color_line="yellow", color_point="yellow")
                elif intersect_below:
                    bst.below.data.hilight(
                        color_line="yellow", color_point="yellow")

                return True
        elif not event_point.is_left:
            control.sleep()
            bst.find_above_below(bst.root, event_point.segment)
            intersect_above_below = bst.below.data.intersects(bst.above.data) if (
                bst.below is not None and bst.above is not None) else False

            if intersect_above_below:
                bst.above.data.hilight(
                    color_line="yellow", color_point="yellow")
                bst.below.data.hilight(
                    color_line="yellow", color_point="yellow")

                return True

            event_point.segment.unhilight()
            bst.delete(bst.root, event_point.segment)

        control.plot_delete(sweep_line_id)
    return False
