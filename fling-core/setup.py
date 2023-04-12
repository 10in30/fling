# -*- coding: utf-8 -*-
from distutils.core import setup

packages = ["fling_core"]

package_data = {"": ["*"]}

install_requires = ["dynaconf>=3.1.12,<4.0.0", "python-dotenv>=1.0.0,<2.0.0"]

setup_kwargs = {
    "name": "fling-core",
    "version": "0.1.0",
    "description": "Fling core components for Side Project Management",
    "long_description": "",
    "author": "Joshua McKenty and Anouk Ruhaak",
    "author_email": "jmckenty@gmail.com",
    "url": None,
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "python_requires": ">=3.9,<4.0",
}


setup(**setup_kwargs)
