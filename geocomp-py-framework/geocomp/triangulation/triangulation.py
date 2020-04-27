from geocomp.common import point
from geocomp.common import segment
from geocomp.common import polygon
from geocomp.common import control
from geocomp import config
from .utils import dcel


def triangulation(p):
    test = dcel.DCEL(p[0].vertices())
