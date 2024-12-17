from distutils.core import setup
from setuptools import find_packages

print("wtf")
setup(
    name="backtester_lib",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "matplotlib==3.8.2",
        "pandas==2.0.2",
        "ta==0.10.2",
    ],
)
