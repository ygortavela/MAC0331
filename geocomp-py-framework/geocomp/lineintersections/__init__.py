from . import brute_force
from . import sweep_line

children = [('sweep_line', 'sweep_line', 'Linha de\nVarredura')]

__all__ = [a[0] for a in children]
