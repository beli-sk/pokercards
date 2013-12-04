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

import logging
from logging import DEBUG, INFO, WARNING, ERROR

from const import __version__

"""Convenience functions for setting up simple logging scenarios."""

def setup_server_logging(name='', logfile='', maxBytes=524288, backupCount=1, level=logging.DEBUG,
        fmt='%(asctime)s %(name)s %(levelname)s %(message)s'):
    logger = logging.getLogger('')
    logger.setLevel(level)
    ch = logging.handlers.RotatingFileHandler(logfile, maxBytes, backupCount)
    ch.setLevel(level)
    formatter = logging.Formatter(fmt)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def setup_console_logging(name='', level=logging.DEBUG,
        fmt='%(name)s %(levelname)s %(message)s'):
    """Convenience function for setting up simple logging to console."""
    logger = logging.getLogger('')
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter(fmt)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

