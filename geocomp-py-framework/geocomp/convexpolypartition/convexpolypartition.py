from geocomp.common import control
from geocomp.common import segment
from geocomp.triangulation import triangulation
from geocomp.triangulation.utils import dcel
from geocomp.common.prim import left, left_on


class ConvexPolyPartition():
    def __init__(self, p):
        triang = triangulation.Triangulation(p)
        self.dcel = triang.polyDCEL
        self.diagonalQueue = triang.diagonalList

        self.partitionatePoly()

    def partitionatePoly(self):
        for diagonal in self.diagonalQueue:
            u = self.dcel.originVertex(diagonal[0]).coordinates
            v = self.dcel.endVertex(diagonal[0]).coordinates
            seg = segment.Segment(u, v)
            seg.hilight(color_line="cyan", color_point="cyan")

            if not self.essentialEdge(diagonal[0]):
                self.dcel.removeHalfEdge(diagonal[0])
                control.plot_delete(diagonal[1])

            control.sleep()
            seg.unhilight()

    def essentialEdge(self, diagonal):
        diagonalAdjacentEdges = self.dcel.adjacentEdges(diagonal)
        diagonalTwinAdjacentEdges = self.dcel.adjacentEdges(
            self.dcel.twinEdge(diagonal))

        control.sleep()
        segListOne = self.__hilightAdjacentEdges(diagonalAdjacentEdges)
        segListTwo = self.__hilightAdjacentEdges(diagonalTwinAdjacentEdges)
        control.sleep()
        self.__unhilightAdjacentEdges(segListOne)
        self.__unhilightAdjacentEdges(segListTwo)

        return self.__testReflexVertex(diagonalAdjacentEdges) or self.__testReflexVertex(diagonalTwinAdjacentEdges)

    def __testReflexVertex(self, adjacentEdges):
        u = self.dcel.originVertex(adjacentEdges[1])
        v = self.dcel.endVertex(adjacentEdges[1])
        w = self.dcel.endVertex(adjacentEdges[0])

        return self.__angle(u, v, w)

    def __angle(self, u, v, w):
        return not left_on(u.coordinates, v.coordinates, w.coordinates)

    def __hilightAdjacentEdges(self, adjacentEdges):
        u = self.dcel.originVertex(adjacentEdges[1])
        v = self.dcel.endVertex(adjacentEdges[1])
        w = self.dcel.endVertex(adjacentEdges[0])

        segOne = segment.Segment(u.coordinates, v.coordinates)
        segTwo = segment.Segment(u.coordinates, w.coordinates)
        segOne.hilight(color_line="green", color_point="green")
        segTwo.hilight(color_line="green", color_point="green")

        return [segOne, segTwo]

    def __unhilightAdjacentEdges(self, segAdjacentList):
        segAdjacentList[0].unhilight()
        segAdjacentList[1].unhilight()


def convexpolypartition(p):
    polyPart = ConvexPolyPartition(p)
