#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 16:12:02 2017

@author: phypoh

https://github.com/schneefux/python-gamelocker
"""
import gamelocker
from gamelocker.strings import pretty

APIKEY = "aaa.bbb.ccc"
api = gamelocker.Gamelocker(APIKEY).Vainglory()

#player_name = input("Player name?")

player_name = "IraqiZorro"

matches = api.matches({"page[limit]": 10, "filter[playerNames]": player_name})

match = matches[0]

for team in range(2):
    print("\nTeam", team+1)
    for player in range(3):
        name = match.rosters[team].participants[player].player.name
        hero = pretty(match.rosters[team].participants[player].actor)
        kills = match.rosters[team].participants[player].stats["kills"]
        deaths = match.rosters[team].participants[player].stats["deaths"]
        assists = match.rosters[team].participants[player].stats["assists"]
        print(name, hero, kills, '/', deaths,  '/', assists)
