from geocomp.common import point
from geocomp.common import segment
from geocomp.common.prim import left, left_on


class Vertex():
    def __init__(self, point, edge):
        self.coordinates = point
        self.incidentEdge = edge

    def __repr__(self):
        return '[ coordinates: ' + repr(self.coordinates) +\
            '; incidentEdge: ' + repr(self.incidentEdge) + ' ]'

    def __eq__(self, other):
        if self is other:
            return True

        if type(self) != type(other):
            return False

        return self.incidentEdge[0] == other.incidentEdge[0]

    def __lt__(self, other):
        if self.coordinates.y < other.coordinates.y:
            return False
        elif self.coordinates.y > other.coordinates.y:
            return True
        else:
            if self.coordinates.x > other.coordinates.x:
                return False
            elif self.coordinates.x < other.coordinates.x:
                return True

        return False

    def vertexNumber(self):
        return self.incidentEdge[0]

    @property
    def x(self):
        return self.coordinates.x

    @property
    def y(self):
        return self.coordinates.y


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
        self.halfEdge = {}
        self.size = len(points)
        self.__initVertex(points)
        self.__initHalfEdgeTable(points)

    def __initVertex(self, points):
        for i in range(self.size):
            previousVertex = self.iterateVertex(i - 1)
            edge = (i, previousVertex)
            self.vertex.append(Vertex(points[i], edge))

    def __initHalfEdgeTable(self, points):
        for i in range(self.size):
            nextVertex = self.iterateVertex(i + 1)
            afterNextVertex = self.iterateVertex(i + 2)
            previousVertex = self.iterateVertex(i - 1)
            edge = (i, nextVertex)
            twinEdge = (nextVertex, i)

            self.halfEdge[edge] = HalfEdge(self.vertex[i], twinEdge, (
                nextVertex, afterNextVertex), (previousVertex, i))
            self.halfEdge[twinEdge] = HalfEdge(self.vertex[nextVertex], edge, (
                i, previousVertex), (afterNextVertex, nextVertex))

    def iterateVertex(self, i):
        return (i + self.size) % self.size

    def monotonePolygonsList(self):
        visitedVertex = [False for vertex in self.vertex]
        polygons = []

        for i in range(self.size):
            if not visitedVertex[i]:
                faceVertex = []
                startEdge = self.twinEdge(self.vertex[i].incidentEdge)
                edge = startEdge
                faceVertex.append(self.vertex[edge[0]].coordinates)
                visitedVertex[edge[0]] = True

                while self.nextEdge(edge) != startEdge:
                    edge = self.nextEdge(edge)
                    visitedVertex[edge[0]] = True
                    faceVertex.append(self.vertex[edge[0]].coordinates)

                polygons.append(faceVertex)

        return polygons

    def addHalfEdge(self, diagonalEdge):
        revertedDiagonalEdge = self.revertEdgeVertex(diagonalEdge)
        initIncidentEdges = self.incidentEdgesInCone(diagonalEdge)
        endIncidentEdges = self.incidentEdgesInCone(revertedDiagonalEdge)

        self.halfEdge[diagonalEdge] = HalfEdge(self.vertex[diagonalEdge[0]],
                                               revertedDiagonalEdge,
                                               endIncidentEdges[1],
                                               self.twinEdge(initIncidentEdges[0]))
        self.halfEdge[revertedDiagonalEdge] = HalfEdge(self.vertex[revertedDiagonalEdge[0]],
                                                       diagonalEdge,
                                                       initIncidentEdges[1],
                                                       self.twinEdge(endIncidentEdges[0]))
        self.halfEdge[self.twinEdge(
            initIncidentEdges[0])].nextEdge = diagonalEdge
        self.halfEdge[endIncidentEdges[1]].previousEdge = diagonalEdge
        self.halfEdge[self.twinEdge(
            endIncidentEdges[0])].nextEdge = revertedDiagonalEdge
        self.halfEdge[initIncidentEdges[1]].previousEdge = revertedDiagonalEdge

    def removeHalfEdge(self, diagonalEdge):
        twinEdge = self.twinEdge(diagonalEdge)

        self.halfEdge[self.previousEdge(
            diagonalEdge)].nextEdge = self.nextEdge(twinEdge)
        self.halfEdge[self.nextEdge(
            twinEdge)].previousEdge = self.previousEdge(diagonalEdge)

        self.halfEdge[self.previousEdge(
            twinEdge)].nextEdge = self.nextEdge(diagonalEdge)
        self.halfEdge[self.nextEdge(
            diagonalEdge)].previousEdge = self.previousEdge(twinEdge)

        del self.halfEdge[diagonalEdge]
        del self.halfEdge[twinEdge]

    def incidentEdgesInCone(self, diagonalEdge):
        incidentEdgesList = self.incidentEdges(diagonalEdge[0])
        edgesInConeList = [incidentEdgesList[0], incidentEdgesList[1]]

        if (len(incidentEdgesList) == 2):
            return edgesInConeList

        for i in range(len(incidentEdgesList) - 1):
            edgesInConeList[0] = incidentEdgesList[i]
            edgesInConeList[1] = incidentEdgesList[i + 1]

            if (self.diagonalInCone(edgesInConeList[0][1], edgesInConeList[1][1], diagonalEdge)):
                break

        return edgesInConeList

    def incidentEdges(self, vertexNumber):
        incidentEdgesList = []
        startEdge = self.vertex[vertexNumber].incidentEdge
        halfEdge = startEdge
        incidentEdgesList.append(halfEdge)

        while (self.nextEdge(self.twinEdge(halfEdge)) != startEdge):
            halfEdge = self.nextEdge(self.twinEdge(halfEdge))
            incidentEdgesList.append(halfEdge)

        return incidentEdgesList

    def diagonalInCone(self, firstVertex, secondVertex, diagonalEdge):
        i = self.vertexCoordinates(diagonalEdge[0])
        j = self.vertexCoordinates(diagonalEdge[1])
        u = self.vertexCoordinates(firstVertex)
        w = self.vertexCoordinates(secondVertex)

        if (left_on(u, i, w)):
            return left(i, j, u) and left(j, i, w)
        else:
            return not (left_on(i, j, w) and left_on(j, i, u))

    def adjacentVertexes(self, vertexNumber):
        adjacentVertexesList = []
        startEdge = self.vertex[vertexNumber].incidentEdge
        halfEdge = startEdge
        adjacentVertex = self.endVertex(halfEdge)
        adjacentVertexesList.append(adjacentVertex)

        while (self.nextEdge(self.twinEdge(halfEdge)) != startEdge):
            halfEdge = self.nextEdge(self.twinEdge(halfEdge))
            adjacentVertex = self.endVertex(halfEdge)
            adjacentVertexesList.append(adjacentVertex)

        return adjacentVertexesList

    def adjacentEdges(self, edge):
        previousEdge = self.twinEdge(self.previousEdge(edge))
        nextEdge = self.nextEdge(self.twinEdge(edge))

        return [previousEdge, nextEdge]

    def originVertex(self, edge):
        return self.halfEdge[edge].originVertex

    def endVertex(self, edge):
        return self.originVertex(self.nextEdge(edge))

    def vertexCoordinates(self, vertexNumber):
        return self.vertex[vertexNumber].coordinates

    def getVertex(self, vertexNumber):
        return self.vertex[vertexNumber]

    def twinEdge(self, edge):
        return self.halfEdge[edge].twinEdge

    def nextEdge(self, edge):
        return self.halfEdge[edge].nextEdge

    def previousEdge(self, edge):
        return self.halfEdge[edge].previousEdge

    def revertEdgeVertex(self, edge):
        return (edge[1], edge[0])

    def buildSegmentFromEdge(self, edge):
        return segment.Segment(edge[0].coordinates, edge[1].coordinates)
