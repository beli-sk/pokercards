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

class Player(object):
    def __init__(self, index=None):
        self.index = index
        self.all_in = False
        self.bet = 0

ACT_FOLD = 0
ACT_CALL = 1 # check/call
ACT_RAISE = 2 # bet/raise

class BaseGame(object):
    """Base game class. No functionality, used only for subclassing."""
    pass


class TexasGame(BaseGame):
    """Implements Texas Hold'em Poker variant"""
    def __init__(self, num_players, dealer, bigblind):
        self.bigblind = bigblind
        self.deck = Cards.Deck()
        self.num_players = num_players
        self.players = [Player(index=i) for i in xrange(self.num_players)]
        self.com_cards = []
        self.dealer = dealer
        self.players[dealer].dealer = True
        self.current_bet = 0 # current round bet (all players should call to this amount)
        self.pot = 0
        self.turn = dealer

    def action(self, action, amount):
        raise NotImplemented()
        
