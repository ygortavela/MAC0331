from geocomp.common import control
from geocomp.common.prim import left, left_on
from .utils import dcel
from .utils import bst


class PolyPartitioning():
    def __init__(self, vertexesList):
        self.partitionDiagonalList = []
        self.dcel = dcel.DCEL(vertexesList)
        self.__partitionatePolygon()
        self.partitions = self.dcel.monotonePolygonsList()

    def __partitionatePolygon(self):
        BST = bst.SplayTree()

        for eventVertex in sorted(self.dcel.vertex):
            vertexNumber = eventVertex.vertexNumber()
            previousVertexNumber = self.dcel.iterateVertex(vertexNumber - 1)
            nextVertexNumber = self.dcel.iterateVertex(vertexNumber + 1)

            previousVertex = self.dcel.getVertex(previousVertexNumber)
            nextVertex = self.dcel.getVertex(nextVertexNumber)

            sweepLineId = control.plot_horiz_line(eventVertex.y, color="cyan")
            suppPointId = eventVertex.coordinates.hilight(color="white")
            control.sleep()

            if ((previousVertex.y < eventVertex.y) and (eventVertex.y < nextVertex.y)) or\
                    ((nextVertex.y < eventVertex.y) and (eventVertex.y < previousVertex.y)) or\
                    ((eventVertex.y < previousVertex.y) and (eventVertex.y == nextVertex.y) and (eventVertex.x < nextVertex.x)) or\
                    ((eventVertex.y == previousVertex.y) and (eventVertex.y > nextVertex.y) and (eventVertex.x > previousVertex.x)):
                self.__caseOne(BST, previousVertex, eventVertex, nextVertex)
            elif (previousVertex.y < eventVertex.y):
                self.__caseTwo(BST, previousVertex, eventVertex, nextVertex)
            else:
                self.__caseThree(BST, eventVertex)

            control.plot_delete(sweepLineId)
            control.plot_delete(suppPointId)

    def __caseOne(self, BST, u, v, w):
        control.sleep()
        if (u.y < w.y):
            u, w = w, u

        trap = BST.getTrapAndRemove(v)
        x = trap.topSuppVertex

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

        leftId = self.dcel.buildSegmentFromEdge(leftEdge).hilight(
            color_line="blue", color_point="red")
        rightId = self.dcel.buildSegmentFromEdge(rightEdge).hilight(
            color_line="blue", color_point="red")

        if self.__interiorDownCusp(x):
            xNumber = x.vertexNumber()
            vNumber = v.vertexNumber()
            diagonal = (xNumber, vNumber)
            self.dcel.addHalfEdge(diagonal)
            self.partitionDiagonalList.append(
                [x.coordinates, v.coordinates])
            self.dcel.buildSegmentFromEdge([x, v]).plot(cor="yellow")

        control.sleep()
        control.plot_delete(leftId)
        control.plot_delete(rightId)

    def __caseTwo(self, BST, u, v, w):
        control.sleep()
        if (left(u.coordinates, v.coordinates, w.coordinates)):
            u, w = w, u

        trap = BST.getTrapAndRemove(v)

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

            secLeftId = self.dcel.buildSegmentFromEdge(trap.leftEdge).hilight(
                color_line="blue", color_point="red")
            secRightId = self.dcel.buildSegmentFromEdge(trap.rightEdge).hilight(
                color_line="blue", color_point="red")

            x = trap.topSuppVertex
            xNumber = x.vertexNumber()
            vNumber = v.vertexNumber()
            diagonal = (xNumber, vNumber)
            self.dcel.addHalfEdge(diagonal)
            self.partitionDiagonalList.append(
                [x.coordinates, v.coordinates])
            self.dcel.buildSegmentFromEdge([x, v]).plot(cor="yellow")

        leftId = self.dcel.buildSegmentFromEdge(leftEdge).hilight(
            color_line="blue", color_point="red")
        rightId = self.dcel.buildSegmentFromEdge(rightEdge).hilight(
            color_line="blue", color_point="red")

        control.sleep()
        control.plot_delete(leftId)
        control.plot_delete(rightId)
        if (trap is not None):
            control.plot_delete(secLeftId)
            control.plot_delete(secRightId)

    def __caseThree(self, BST, v):
        control.sleep()
        firstTrap = BST.getTrapAndRemove(v)
        x = firstTrap.topSuppVertex

        if self.__interiorDownCusp(x):
            xNumber = x.vertexNumber()
            vNumber = v.vertexNumber()
            diagonal = (xNumber, vNumber)
            self.dcel.addHalfEdge(diagonal)
            self.partitionDiagonalList.append(
                [x.coordinates, v.coordinates])
            self.dcel.buildSegmentFromEdge([x, v]).plot(cor="yellow")

        if (firstTrap.leftEdge[1] != v) or (firstTrap.rightEdge[1] != v):
            secondTrap = BST.getTrapAndRemove(v)
            y = secondTrap.topSuppVertex

            if self.__interiorDownCusp(y):
                yNumber = y.vertexNumber()
                vNumber = v.vertexNumber()
                diagonal = (yNumber, vNumber)
                self.dcel.addHalfEdge(diagonal)
                self.partitionDiagonalList.append(
                    [y.coordinates, v.coordinates])
                self.dcel.buildSegmentFromEdge([y, v]).plot(cor="yellow")

            if firstTrap.rightEdge[1] == v:
                newTrap = bst.Trap(firstTrap.leftEdge, v, secondTrap.rightEdge)
                BST.insert(newTrap)
                leftId = self.dcel.buildSegmentFromEdge(firstTrap.leftEdge).hilight(
                    color_line="blue", color_point="red")
                rightId = self.dcel.buildSegmentFromEdge(secondTrap.rightEdge).hilight(
                    color_line="blue", color_point="red")
            else:
                newTrap = bst.Trap(secondTrap.leftEdge, v, firstTrap.rightEdge)
                BST.insert(newTrap)
                leftId = self.dcel.buildSegmentFromEdge(secondTrap.leftEdge).hilight(
                    color_line="blue", color_point="red")
                rightId = self.dcel.buildSegmentFromEdge(firstTrap.rightEdge).hilight(
                    color_line="blue", color_point="red")

            control.sleep()
            control.plot_delete(leftId)
            control.plot_delete(rightId)

    def __interiorDownCusp(self, vertex):
        vertexNumber = vertex.vertexNumber()
        previousVertexNumber = self.dcel.iterateVertex(vertexNumber - 1)
        nextVertexNumber = self.dcel.iterateVertex(vertexNumber + 1)

        point = self.dcel.vertexCoordinates(vertexNumber)
        previousPoint = self.dcel.vertexCoordinates(previousVertexNumber)
        nextPoint = self.dcel.vertexCoordinates(nextVertexNumber)

        if (previousPoint.y > point.y) and (nextPoint.y > point.y):
            return True

        return False


class PolyTriangulate():
    def __init__(self, monotonePolyList):
        self.monotoneDiagonalList = []

        if len(monotonePolyList) > 3:
            self.__dcel = dcel.DCEL(monotonePolyList)
            self.__sortedVertexes = sorted(self.__dcel.vertex)
            self.__stack = []
            self.__triangulate()

    def __triangulate(self):
        self.__stack.append(self.__sortedVertexes[0])
        self.__stack.append(self.__sortedVertexes[1])

        for i in range(2, len(self.__sortedVertexes)):
            adjacentVertexes = self.__getAdjacentVertexes(i)
            currentVertex = self.__sortedVertexes[i]
            suppPointId = currentVertex.coordinates.hilight(color="white")

            stackBase = self.__stackBase()
            stackTop = self.__stackTop()
            neighborFromBase = self.__isVertexNeighborFrom(
                adjacentVertexes, stackBase)
            neighborFromTop = self.__isVertexNeighborFrom(
                adjacentVertexes, stackTop)

            if (neighborFromTop and not neighborFromBase):
                self.__caseA(currentVertex)
            elif (not neighborFromTop and neighborFromBase):
                self.__caseB(currentVertex)
            elif (neighborFromTop and neighborFromBase):
                self.__caseC(currentVertex)

            control.sleep()
            control.plot_delete(suppPointId)

    def __getAdjacentVertexes(self, i):
        return self.__dcel.adjacentVertexes(self.__sortedVertexes[i].vertexNumber())

    def __isVertexNeighborFrom(self, adjacentList, neighbor):
        return adjacentList[0] == neighbor or adjacentList[1] == neighbor

    def __caseA(self, currentVertex):
        isTopNextOrder = self.__stackTop().vertexNumber() == self.__dcel.iterateVertex(
            currentVertex.vertexNumber() + 1)

        while (self.__stackSize() > 1 and self.__angle(currentVertex, isTopNextOrder)):
            control.sleep()
            self.__stack.pop()
            self.__dcel.buildSegmentFromEdge(
                [currentVertex, self.__stackTop()]).plot(cor="white")
            self.monotoneDiagonalList.append(
                [currentVertex.coordinates, self.__stackTop().coordinates])

        self.__stack.append(currentVertex)

    def __caseB(self, currentVertex):
        aux = self.__stackTop()

        while (self.__stackSize() > 1):
            control.sleep()
            self.__dcel.buildSegmentFromEdge(
                [currentVertex, self.__stackTop()]).plot(cor="white")
            self.monotoneDiagonalList.append(
                [currentVertex.coordinates, self.__stackTop().coordinates])
            self.__stack.pop()

        self.__stack.pop()
        self.__stack.append(aux)
        self.__stack.append(currentVertex)

    def __caseC(self, currentVertex):
        self.__stack.pop()

        while (self.__stackSize() > 2):
            control.sleep()
            self.__dcel.buildSegmentFromEdge(
                [currentVertex, self.__stackBeforeTop()]).plot(cor="white")
            self.monotoneDiagonalList.append(
                [currentVertex.coordinates, self.__stackBeforeTop().coordinates])
            self.__stack.pop()

    def __angle(self, currentVertex, isTopNextOrder):
        stackBeforeTop = self.__stackBeforeTop()
        stackTop = self.__stackTop()

        if isTopNextOrder:
            return left(currentVertex.coordinates, stackTop.coordinates, stackBeforeTop.coordinates)

        return left(stackBeforeTop.coordinates, stackTop.coordinates, currentVertex.coordinates)

    def __stackBase(self):
        if not self.__stackIsEmpty():
            return self.__stack[0]

        return None

    def __stackTop(self):
        if not self.__stackIsEmpty():
            return self.__stack[self.__stackSize() - 1]

        return None

    def __stackBeforeTop(self):
        if self.__stackSize() >= 2:
            return self.__stack[self.__stackSize() - 2]

    def __stackIsEmpty(self):
        return self.__stackSize() == 0

    def __stackSize(self):
        return len(self.__stack)


def triangulation(p):
    diagonalList = []
    polyPartitioning = PolyPartitioning(p[0].vertices())
    diagonalList.extend(polyPartitioning.partitionDiagonalList)

    for monotonePolygon in polyPartitioning.partitions:
        polyTriangulate = PolyTriangulate(monotonePolygon)
        diagonalList.extend(polyTriangulate.monotoneDiagonalList)

    print('Diagonal List:')
    print(diagonalList)
