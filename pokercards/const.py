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

__version__ = '0.1.0'

suits = ['S', 'H', 'D', 'C']
ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

# throughout this module top/bottom refers to a deck face down on the table
POS_TOP = 0
POS_BOTTOM = 1
