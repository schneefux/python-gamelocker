#!/usr/bin/python

import gamelocker

def getID(name):
    api = gamelocker.Gamelocker("aaa.bbb.ccc").Vainglory()
    m = api.matches({"page[limit]": 1, "filter[playerNames]": name})
    for i in m[0].rosters:
        for j in i.participants:
            if j.player.name == name:
                return (j.player.id)

print(getID("bigdog1129"))
