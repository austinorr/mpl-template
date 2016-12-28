# Setup script for the template package
#
# Usage: python setup.py install

import os
from setuptools import setup, find_packages


DESCRIPTION = "mpl-template: matplotlib report template constructor"
LONG_DESCRIPTION = DESCRIPTION
NAME = "template"
VERSION = "0.2.1"
AUTHOR = "Austin Orr (Geosyntec Consultants)"
AUTHOR_EMAIL = "aorr@geosyntec.com"
URL = "https://github.com/austinorr"
DOWNLOAD_URL = "https://github.com/austinorr/mpl-template.git"
LICENSE = "BSD 3-clause"
PACKAGES = find_packages()
PLATFORMS = "Python 2.7, 3.4 and later."
CLASSIFIERS = [
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Intended Audience :: Science/Research",
    "Topic :: Software Development :: Libraries :: Python Modules",
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
]
INSTALL_REQUIRES = ['numpy', 'matplotlib', 'pillow', 'pytest']
PACKAGE_DATA = {
    'template.tests.baseline_images': ['*png'],
    'template.tests.img': ['*png'],
}

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    download_url=DOWNLOAD_URL,
    license=LICENSE,
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    platforms=PLATFORMS,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    zip_safe=False,
)
