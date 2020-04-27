from geocomp.common import point
from geocomp.common import segment


class Face():
    def __init__(self, edge):
        self.edge = edge

    def __repr__(self):
        return '[ faceEdge: ' + repr(self.edge) + ' ]'


class Vertex():
    def __init__(self, point, edge):
        self.coordinates = point
        self.incidentEdge = edge

    def __repr__(self):
        return '[ coordinates: ' + repr(self.coordinates) +\
            '; incidentEdge: ' + repr(self.incidentEdge) + ' ]'


class HalfEdge():
    def __init__(self, originVertex, twinEdge, nextEdge, previousEdge):
        self.originVertex = originVertex
        self.twinEdge = twinEdge
        self.nextEdge = nextEdge
        self.previousEdge = previousEdge

    def __repr__(self):
        return '\n[ originVertex: ' + repr(self.originVertex) +\
            '\n twinEdge: ' + repr(self.twinEdge) +\
            '\n nextEdge: ' + repr(self.nextEdge) +\
            '\n previousEdge: ' + repr(self.previousEdge) + ' ]'


class DCEL():
    def __init__(self, points):
        self.vertex = []
        self.face = []
        self.halfEdge = {}
        self.size = len(points)
        self.__initVertex(points)
        self.__initFace()
        self.__initHalfEdgeTable(points)
        print(self.vertex[0])
        a = self.incidentEdges(0)
        print(a)

    def __initVertex(self, points):
        for i in range(self.size):
            previousVertex = self.iterateVertex(i - 1)
            edge = (i, previousVertex)
            self.vertex.append(Vertex(points[i], edge))

    def __initFace(self):
        initEdge = (0, 1)
        initTwinEdge = (1, 0)
        self.face.append(Face(initTwinEdge))
        self.face.append(Face(initEdge))

    def __initHalfEdgeTable(self, points):
        for i in range(self.size):
            nextVertex = self.iterateVertex(i + 1)
            afterNextVertex = self.iterateVertex(i + 2)
            previousVertex = self.iterateVertex(i - 1)
            edge = (i, nextVertex)
            twinEdge = (nextVertex, i)

            self.vertex.append(Vertex(points[i], edge))
            self.halfEdge[edge] = HalfEdge(self.vertex[i], twinEdge, (
                nextVertex, afterNextVertex), (previousVertex, i))
            self.halfEdge[twinEdge] = HalfEdge(self.vertex[nextVertex], edge, (
                i, previousVertex), (afterNextVertex, nextVertex))

    def iterateVertex(self, i):
        return (i + self.size) % self.size

    def addEdge(self, initVertex, endVertex):
        pass

    def inCone(self, diagonalInitVertex, diagonalEndVertex):
        pass

    def incidentEdges(self, vertexNumber):
        incidentEdgesList = []
        startEdge = self.vertex[vertexNumber].incidentEdge
        halfEdge = startEdge
        incidentEdgesList.append(halfEdge)

        while (self.nextEdge(self.twinEdge(halfEdge)) != startEdge):
            halfEdge = self.nextEdge(self.twinEdge(halfEdge))
            incidentEdgesList.append(halfEdge)

        return incidentEdgesList

    def originVertex(self, edge):
        return self.halfEdge[edge].originVertex

    def twinEdge(self, edge):
        return self.halfEdge[edge].twinEdge

    def nextEdge(self, edge):
        return self.halfEdge[edge].nextEdge

    def previousEdge(self, edge):
        return self.halfEdge[edge].previousEdge
