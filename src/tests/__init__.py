from os.path import dirname, basename, isfile, join
import glob
from pathlib import Path

modules = list(Path(__file__).parent.parent.joinpath('gerg_plotting','examples').rglob('*.py'))
modules = [str(module) for module in modules]
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
