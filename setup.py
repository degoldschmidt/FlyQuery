import os
from setuptools import setup
import distutils.util

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="flyquery",
    version="0.9",
    author="Dennis Goldschmidt",
    author_email="dennis.goldschmidt@neuro.fchampalimaud.org",
    description=("FlyQuery API to read out Google Sheets, query FlyBase stock numbers, and write FlyBase data back into Sheets."),
    license="GPLv3",
    keywords=[],
    url="",
    packages=['flyquery'],
    python_requires='>=3.6',
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.9",
    ],
    platforms=['Windows10Pro', 'MacOSX-BigSur'],
    install_requires=['pygsheets', 'requests', 'bs4', 'pandas', 'numpy'],
    entry_points={'console_scripts': [
            'flyquery = flyquery.main:main',
        ],
    },
)
