"""Core libraries and configuration for fling components"""
__version__ = "0.1.0"

import os
import pathlib
from dynaconf import Dynaconf

defaults_path = pathlib.Path(os.path.dirname(os.path.abspath(__file__)), 'fling.yaml')
settings = Dynaconf(
    envvar_prefix="FLING",
    settings_files=[defaults_path, 'fling.yaml', '.secrets.yaml'],
    root_path="./"
)
