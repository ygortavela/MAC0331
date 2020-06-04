from geocomp.triangulation import triangulation
from geocomp.triangulation.utils import dcel


class ConvexPolyPartition():
    def __init__(self, p):
        triang = triangulation.Triangulation(p)
        diagonalList = triang.diagonalList
        triang.clearDiagonalPlots()
        self.dcel = dcel.DCEL(p[0].vertices())
        self.diagonalQueue = []

        for diagonal in diagonalList:
            self.dcel.addHalfEdge((diagonal[0].vertexNumber(),
                                   diagonal[1].vertexNumber()))
            diagonalPlotID = self.dcel.buildSegmentFromEdge(
                diagonal).plot(cor="yellow")
            self.diagonalQueue.append([diagonal, diagonalPlotID])


def convexpolypartition(p):
    polyPart = ConvexPolyPartition(p)
    # print(polyPart.diagonalQueue)
