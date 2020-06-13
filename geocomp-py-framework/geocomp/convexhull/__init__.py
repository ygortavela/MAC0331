from . import giftwrapping
from . import graham

children = [('giftwrapping', 'main',
             'Embrulho de Presente'),
            ('graham', 'main',
             'Graham')]

__all__ = [a[0] for a in children]
