# py-quickbase - Python bindings for Intuit's QuickBase
# Copyright (C) 2012-2014 WesTower Communications
# Copyright (C) 2014-2015 MasTec
#
# This file is part of py-quickbase.
#
# py-quickbase is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

from setuptools import setup
import platform

version = '1.0.0'
packages = [
        'quickbase',
        ]
install_requires = [
        'setuptools',
        'BeautifulSoup4 >= 4.0.0',
        'lxml',
        ]

setup(
    name='py-quickbase',
    version=version,
    packages=packages,
    license='LGPL',
    url='http://www.mastec.com/',
    author='Bob Uhl',
    author_email='robert.uhl@mastec.com',
    install_requires=install_requires,
    )
