import sys
import typing
from . import ops
from . import types
from . import app
from . import path
from . import utils
from . import props
from . import context

context: 'types.Context' = None

data: 'types.BlendData' = None
'''Access to Blenders internal data '''
