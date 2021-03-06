#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
BoardGameGeek.com interface for pyprototypr
"""
# future
from __future__ import division
# lib
# third party
from boardgamegeek import BoardGameGeek


class BGGGameList(object):
    """Lists which are groups of multiple games' string-based properties."""

    def __init__(self):
        """create empty lists to hold values"""
        self.alternative_names = []
        self.artists = []
        self.average = []
        self.averageweight = []
        self.bayesaverage = []
        self.categories = []
        self.description = []
        self.designers = []
        self.expands = []
        self.expansion = []
        self.expansions = []
        self.families = []
        self.id = []
        self.image = []
        self.implementations = []
        self.maxplayers = []
        self.mechanics = []
        self.median = []
        self.minage = []
        self.minplayers = []
        self.name = []
        self.numcomments = []
        self.numweights = []
        self.owned = []
        self.playingtime = []
        self.publishers = []
        self.ranks = []
        self.stddev = []
        self.thumbnail = []
        self.trading = []
        self.usersrated = []
        self.wanting = []
        self.wishing = []
        self.yearpublished = []
        # custom fields
        self.players = []
        self.description_short = []
        self.age = []

    def set_values(self, game):
        """Append a game's property to a matching list."""
        self._game = game  # BGGGame object
        if self._game:
            self.alternative_names.append(self._game.alternative_names)
            self.artists.append(self._game.artists)
            self.average.append(self._game.average)
            self.averageweight.append(self._game.averageweight)
            self.bayesaverage.append(self._game.bayesaverage)
            self.categories.append(self._game.categories)
            self.description.append(self._game.description)
            self.designers.append(self._game.designers)
            self.expands.append(self._game.expands)
            self.expansion.append(self._game.expansion)
            self.expansions.append(self._game.expansions)
            self.families.append(self._game.families)
            self.id.append(self._game.id)
            self.image.append(self._game.image)
            self.implementations.append(self._game.implementations)
            self.maxplayers.append(self._game.maxplayers)
            self.mechanics.append(self._game.mechanics)
            self.median.append(self._game.median)
            self.minage.append(self._game.minage)
            self.minplayers.append(self._game.minplayers)
            self.name.append(self._game.name)
            self.numcomments.append(self._game.numcomments)
            self.numweights.append(self._game.numweights)
            self.owned.append(self._game.owned)
            self.playingtime.append(self._game.playingtime)
            self.publishers.append(self._game.publishers)
            self.ranks.append(self._game.ranks)
            self.stddev.append(self._game.stddev)
            self.thumbnail.append(self._game.thumbnail)
            self.trading.append(self._game.trading)
            self.usersrated.append(self._game.usersrated)
            self.wanting.append(self._game.wanting)
            self.wishing.append(self._game.wishing)
            self.yearpublished.append(self._game.yearpublished)
            # custom fields
            self.players.append(self._game.players)
            self.description_short.append(self._game.description_short)
            self.age.append(self._game.age)


class BGGGame(object):
    """Wrapper around the `game` object from boardgamegeek.api"""

    def __init__(self, game_id, short=500):
        """
        Args:
            short: int
                number of characters to use for short description
        """
        #try:
        self._game = None
        self.short = int(short) or 500
        self.bgg = BoardGameGeek()
        if isinstance(game_id, int):
            self._game = self.bgg.game(game_id=game_id)
        elif isinstance(game_id, ""):
            self._game = self.bgg.game(name=game_id)
        else:
            pass
        self.set_properties()
        #except Exception as err:
        #    log.error('Unable to create game:%s (%s)', game_id, err)

    def get_description_short(self):
        """Create an abbreviated description for a game."""
        if self._game:
            desc = self._game.description[0:self.short]
            _cut = int(
                (len(desc) -
                 len(desc.replace(',', '').replace('.', '').replace(':', '')))
                / 2 + self.short)
            desc = self._game.description[0:_cut]
            return desc[0:-3] + '...'

    def set_properties(self):
        """Create both raw (_ prefix) and string formatted versions of props"""
        if self._game:
            self._alternative_names = self._game.alternative_names
            self.alternative_names = ', '.join(self._game.alternative_names)
            self._artists = self._game.artists
            self.artists = ', '.join(self._game.artists)
            self._average = self._game.average
            self.average = '%.3f' % self._game.average
            self._averageweight = self._game.averageweight
            self.averageweight = '%.3f' % self._game.averageweight
            self._bayesaverage = self._game.bayesaverage
            self.bayesaverage = '%.3f' % self._game.bayesaverage
            self._categories = self._game.categories
            self.categories = ', '.join(self._game.categories)
            self._description = self._game.description
            self.description = '%s' % self._game.description
            self._designers = self._game.designers
            self.designers = ', '.join(self._game.designers)
            self._expands = self._game.expands
            self.expands = ', '.join(self._game.expands)
            self._expansion = self._game.expansion
            if self._game.expansion is True:
                self.expansion = 'Yes'
            else:
                self.expansion = 'False'
            self._expansions = self._game.expansions
            self.expansions = ', '.join(self._game.expansions)
            self._families = self._game.families
            self.families = ', '.join(self._game.families)
            self._id = self._game.id
            self.id = '%s' % self._game.id
            self._image = self._game.image
            self.image = '%s' % self._game.image
            self._implementations = self._game.implementations
            self.implementations = ', '.join(self._game.implementations)
            self._maxplayers = self._game.maxplayers
            self.maxplayers = '%s' % self._game.maxplayers
            self._mechanics = self._game.mechanics
            self.mechanics = ', '.join(self._game.mechanics)
            self._median = self._game.median
            self.median = '%.3f' % self._game.median
            self._minage = self._game.minage
            self.minage = '%s' % self._game.minage
            self._minplayers = self._game.minplayers
            self.minplayers = '%s' % self._game.minplayers
            self._name = self._game.name
            self.name = '%s' % self._game.name
            self._numcomments = self._game.numcomments
            self.numcomments = '%s' % self._game.numcomments
            self._numweights = self._game.numweights
            self.numweights = '%s' % self._game.numweights
            self._owned = self._game.owned
            self.owned = '%s' % self._game.owned
            self._playingtime = self._game.playingtime
            self.playingtime = '%s' % self._game.playingtime
            self._publishers = self._game.publishers
            self.publishers = ', '.join(self._game.publishers)
            self._ranks = self._game.ranks
            self.ranks = '%s' % self._game.ranks
            self._stddev = self._game.stddev
            self.stddev = '%.3f' % self._game.stddev
            self._thumbnail = self._game.thumbnail
            self.thumbnail = '%s' % self._game.thumbnail
            self._trading = self._game.trading
            self.trading = '%s' % self._game.trading
            self._usersrated = self._game.usersrated
            self.usersrated = '%s' % self._game.usersrated
            self._wanting = self._game.wanting
            self.wanting = '%s' % self._game.wanting
            self._wishing = self._game.wishing
            self.wishing = '%s' % self._game.wishing
            self._yearpublished = self._game.yearpublished
            self.yearpublished = '%s' % self._game.yearpublished
            # custom fields
            self.description_short = self.get_description_short()
            self._description_short = self.description_short
            if self._game.minplayers == self._game.maxplayers:
                    self.players = '%s' % self._game.maxplayers
            else:
                self.players = '%s-%s' % (self._game.minplayers,
                                          self._game.maxplayers)
            self._players = (self._game.minplayers, self._game.maxplayers)
            self.age = '%s+' % self._game.minage
            self._age = self._game.minage

