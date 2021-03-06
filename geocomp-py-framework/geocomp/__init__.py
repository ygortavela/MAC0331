# -*- coding: utf-8 -*-

"""Algoritmos de Geometria Computacional

Sub-modulos:
- closest: algoritmos para encontar o par de pontos mais próximo
- lineintersections: algoritmos para encontrar todas as intersecções de segmentos

- common:     classes e operacoes usadas por diversos algoritmos
- gui:        implementacoes das operacoes graficas
"""

from . import lineintersections
from . import triangulation
from . import convexpolypartition
from . import convexhull
from .common.guicontrol import init_display
from .common.guicontrol import plot_input
from .common.guicontrol import run_algorithm
from .common.prim import get_count
from .common.prim import reset_count

children = (('lineintersections',  None, 'Detecção de interseção de segmentos - Ygor Tavela'),
            ('triangulation', None, 'Triangulação de Polígonos - Ygor Tavela'),
            ('convexpolypartition', None,
             'Partição de Polígonos Convexos - Rogério Fernandes & Ygor Tavela'),
            ('convexhull', None, 'Algoritmos de Fecho Convexo - Ygor Tavela')
            )

__all__ = [p[0] for p in children]
