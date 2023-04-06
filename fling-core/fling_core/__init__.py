"""Core libraries and configuration for fling components"""
__version__ = "0.1.0"


from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="FLING",
    settings_files=['fling.yaml', '.secrets.yaml'],
)

# `envvar_prefix` = export envvars with `export FLING_FOO=bar`.
# `settings_files` = Load these files in the order.
