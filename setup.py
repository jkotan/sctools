#!/usr/bin/env python
#   This file is part of sctools - Scientific Catalog Tools
#
#    Copyright (C) 2021-2021 DESY, Jan Kotanski <jkotan@mail.desy.de>
#
#    nexdatas is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nexdatas is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with sctools.  If not, see <http://www.gnu.org/licenses/>.
#

""" setup.py for command-line sctools """

import os
import sys
from setuptools import setup
# from setuptools.command.build_py import build_py
# from distutils.core import setup
from distutils.core import Command

try:
    from sphinx.setup_command import BuildDoc
except Exception:
    BuildDoc = None


PKG = "sctools"
IPKG = __import__(PKG)

needs_pytest = set(['test']).intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

install_requires = [
    'argcomplete',
    # 'h5py',
    # 'pytz',
    # 'numpy>1.6.0',
    # 'lxml',
    # 'fabio',
    # 'pytango',
    # 'pninexus',
]


def read(fname):
    """reading a file

    :param fname: file name
    :type fname: :obj:`str`
    """
    with open(os.path.join(os.path.dirname(__file__), fname)) as fl:
        return fl.read()


class TestCommand(Command):
    """ test command class
    """

    #: user options
    user_options = []

    #: initializes options
    def initialize_options(self):
        pass

    #: finalizes options
    def finalize_options(self):
        pass

    #: runs command
    def run(self):
        import sys
        import subprocess
        errno = subprocess.call([sys.executable, 'test'])
        raise SystemExit(errno)


release = IPKG.__version__
version = ".".join(release.split(".")[:2])
name = "SCTools"
author = "Jan Kotanski",
glicense = "GNU GENERAL PUBLIC LICENSE, version 3",

#: metadata for distutils
SETUPDATA = dict(
    name="sctools",
    version=IPKG.__version__,
    author=author,
    author_email="jankotan@gmail.com",
    maintainer="Jan Kotanski",
    maintainer_email="jankotan@gmail.com",
    license=glicense,
    description=("Scientific Catalog Tools"),
    keywords="metadata catalog tools metadata photon science",
    url="http://github.com/jkotan/sctools",
    platforms=("Linux"),
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=["sctools"],
    scripts=[
        'scmeta'
    ],
    cmdclass={
        # 'test': TestCommand,
        # 'build_sphinx': BuildDoc
    },
    zip_safe=False,
    setup_requires=pytest_runner,
    # tests_require=['pytest'],
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release)
        }
    },
    long_description=read('README.md'),
    # long_description_content_type='text/x-rst'
)


def main():
    """ the main function
    """
    setup(**SETUPDATA)


if __name__ == '__main__':
    main()
