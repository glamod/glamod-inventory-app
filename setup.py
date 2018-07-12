from setuptools import setup, find_packages

import sys
sys.path.append('glamod_inv_site')

from glamod_inv_site import __version__


def readme():
    with open('README.md') as f:
        return f.read()

def license():
    with open('LICENSE') as f:
        return f.read()


reqs = [line.strip() for line in open('requirements.txt')]
GIT_REPO = "https://github.com/glamod/glamod-inv-site"


setup(
    name                 = "glamod-inv-site",
    version              = __version__,
    description          = "Web-app for GLAMOD inventories.",
    long_description     = readme(),
    license              = license(),
    author               = "Ag Stephens",
    author_email         = "ag.stephens@stfc.ac.uk",
    url                  = GIT_REPO,
    packages             = find_packages(),
    install_requires     = reqs,
    tests_require        = ['pytest'],
    classifiers          = [
        'Development Status :: 2 - ???',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: BSD 3-Clause License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
    ],
    include_package_data = True,
    scripts=[],
    entry_points         = {},
    package_data         = {}
)

