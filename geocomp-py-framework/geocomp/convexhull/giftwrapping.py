from geocomp.common.prim import left, left_on
from geocomp.common import control
from geocomp import config


class ConvexHull():
    def __init__(self, pointList):
        self.convexHull = []
        self.pointList = pointList
        self.pointListSize = len(pointList)

    def giftWrapping(self):
        if len(self.convexHull) > 0:
            return

        firstHullPointIndex = self.__getExtremePoint()
        self.convexHull.append(firstHullPointIndex)
        nextHullPointIndex = (firstHullPointIndex + 1 +
                              self.pointListSize) % self.pointListSize
        minIndexPlotId = []

        while nextHullPointIndex != firstHullPointIndex:
            nextHullPointIndex = (self.convexHull[-1] + 1 +
                                  self.pointListSize) % self.pointListSize
            pointSegmentIdList = []
            minIndexPlotId = self.__hilightSegment(
                self.convexHull[-1], nextHullPointIndex, lineColor="green", pointColor="green")
            control.sleep()

            for index in range(self.pointListSize):
                if index != nextHullPointIndex:
                    pointSegmentIdList.append(self.__hilightSegment(
                        self.convexHull[-1], index))

                if self.__rightWrap(self.convexHull[-1], nextHullPointIndex, index):
                    nextHullPointIndex = index
                    self.__unhilightSegment(minIndexPlotId)
                    minIndexPlotId = self.__hilightSegment(
                        self.convexHull[-1], index, lineColor="green", pointColor="green")

                if index != nextHullPointIndex:
                    control.sleep()

            for pointSegmentId in pointSegmentIdList:
                self.__unhilightSegment(pointSegmentId)

            self.__unhilightSegment(minIndexPlotId)
            self.__hilightSegment(
                self.convexHull[-1], nextHullPointIndex, lineColor="cyan", pointColor="cyan")
            self.convexHull.append(nextHullPointIndex)

            if nextHullPointIndex != firstHullPointIndex:
                control.sleep()

    def graham(self):
        if len(self.convexHull) > 0:
            return

        self.__sortPointList()
        self.convexHull = [0, 1, 2]
        hullSegmentIdList = []
        hullSize = 3

        for hullPointIndex in range(hullSize):
            hullSegmentIdList.append(self.__hilightSegment(
                self.convexHull[hullPointIndex % hullSize],
                self.convexHull[(hullPointIndex + 1) % hullSize],
                lineColor="cyan", pointColor="cyan"))

            if hullPointIndex < 2:
                control.sleep()

        for pointIndex in range(3, self.pointListSize):
            pointPlotId = self.pointList[pointIndex].hilight(color="red")
            control.sleep()

            while self.__rightWrap(self.convexHull[-2], self.convexHull[-1], pointIndex):
                linePlotId = self.__hilightLine(
                    self.convexHull[-2], self.convexHull[-1])
                control.sleep()
                self.convexHull.pop()
                self.__unhilightSegment(hullSegmentIdList.pop())
                control.plot_delete(linePlotId)
                control.sleep()

            self.__unhilightSegment(hullSegmentIdList.pop())
            hullSegmentIdList.append(self.__hilightSegment(
                self.convexHull[-1],
                pointIndex,
                lineColor="cyan", pointColor="cyan"))
            control.sleep()
            hullSegmentIdList.append(self.__hilightSegment(
                pointIndex,
                self.convexHull[0],
                lineColor="cyan", pointColor="cyan"))
            self.convexHull.append(pointIndex)
            control.plot_delete(pointPlotId)

            if pointIndex < self.pointListSize - 1:
                control.sleep()

        self.convexHull.append(0)

    def __sortPointList(self):
        hullPointIndex = self.__getExtremePoint(coordinateKey=lambda k: k.y)
        self.pointList[0], self.pointList[hullPointIndex] = self.pointList[hullPointIndex], self.pointList[0]
        self.__mergeSortPointList()

    def __getExtremePoint(self, coordinateKey=lambda k: k.x):
        extremeIndex = 0

        for index in range(1, self.pointListSize):
            if coordinateKey(self.pointList[index]) < coordinateKey(self.pointList[extremeIndex]):
                extremeIndex = index

        return extremeIndex

    def __mergeSortPointList(self):
        self.__mergeSortPointListRec(1, self.pointListSize - 1)

    def __mergeSortPointListRec(self, startIndex, endIndex):
        if endIndex <= startIndex:
            return

        midIndex = (startIndex + endIndex)//2
        self.__mergeSortPointListRec(startIndex, midIndex)
        self.__mergeSortPointListRec(midIndex + 1, endIndex)
        self.__merge(startIndex, midIndex, endIndex)

    def __merge(self, startIndex, midIndex, endIndex):
        leftCopy = self.pointList[startIndex:midIndex + 1]
        rightCopy = self.pointList[midIndex + 1:endIndex + 1]

        leftIndex = 0
        rightIndex = 0
        sortIndex = startIndex

        while leftIndex < len(leftCopy) and rightIndex < len(rightCopy):
            if not left_on(self.pointList[0], rightCopy[rightIndex], leftCopy[leftIndex]):
                self.pointList[sortIndex] = leftCopy[leftIndex]
                leftIndex = leftIndex + 1
            else:
                self.pointList[sortIndex] = rightCopy[rightIndex]
                rightIndex = rightIndex + 1

            sortIndex = sortIndex + 1

        while leftIndex < len(leftCopy):
            self.pointList[sortIndex] = leftCopy[leftIndex]
            leftIndex = leftIndex + 1
            sortIndex = sortIndex + 1

        while rightIndex < len(rightCopy):
            self.pointList[sortIndex] = rightCopy[rightIndex]
            rightIndex = rightIndex + 1
            sortIndex = sortIndex + 1

    def __leftWrap(self, i, j, k):
        return left(self.pointList[i], self.pointList[j], self.pointList[k])

    def __rightWrap(self, i, j, k):
        return not left_on(self.pointList[i], self.pointList[j], self.pointList[k])

    def __hilightSegment(self, initPointIndex, toPointIndex, lineColor="yellow",
                         pointColor="yellow"):
        initPoint = self.pointList[initPointIndex]
        toPoint = self.pointList[toPointIndex]
        lineId = initPoint.lineto(toPoint, lineColor)
        initPointId = initPoint.hilight(pointColor)
        toPointId = toPoint.hilight(pointColor)

        return [lineId, initPointId, toPointId]

    def __unhilightSegment(self, pointSegmentId):
        for plotId in pointSegmentId:
            control.plot_delete(plotId)

    def __hilightLine(self, firstPointIndex, secondPointIndex):
        firstPoint = self.pointList[firstPointIndex]
        secondPoint = self.pointList[secondPointIndex]
        plotId = control.plot_line(firstPoint.x, firstPoint.y, secondPoint.x, secondPoint.y,
                                   color="yellow", linewidth=1)

        return plotId


def main(pointList):
    convexHull = ConvexHull(pointList)
    convexHull.giftWrapping()
    print(convexHull.convexHull)
