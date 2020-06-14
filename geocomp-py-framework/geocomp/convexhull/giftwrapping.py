from .convexhull import ConvexHull


def main(pointList):
    convexHull = ConvexHull(pointList)
    convexHull.giftWrapping()
    print(convexHull.convexHull)
