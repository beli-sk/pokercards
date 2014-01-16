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
:mod:`pokercards.cards` -- Represent cards, decks and hands
===========================================================
"""

import random
import logging
from collections import OrderedDict

from const import __version__, suits, ranks, POS_TOP, POS_BOTTOM

logger = logging.getLogger(__name__)

def f_list(lst, sep=','):
    return sep.join([str(x) for x in lst])

def f_lists(lst, sep=' / '):
    return f_list(map(f_list, lst), sep)

class Card(object):
    """Represents a single french-design card with it's rank and suit.

    Cards can be compared and ordered by rank. A card, relative to
    a card of the same rank but different suit, is compared as neither
    higher, lower nor equal.

    :param rank: Either the rank (one of 'A', 'K', 'Q', 'J', 'T', '9', ... '2')
       or rank and suit together (e.g. 'AS', '8H', etc.)
    :type rank: str
    :param suit: The suit, if not given as one string with rank
       (one of 'S', 'H', 'C', 'D' for spade, heart, club or diamond)
    :type suit: str
    :raises: ValueError
    """

    def __init__(self, rank, suit=None):
        if suit is None:
            suit = rank[1]
            rank = rank[0]
        if rank not in ranks:
            raise ValueError('Card(): Invalid rank')
        if suit not in suits:
            raise ValueError('Card(): Invalid suit')
        self.rank = rank
        self.suit = suit

    @classmethod
    def card_list(cls, *args):
        """Create a list of new cards.

        Each argument should describe one card with rank and suit together.

        :param args: One or more cards.
        :type rank: str
        :returns: List of new cards, one for each input parameter.
        :rtype: list of :class:`pokercards.cards.Card` objects
        :raises: ValueError
        """
        lst = []
        for c in args:
            lst.append(cls(c))
        return lst

    def __str__(self):
        return self.rank + self.suit

    def __repr__(self):
        return 'Card(%s, %s)' % (self.rank, self.suit)

    def __hash__(self):
        return (ord(self.rank) << 8) + ord(self.suit)

    def __eq__(self, obj):
        return self.rank == obj.rank and self.suit == obj.suit

    def __ne__(self, obj):
        return self.rank != obj.rank or self.suit != obj.suit

    def __lt__(self, obj):
        return ranks.index(self.rank) > ranks.index(obj.rank)

    def __gt__(self, obj):
        return ranks.index(self.rank) < ranks.index(obj.rank)

    def __le__(self, obj):
        return ranks.index(self.rank) >= ranks.index(obj.rank)

    def __ge__(self, obj):
        return ranks.index(self.rank) <= ranks.index(obj.rank)

class Deck(object):
    """Represents a single deck of 52 :class:`card.Card` objects.

    The deck could be imagined face down on a table. All internal lists
    represent the cards in order from bottom up. So dealing the top
    card means poping last item from the list.
    """
    def __init__(self):
        self.popped = []
        self.discarded = []
        self.active = []
        for s in suits:
            for r in ranks:
                self.active.append(Card(r, s))

    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.active)

    def pop(self):
        """Deal the top card from the deck.

        :returns: :class:`pokercards.cards.Card` instance
        """
        card = self.active.pop()
        self.popped.append(card)
        return card

    def discard(self):
        card = self.active.pop()
        self.discarded.append(card)

    def return_cards(self, cards, pos = POS_BOTTOM):
        if pos not in (POS_BOTTOM, POS_TOP):
            raise Exception('Deck.return_cards(): invalid pos parameter')

        for card in cards[:]:
            if card in self.discarded:
                self.discarded.remove(card)
            elif card in self.popped:
                self.popped.remove(card)
            else:
                raise Exception('Deck.return_cards(): card not among removed cards')

            if pos == POS_BOTTOM:
                self.active[0:0] = [card]
            else:
                self.active.append(card)

    def return_discarded(self, pos = POS_BOTTOM):
        self.return_cards(self.discarded, pos)

    def return_popped(self, pos = POS_BOTTOM):
        self.return_cards(self.popped, pos)

    def return_all(self, pos = POS_BOTTOM):
        self.return_popped()
        self.return_discarded()

    def stats(self):
        return (len(self.active), len(self.popped), len(self.discarded))

    def __str__(self):
        return '[%s]' % ' '.join((str(card) for card in self.active))

    def __repr__(self):
        return 'Deck(%s)' % self.__str__()

class PokerHand(object):
    """Compute the best hand from given cards, implementing traditional
    "high" poker hand ranks.

    The hand object can be given more than five cards (as in Texas
    Hold'em or similar variants) and the evaluation will pick the best
    hand.

    Evaluated :class:`pokercards.cards.PokerHand` objects are
    compared and sorted by the rank of the hand.

    .. attribute:: cards

       List of :class:`pokercards.cards.Card` objects to make the hand
       from. The :meth:`pokercards.cards.PokerHand.evaluate` method
       should be called after manual update to re-evaluate the updated
       hand.

    Following attributes are available after evaluating the hand.

    .. attribute:: hand_rank

       Readonly rank of the hand (0 = high card to 8 = straight flush)

    .. attribute:: hand_cards

       Readonly list of cards which complete the rank.

    .. attribute:: kickers

       Readonly list of extra cards which can break a tie.

    :param cards: List of :class:`pokercards.cards.Card` objects.
    :param evaluate: Evaluate the hand when creating.
    :type evaluate: bool
    """

    def __init__(self, cards, evaluate=True):
        cards.sort(reverse=True)
        self.cards = cards
        if evaluate:
            self.evaluate()

    def evaluate(self):
        """Evaluate the rank of the hand.

        Should be called either implicitly at start by leaving
        parameter ``evaluate`` True when creating the hand or
        explicitly by calling this method later, e.g. after changing
        the :attr:`cards` attribute manually.
        """
        self._eval_hand_rank()
        self._fill_kickers()

    def _by_rank(self, cards=None):
        if cards is None:
            cards = self.cards
        ranked = OrderedDict()
        for card in cards:
            if card.rank in ranked:
                ranked[card.rank].append(card)
            else:
                ranked[card.rank] = [card]
        return ranked

    def _by_suit(self, cards=None):
        if cards is None:
            cards = self.cards
        suited = OrderedDict()
        for card in cards:
            if card.suit in suited:
                suited[card.suit].append(card)
            else:
                suited[card.suit] = [card]
        return suited

    def _find_flushes(self, cards=None):
        if cards is None:
            cards = self.cards
        flushes = []
        for cards in self._by_suit(cards).values():
            l = len(cards)
            if l >= 5:
                for i in xrange(0, l - 4):
                    flushes.append(cards[i:i+5])
        return flushes

    def _find_straights(self, cards=None):
        if cards is None:
            cards = self.cards
        straights = []
        for i in xrange(0, len(cards) - 4):
            card_ranks = [c.rank for c in cards[i:i+5]]
            j = ranks.index(card_ranks[0])
            if card_ranks == ranks[j:j+5]:
                straights.append(cards[i:i+5])
        return straights

    def _fill_kickers(self):
        hand_count = len(self.hand_cards)
        kicker_count = 5 - hand_count
        if kicker_count > 0:
            kickers = self.cards[:]
            for card in self.hand_cards:
                kickers.remove(card)
            self.kickers = kickers[:kicker_count]
        else:
            self.kickers = []
        logger.debug("kickers: %s", f_list(self.kickers))
        logger.debug("--- -------------- ---")

    def _eval_hand_rank(self):
        logger.debug("--- Evaluating %s ---", f_list(self.cards))
        straights = self._find_straights()
        if straights: logger.debug( "straights: %s", f_lists(straights))
        flushes = self._find_flushes()
        if flushes: logger.debug("flushes: %s", f_lists(flushes))
        pairs = []
        threes = []
        fours = []
        for cards in self._by_rank().values():
            l = len(cards)
            if l >= 4:
                fours.append(cards[0:4])
            elif l == 3:
                threes.append(cards)
            elif l == 2:
                pairs.append(cards)
        if pairs: logger.debug("pairs: %s", f_lists(pairs))
        if threes: logger.debug("threes: %s", f_lists(threes))
        if fours: logger.debug("fours: %s", f_lists(fours))
        # straight flush
        for cards in straights:
            if cards in flushes:
                self.hand_rank = 8
                self.hand_cards = cards
                logger.debug("* straight flush: %s", f_list(self.hand_cards))
                return
        # four of a kind
        if len(fours) > 0:
            self.hand_rank = 7
            self.hand_cards = fours[0]
            logger.debug("* four of a kind: %s", f_list(self.hand_cards))
            return
        # full house
        if len(threes) > 1:
            self.hand_rank = 6
            self.hand_cards = threes[0] + threes[1][:2]
            logger.debug("* full house: %s", f_list(self.hand_cards))
            return
        elif len(threes) == 1 and len(pairs) > 0:
            self.hand_rank = 6
            self.hand_cards = threes[0] + pairs[0]
            logger.debug("* full house: %s", f_list(self.hand_cards))
            return
        # flush
        if len(flushes) > 0:
            self.hand_rank = 5
            self.hand_cards = flushes[0]
            logger.debug("* flush: %s", f_list(self.hand_cards))
            return
        # straight
        if len(straights) > 0:
            self.hand_rank = 4
            self.hand_cards = straights[0]
            logger.debug("* straight: %s", f_list(self.hand_cards))
            return
        # three of a kind
        if len(threes) > 0:
            self.hand_rank = 3
            self.hand_cards = threes[0]
            logger.debug("* three of a kind: %s", f_list(self.hand_cards))
            return
        # two pair
        if len(pairs) > 1:
            self.hand_rank = 2
            self.hand_cards = pairs[0] + pairs[1]
            logger.debug("* two pairs: %s", f_list(self.hand_cards))
            return
        # one pair
        if len(pairs) == 1:
            self.hand_rank = 1
            self.hand_cards = pairs[0];
            logger.debug("* two of a kind: %s", f_list(self.hand_cards))
            return
        # high card
        self.hand_rank = 0
        self.hand_cards = [self.cards[0]]
        logger.debug("* high card: %s", f_list(self.hand_cards))

    def __str__(self):
        return '[%s]' % f_list(self.cards)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.__str__())

    def __cmp__(self, other):
        if self.hand_rank > other.hand_rank:
            return 1
        elif self.hand_rank < other.hand_rank:
            return -1
        else:
            # same rank
            for c1, c2 in zip(self.hand_cards, other.hand_cards):
                if c1 > c2:
                    return 1
                elif c1 < c2:
                    return -1
            else:
                # same cards, check kickers
                for c1, c2 in zip(self.kickers, other.kickers):
                    if c1 > c2:
                        return 1
                    elif c1 < c2:
                        return -1
            # really, a tie
            return 0
