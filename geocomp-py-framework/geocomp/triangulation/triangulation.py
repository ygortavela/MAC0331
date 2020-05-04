from geocomp.common import point
from geocomp.common import segment
from geocomp.common import polygon
from geocomp.common import control
from geocomp import config
from geocomp.common.prim import left
from .utils import dcel
from .utils import bst


class PolyPartitioning():
    def __init__(self, vertexesList):
        self.dcel = dcel.DCEL(vertexesList)
        self.size = len(vertexesList)
        self.partitionatePolygon()
        self.partitions = self.dcel.monotonePolygonsList()
        print(self.partitions)

    def partitionatePolygon(self):
        BST = bst.SplayTree()

        for eventVertex in sorted(self.dcel.vertex):
            print(eventVertex)
            vertexNumber = eventVertex.vertexNumber()
            previousVertexNumber = self.dcel.iterateVertex(vertexNumber - 1)
            nextVertexNumber = self.dcel.iterateVertex(vertexNumber + 1)

            previousVertex = self.dcel.getVertex(previousVertexNumber)
            nextVertex = self.dcel.getVertex(nextVertexNumber)

            if ((previousVertex.y < eventVertex.y) and (eventVertex.y < nextVertex.y)) or\
                    ((nextVertex.y < eventVertex.y) and (eventVertex.y < previousVertex.y)) or\
                    ((eventVertex.y < previousVertex.y) and (eventVertex.y == nextVertex.y) and (eventVertex.x < nextVertex.x)) or\
                    ((eventVertex.y == previousVertex.y) and (eventVertex.y > nextVertex.y) and (eventVertex.x > previousVertex.x)):
                self.caseOne(BST, previousVertex, eventVertex, nextVertex)
            elif (previousVertex.y < eventVertex.y):
                self.caseTwo(BST, previousVertex, eventVertex, nextVertex)
            else:
                self.caseThree(BST, eventVertex)

    def caseOne(self, BST, u, v, w):
        control.sleep()
        print('Caso 1')
        if (u.y < w.y):
            u, w = w, u

        trap = BST.getTrapAndRemove(v)
        x = trap.topSuppVertex
        print('x')
        print(trap)
        suppPointId = v.coordinates.hilight(color="white")
        control.sleep()

        if v == trap.leftEdge[1]:
            leftEdge = [v, w]
            rightEdge = trap.rightEdge
            newTrap = bst.Trap(leftEdge, v, rightEdge)
            BST.insert(newTrap)
        else:
            leftEdge = trap.leftEdge
            rightEdge = [v, w]
            newTrap = bst.Trap(leftEdge, v, rightEdge)
            BST.insert(newTrap)

        leftId = self.buildSegmentFromEdge(leftEdge).hilight(
            color_line="blue", color_point="red")
        rightId = self.buildSegmentFromEdge(rightEdge).hilight(
            color_line="blue", color_point="red")

        if self.interiorDownCusp(x):
            xNumber = x.vertexNumber()
            vNumber = v.vertexNumber()
            diagonal = (xNumber, vNumber)
            self.dcel.addHalfEdge(diagonal)
            self.buildSegmentFromEdge([x, v]).plot(cor="yellow")
            print('Adicionei diagonal ' + str(diagonal))

        control.sleep()
        control.plot_delete(suppPointId)
        control.plot_delete(leftId)
        control.plot_delete(rightId)

    def caseTwo(self, BST, u, v, w):
        control.sleep()
        print('Caso 2')
        if (left(u.coordinates, v.coordinates, w.coordinates)):
            u, w = w, u

        trap = BST.getTrapAndRemove(v)
        print('x')
        print(trap)
        suppPointId = v.coordinates.hilight(color="white")
        control.sleep()

        if trap is None:
            leftEdge = [v, u]
            rightEdge = [v, w]
            newTrap = bst.Trap(leftEdge, v, rightEdge)
            BST.insert(newTrap)
        else:
            rightEdge = [v, u]
            newTrap = bst.Trap(trap.leftEdge, v, rightEdge)
            BST.insert(newTrap)

            leftEdge = [v, w]
            newTrap = bst.Trap(leftEdge, v, trap.rightEdge)
            BST.insert(newTrap)

            secLeftId = self.buildSegmentFromEdge(trap.leftEdge).hilight(
                color_line="blue", color_point="red")
            secRightId = self.buildSegmentFromEdge(trap.rightEdge).hilight(
                color_line="blue", color_point="red")

            x = trap.topSuppVertex
            xNumber = x.vertexNumber()
            vNumber = v.vertexNumber()
            diagonal = (xNumber, vNumber)
            self.dcel.addHalfEdge(diagonal)
            self.buildSegmentFromEdge([x, v]).plot(cor="yellow")
            print('Adicionei diagonal ' + str(diagonal))

        leftId = self.buildSegmentFromEdge(leftEdge).hilight(
            color_line="blue", color_point="red")
        rightId = self.buildSegmentFromEdge(rightEdge).hilight(
            color_line="blue", color_point="red")

        control.sleep()
        control.plot_delete(suppPointId)
        control.plot_delete(leftId)
        control.plot_delete(rightId)
        if (trap is not None):
            control.plot_delete(secLeftId)
            control.plot_delete(secRightId)

    def caseThree(self, BST, v):
        control.sleep()
        print('Caso 3')
        firstTrap = BST.getTrapAndRemove(v, True)
        x = firstTrap.topSuppVertex
        print('x')
        print(firstTrap)
        suppPointId = v.coordinates.hilight(color="white")
        control.sleep()

        if self.interiorDownCusp(x):
            xNumber = x.vertexNumber()
            vNumber = v.vertexNumber()
            diagonal = (xNumber, vNumber)
            self.dcel.addHalfEdge(diagonal)
            self.buildSegmentFromEdge([x, v]).plot(cor="yellow")
            print('Adicionei diagonal ' + str(diagonal))

        if (firstTrap.leftEdge[1] != v) or (firstTrap.rightEdge[1] != v):
            secondTrap = BST.getTrapAndRemove(v)
            y = secondTrap.topSuppVertex
            print('y')
            print(secondTrap)

            if self.interiorDownCusp(y):
                yNumber = y.vertexNumber()
                vNumber = v.vertexNumber()
                diagonal = (yNumber, vNumber)
                self.dcel.addHalfEdge(diagonal)
                self.buildSegmentFromEdge([y, v]).plot(cor="yellow")
                print('Adicionei diagonal ' + str(diagonal))

            if firstTrap.rightEdge[1] == v:
                newTrap = bst.Trap(firstTrap.leftEdge, v, secondTrap.rightEdge)
                BST.insert(newTrap)
                leftId = self.buildSegmentFromEdge(firstTrap.leftEdge).hilight(
                    color_line="blue", color_point="red")
                rightId = self.buildSegmentFromEdge(secondTrap.rightEdge).hilight(
                    color_line="blue", color_point="red")
            else:
                newTrap = bst.Trap(secondTrap.leftEdge, v, firstTrap.rightEdge)
                BST.insert(newTrap)
                leftId = self.buildSegmentFromEdge(secondTrap.leftEdge).hilight(
                    color_line="blue", color_point="red")
                rightId = self.buildSegmentFromEdge(firstTrap.rightEdge).hilight(
                    color_line="blue", color_point="red")

            control.sleep()
            control.plot_delete(leftId)
            control.plot_delete(rightId)

        control.plot_delete(suppPointId)

    def interiorDownCusp(self, vertex):
        vertexNumber = vertex.vertexNumber()
        previousVertexNumber = self.dcel.iterateVertex(vertexNumber - 1)
        nextVertexNumber = self.dcel.iterateVertex(vertexNumber + 1)

        point = self.dcel.vertexCoordinates(vertexNumber)
        previousPoint = self.dcel.vertexCoordinates(previousVertexNumber)
        nextPoint = self.dcel.vertexCoordinates(nextVertexNumber)

        if (previousPoint.y > point.y) and (nextPoint.y > point.y):
            return True

        return False

    def buildSegmentFromEdge(self, edge):
        return segment.Segment(edge[0].coordinates, edge[1].coordinates)


class PolyTriangulate():
    def __init__(self, monotonePolyList):
        pass


def triangulation(p):
    polyPartitioning = PolyPartitioning(p[0].vertices())
