from .convexhull import ConvexHull


def main(pointList):
    convexHull = ConvexHull(pointList)
    convexHull.graham()
    print(convexHull.convexHull)
