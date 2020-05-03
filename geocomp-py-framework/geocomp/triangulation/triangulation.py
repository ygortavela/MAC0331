from geocomp.common import point
from geocomp.common import segment
from geocomp.common import polygon
from geocomp.common import control
from geocomp import config
from .utils import dcel
from .utils import bst


class PolyPoint():
    def __init__(self, pointNumber, pointCoordinates):
        self.pointNumber = pointNumber
        self.pointCoordinates = pointCoordinates

    def __gt__(self, other):
        if self.pointCoordinates.y < other.pointCoordinates.y:
            return True
        elif self.pointCoordinates.y > other.pointCoordinates.y:
            return False
        else:
            if self.pointCoordinates.x > other.pointCoordinates.x:
                return True
            elif self.pointCoordinates.x < other.pointCoordinates.x:
                return False

        return False

    def __lt__(self, other):
        if self.pointCoordinates.y < other.pointCoordinates.y:
            return False
        elif self.pointCoordinates.y > other.pointCoordinates.y:
            return True
        else:
            if self.pointCoordinates.x > other.pointCoordinates.x:
                return False
            elif self.pointCoordinates.x < other.pointCoordinates.x:
                return True

        return False


class PolyPartitioning():
    def __init__(self, vertexesList):
        self.pointList = []
        self.dceList = dcel.DCEL(vertexesList)
        self.size = len(vertexesList)

        for i in range(self.size):
            point = PolyPoint(i, vertexesList[i])
            self.pointList.append(point)

        self.pointList.sort()

    def interiorDownCusp(self, point):
        previousPoint = self.iteratePoint

    # criar iterador que percorre ordenado

    def iteratePoint(self, i):
        return (i + self.size) % self.size


def triangulation(p):
    polyPartitioning = PolyPartitioning(p[0].vertices())
