# Author: Ngo Kim Phu
from os.path import dirname, basename
import glob
Scanners = { b[:-7]: getattr(__import__(b, globals(), locals()), b)
    for f in glob.glob(dirname(__file__) + '/*?Scanner.py') for b in [basename(f)[:-3]] }
