from geocomp.common.prim import left, left_on, collinear, dist2
from geocomp.common import control
from geocomp import config


class ConvexHull():
    def __init__(self, pointList):
        self.convexHull = []
        self.pointList = pointList
        self.pointListSize = len(pointList)

        if self.pointListSize < 3:
            for pointIndex in range(self.pointListSize):
                self.convexHull.append(pointIndex)

            if self.pointListSize == 2:
                self.__hilightSegment(
                    0, 1, lineColor="cyan", pointColor="cyan")

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
                        self.convexHull[-1], index, lineWidth=1))

                if self.__rightWrap(self.convexHull[-1], nextHullPointIndex, index):
                    nextHullPointIndex = index
                    self.__unhilightSegment(minIndexPlotId)
                    minIndexPlotId = self.__hilightSegment(
                        self.convexHull[-1], index, lineColor="green", pointColor="green")
                elif self.__collinearWrap(self.convexHull[-1], nextHullPointIndex, index):
                    if self.__distanceWrap(self.convexHull[-1], nextHullPointIndex) < self.__distanceWrap(self.convexHull[-1], index):
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

            if nextHullPointIndex != firstHullPointIndex:
                self.convexHull.append(nextHullPointIndex)
                control.sleep()

    def graham(self):
        if len(self.convexHull) > 0:
            return

        self.__sortPointList()
        self.convexHull = [0, 1, 2]
        hullSegmentIdList = []
        hullSize = len(self.convexHull)

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

            while self.__rightOnWrap(self.convexHull[-2], self.convexHull[-1], pointIndex) and\
                    len(self.convexHull) > 2:
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

    def __sortPointList(self):
        hullPointIndex = self.__getExtremePoint(reverseCoordinate=True)
        self.pointList[0], self.pointList[hullPointIndex] = self.pointList[hullPointIndex], self.pointList[0]
        self.__mergeSortPointList()

    def __getExtremePoint(self, reverseCoordinate=False):
        extremeIndex = 0
        def coordinateKey(k): return k.x
        def reverseCoordinateKey(k): return k.y

        if reverseCoordinate:
            coordinateKey, reverseCoordinateKey = reverseCoordinateKey, coordinateKey

        for index in range(1, self.pointListSize):
            if coordinateKey(self.pointList[index]) < coordinateKey(self.pointList[extremeIndex]):
                extremeIndex = index
            elif coordinateKey(self.pointList[index]) == coordinateKey(self.pointList[extremeIndex]):
                if reverseCoordinateKey(self.pointList[index]) < reverseCoordinateKey(self.pointList[extremeIndex]):
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
            elif collinear(self.pointList[0], leftCopy[leftIndex], rightCopy[rightIndex]):
                if dist2(self.pointList[0], leftCopy[leftIndex]) < dist2(self.pointList[0], rightCopy[rightIndex]):
                    self.pointList[sortIndex] = leftCopy[leftIndex]
                    leftIndex = leftIndex + 1
                else:
                    self.pointList[sortIndex] = rightCopy[rightIndex]
                    rightIndex = rightIndex + 1
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

    def __rightWrap(self, i, j, k):
        return not left_on(self.pointList[i], self.pointList[j], self.pointList[k])

    def __rightOnWrap(self, i, j, k):
        return not left(self.pointList[i], self.pointList[j], self.pointList[k])

    def __collinearWrap(self, i, j, k):
        return collinear(self.pointList[i], self.pointList[j], self.pointList[k])

    def __distanceWrap(self, i, j):
        return dist2(self.pointList[i], self.pointList[j])

    def __hilightSegment(self, initPointIndex, toPointIndex, lineColor="yellow",
                         pointColor="yellow", lineWidth=2):
        initPoint = self.pointList[initPointIndex]
        toPoint = self.pointList[toPointIndex]
        lineId = control.plot_segment(
            initPoint.x, initPoint.y, toPoint.x, toPoint.y, lineColor, lineWidth)
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
