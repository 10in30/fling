"""Core libraries and configuration for fling components"""
__version__ = "0.1.3"

import os
import pathlib
from dotenv import load_dotenv
from dynaconf import Dynaconf
import sys

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points


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


print("Loading plugins...")
discovered_plugins = entry_points(group='fling_core.collect')

for plugin in discovered_plugins:
    print(f"Loading plugin {plugin.name}")
    collect = discovered_plugins[plugin.name].load()
    collect()
