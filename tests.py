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

import random
import unittest
from collections import Counter

from pokercards import cards
from pokercards.logsetup import setup_console_logging, INFO

class TestCard(unittest.TestCase):
    def setUp(self):
        """Create a list of a few cards for testing. Ordered by
descending rank."""
        self.cards = [
                cards.Card('KH'),
                cards.Card('QC'),
                cards.Card('JD'),
                cards.Card('TS'),
                cards.Card('9S'),
                cards.Card('8S'),
                ]

    def test_sort(self):
        """Test sorting of cards by rank"""
        self.cards2 = self.cards[:] # copy list
        random.shuffle(self.cards) # shuffle
        self.cards.sort(reverse=True) # and sort back
        self.assertEqual(self.cards, self.cards2)

    def test_exceptions(self):
        """Test exceptions when creating cards of invalid rank/suit"""
        self.assertRaises(ValueError, cards.Card, 'xH')
        self.assertRaises(ValueError, cards.Card, 'Kx')

class TestDeck(unittest.TestCase):
    def setUp(self):
        """Create a new deck for testing."""
        self.deck = cards.Deck()

    def test_pop(self):
        """Test popping and returning a card"""
        stack = []
        self.deck.shuffle()
        # pop three cards
        stack.append(self.deck.pop())
        stack.append(self.deck.pop())
        stack.append(self.deck.pop())
        # check internal counts
        self.assertEqual(len(self.deck.popped), 3)
        self.assertEqual(len(self.deck.active), 52-3)
        # see if the cards are in popped list
        self.assertEqual(self.deck.popped, stack)
        # return them to top of the deck
        self.deck.return_popped(pos=cards.POS_TOP)
        # check counts again
        self.assertEqual(len(self.deck.popped), 0)
        self.assertEqual(len(self.deck.active), 52)
        # see if the cards really are on top of the deck
        self.assertEqual(self.deck.active[-3:], stack)

    def test_discard(self):
        """Test discarding and returning a card"""
        stack = []
        self.deck.shuffle()
        # discard three cards
        self.deck.discard()
        stack.append(self.deck.discarded[-1])
        self.deck.discard()
        stack.append(self.deck.discarded[-1])
        self.deck.discard()
        stack.append(self.deck.discarded[-1])
        # check internal counts
        self.assertEqual(len(self.deck.discarded), 3)
        self.assertEqual(len(self.deck.active), 52-3)
        # see if the cards are in discarded list
        self.assertEqual(self.deck.discarded, stack)
        # return them to top of the deck
        self.deck.return_discarded(pos=cards.POS_TOP)
        # check counts again
        self.assertEqual(len(self.deck.discarded), 0)
        self.assertEqual(len(self.deck.active), 52)
        # see if the cards really are on top of the deck
        self.assertEqual(self.deck.active[-3:], stack)

class TestHand(unittest.TestCase):
    def setUp(self):
        """Create some hands for testing, along with information on how
they should be evaluated. Ordered in descending strength."""
        self.testhands = [
            {
                'hand': cards.PokerHand(
                    cards.Card.card_list('KC', 'QH', 'JH', 'TH', '9H', '8H', '7H')
                    ),
                'hand_rank': 8, 
                'hand_cards': cards.Card.card_list('QH', 'JH', 'TH', '9H', '8H'),
                'kickers': [],
            },{
                'hand': cards.PokerHand(
                    cards.Card.card_list('7H', 'JS', 'QH', 'JD', 'JC', 'AH', 'JH')
                    ),
                'hand_rank': 7, 
                'hand_cards': cards.Card.card_list('JS', 'JH', 'JD', 'JC'),
                'kickers': [cards.Card('AH')],
            },{
                'hand': cards.PokerHand(
                    cards.Card.card_list('5C', 'AS', '5H', '2H', '5D', 'AC', '7H')
                    ),
                'hand_rank': 6, 
                'hand_cards': cards.Card.card_list('5C', '5H', '5D', 'AS', 'AC'),
                'kickers': [],
            },{
                'hand': cards.PokerHand(
                    cards.Card.card_list('4C', 'AS', '4H', '2H', '4D', '2C', '2H')
                    ),
                'hand_rank': 6, 
                'hand_cards': cards.Card.card_list('4C', '4H', '4D', '2H', '2C'),
                'kickers': [],
            },{
                'hand': cards.PokerHand(
                    cards.Card.card_list('5C', 'AS', '5H', 'KS', '2D', 'KD', '7H')
                    ),
                'hand_rank': 2, 
                'hand_cards': cards.Card.card_list('5C', '5H', 'KS', 'KD'),
                'kickers': cards.Card.card_list('AS'),
            },{
                'hand': cards.PokerHand(
                    cards.Card.card_list('5D', 'QS', '5S', 'KH', '2C', 'KC', '7H')
                    ),
                'hand_rank': 2, 
                'hand_cards': cards.Card.card_list('5D', '5S', 'KH', 'KC'),
                'kickers': cards.Card.card_list('QS'),
            }]

    def test_evaluation(self):
        """Evaluate the testing hands
and compare results to those entered manually"""
        for testhand in self.testhands:
            hand = testhand['hand']
            self.assertEqual(hand.hand_rank, testhand['hand_rank'])
            self.assertEqual(Counter(hand.hand_cards), Counter(testhand['hand_cards']))
            self.assertEqual(Counter(hand.kickers), Counter(testhand['kickers']))

    def test_comparison(self):
        """Test hand comparison and sorting"""
        hands = [x['hand'] for x in self.testhands]
        hands2 = hands[:]
        random.shuffle(hands)
        hands.sort(reverse=True)
        self.assertEqual(hands2, hands)

if __name__ == '__main__':
    setup_console_logging(level=INFO)
    suite = unittest.TestSuite()
    tl = unittest.TestLoader()
    suite.addTests(map(tl.loadTestsFromTestCase, (TestCard, TestDeck, TestHand)))
    unittest.TextTestRunner(verbosity=2).run(suite)

