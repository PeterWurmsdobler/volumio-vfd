import os
import string

from setuptools import find_packages, setup

NAME = "volumio_vfd"
__version__ = None

repository_dir = os.path.dirname(__file__)

with open(os.path.join(repository_dir, "src", NAME, "_version.py")) as fh:
    exec(fh.read())

with open(os.path.join(repository_dir, "README.md")) as fh:
    long_description = fh.read()

with open(os.path.join(repository_dir, "requirements.txt")) as fh:
    REQUIREMENTS = [line for line in fh.readlines() if line.startswith(tuple(list(string.ascii_letters)))]


setup(
    description="Volumio VFD client",
    author="Peter Wurmsdobler",
    author_email="peter@wurmsdobler.org",
    url="https://github.com/PeterWurmsdobler/volumio-vfd.git",
    include_package_data=True,
    install_requires=REQUIREMENTS,
    long_description=long_description,
    name=NAME,
    package_dir={"": "src"},
    packages=find_packages("src"),
    version=__version__,
)
