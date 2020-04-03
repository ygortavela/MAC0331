from . import brute_force
from . import sweep_line

children = [('brute_force', 'Brute_force', 'Forca\nBruta'),
            ('sweep_line', 'Sweep_line', 'Linha de\nVarredura')]

__all__ = [a[0] for a in children]
