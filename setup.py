import os
from typing import List

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(os.path.join(here, "VERSION"), encoding="utf-8") as f:
    __version__ = f.read().strip()
    with open(os.path.join(here, "fitbert", "version.py"), "w+", encoding="utf-8") as v:
        v.write("# CHANGES HERE HAVE NO EFFECT: ../VERSION is the source of truth\n")
        v.write(f'__version__ = "{__version__}"')

requirementPath = os.path.abspath("./requirements.txt")
install_requires: List[str] = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

setup(
    name="fitbert",
    description="Use BERT to Fill in the Blanks",
    packages=find_packages(),
    package_data={"": ["VERSION", "requirements.txt"]},
    data_files=[(".", ["VERSION", "requirements.txt"])],
    include_package_data=True,
    author="Qordoba",
    author_email="sam.havens@qordoba.com",
    url="https://github.com/Qordobacode/fitbert",
    version=__version__,
    license="Apache License 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "Typing :: Typed",
    ],
)
