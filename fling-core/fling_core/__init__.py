"""Core libraries and configuration for fling components"""
__version__ = "0.1.2"

import os
import pathlib
from dotenv import load_dotenv
from dynaconf import Dynaconf

load_dotenv()

defaults_path = pathlib.Path(os.path.dirname(os.path.abspath(__file__)), 'fling.yaml')
print(defaults_path)
settings = Dynaconf(
    environments=True,
    envvar_prefix="FLING",
    root_path="./",
    preload=[defaults_path],
    settings_files=['fling.yaml', '.secrets.yaml'],
)
