from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import control
from geocomp import config


class SegmentPoint():
    def __init__(self, segment, seg_number, is_left):
        self.__segment = segment
        self.__seg_number = seg_number
        self.__is_left = is_left

    @property
    def segment(self):
        return self.__segment

    @property
    def seg_number(self):
        return self.__seg_number

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

            self.__queue.append(SegmentPoint(segments[i], i, True))
            self.__queue.append(SegmentPoint(segments[i], i, False))

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
                if L[i].compare_points(R[j]) == -1:
                    queue[k] = L[i]
                    i += 1
                elif L[i].compare_points(R[j]) == 1:
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
        self.item = 0
        return self

    def __next__(self):
        if self.item < len(self.__queue):
            element = self.__queue[self.item]
            self.item += 1
            return element
        else:
            raise StopIteration


def Sweep_line(l):
    event_queue = EventQueue(l)
    for event_point in event_queue:
        if event_point.is_left:
            print(repr(event_point.segment.init) + ' ' +
                  str(event_point.seg_number) + 'left\n')
        else:
            print(repr(event_point.segment.to) + ' ' +
                  str(event_point.seg_number) + 'right\n')

    filter_segments(l)
    intersections = []

    for s in l:
        s.plot()

    for i in range(0, len(l) - 1):
        l[i].hilight(color_line="blue")
        control.sleep()
        for j in range(i + 1, len(l)):
            l[j].hilight()
            control.sleep()
            if (prim.intersect(l[i].init, l[i].to, l[j].init, l[j].to)):
                # guarda os indices dos segmentos que se intersectam
                l[i].hilight(color_line="yellow")
                l[j].hilight(color_line="yellow")
                control.sleep()
                intersections.append((i, j))
                l[i].hilight(color_line="blue")
            l[j].plot()
        l[i].plot()


def filter_segments(l):
    for i in range(len(l)):
        if (l[i].init.x > l[i].to.x):
            l[i].init, l[i].to = l[i].to, l[i].init
        elif (l[i].init.x == l[i].to.x):
            if (l[i].init.y > l[i].to.y):
                l[i].init, l[i].to = l[i].to, l[i].init
