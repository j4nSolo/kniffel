from os.path import dirname, basename, isfile, splitext
import glob
modules = glob.glob(dirname(__file__)+"/*.pyc")
__all__ = [splitext(basename(f))[0] for f in modules if isfile(f)]
