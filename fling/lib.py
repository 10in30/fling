"""Main libraries for side project management"""

import os
import shutil
import pyyaml
from dotenv import loadenv

loadenv()

BOILERPLATEDIR = os.environ.get("BOILERPLATEDIR", "boilerplate")  # JMC: TODO: map to installed directory or relative to this file

class FlingConfig:
    config: object = {}
    config_path: str = None

    def __init__(self, config_path='flask.yaml'):
        self.config_path = config_path
        self.load()

    def load(self):
        if not os.path.exists(self.config_path):
            shutil.copyfile(f"{BOILERPLATEDIR}/fling.yaml", self.config_path)
        with open(self.config_path, "r+") as config_file:
            self.config = pyyaml.loads(config_file.read())

    def write(self):
        with open(self.config_path, "w+") as config_file:
            config_file.write(pyyaml.dumps(self.config))
