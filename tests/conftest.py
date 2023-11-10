# conftest.py
import os.path
from distutils.dist import Distribution
from pathlib import Path
from Cython.Build import cythonize


def pytest_sessionstart(session):
    path = os.path.abspath('csv_bleach/json_encode.pyx')
    dist = Distribution(attrs={'ext_modules': cythonize(path)})
    build_ext_cmd = dist.get_command_obj('build_ext')
    build_ext_cmd.ensure_finalized()
    build_ext_cmd.inplace = 1
    build_ext_cmd.run()
    session.fib_obj = Path(build_ext_cmd.get_ext_fullpath(path))


def pytest_sessionfinish(session):
    session.fib_obj.unlink()