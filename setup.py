from distutils.core import setup
from setuptools import find_packages


PACKAGE_NAME = "pypropeller"
PACKAGE_VERSION = "0.1"
AUTHOR = "Johnny Crash"
AUTHOR_EMAIL = "cannon.imus@gmail.com"
URL = "https://github.com/crashmaster/pypropeller"


setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    packages=find_packages()
)
