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

"""
:mod:`pokercards.games` -- Poker game
=====================================

Manage game flow, betting rules, dealing cards, etc.

"""

import cards

class BaseGame(object):
    """Base game class. No functionality, used only for subclassing."""
    pass

class TexasGame(object):
    """Iplements Texas Hold'em Poker variant"""
    # TODO
    pass
