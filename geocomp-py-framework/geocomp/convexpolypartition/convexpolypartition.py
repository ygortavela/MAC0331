from geocomp.triangulation import triangulation


def convexpolypartition(p):
    triang = triangulation.Triangulation(p)
    diagonalList = triang.diagonalList

    print('Diagonal List:')
    print(diagonalList)
    print('dahora')
