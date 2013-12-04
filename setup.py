#!/usr/bin/env python
#
# Poker Cards
#
# Python module for working with poker cards and managing games.
#
# Copyright 2013 Michal Belica <devel@beli.sk>
#
# This file is part of Poker Cards.
# 
# Poker Cards is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Poker Cards is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Poker Cards.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup

from pokercards.const import __version__

with open('README.rst') as file:
    long_description = file.read()

setup(name='PokerCards',
        version=__version__,
        author='Michal Belica',
        author_email='devel@beli.sk',
        url='https://github.com/beli-sk/pokercards',
        description='Python module for working with poker cards and managing games.',
        long_description=long_description,
        classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Games/Entertainment',
            ],
        packages=['pokercards'],
        )

