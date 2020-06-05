from geocomp.common import control
from geocomp.triangulation import triangulation
from geocomp.triangulation.utils import dcel


class ConvexPolyPartition():
    def __init__(self, p):
        triang = triangulation.Triangulation(p)
        triang.clearDiagonalPlots()
        self.dcel = triang.polyDCEL
        self.diagonalQueue = []

        for diagonal in triang.diagonalList:
            diagonalInit = diagonal[0][0]
            diagonalEnd = diagonal[0][1]
            self.diagonalQueue.append([diagonal[0], control.plot_segment(
                diagonalInit.x, diagonalInit.y, diagonalEnd.x, diagonalEnd.y, "white")])


def convexpolypartition(p):
    polyPart = ConvexPolyPartition(p)
    print(polyPart.diagonalQueue)
