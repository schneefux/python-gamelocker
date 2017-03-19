#Modified from Github python-gamelocker/examples/kda.py
# __author__: iAm-Kashif

import gamelocker
from gamelocker.strings import pretty

api = gamelocker.Gamelocker(VG_API_Key).Vainglory()

def getPlayerStats(IGN):

    matches = api.matches({"sort": "-createdAt",
                           "filter[playerNames]": IGN,
                           "filter[createdAt-start]": "2017-03-10T00:00:00Z",
                           "page[limit]": "5"})

    matches = sorted(matches, key=lambda d: d.createdAt, reverse=True)

    if (matches == False):
        print ("No Matches found")

    else:
        match = matches[0]
        print('Time Played: ', match.createdAt)
        print('GameMode: ', match.gameMode)
        print('Telemetry: ', match.assets[0].url)

        for team in range(2):
            print("\nTeam", team+1)
            for player in range(3):
                name = match.rosters[team].participants[player].player.name

                hero = pretty(match.rosters[team].participants[player].actor)
                k = match.rosters[team].participants[player].stats["kills"]
                d = match.rosters[team].participants[player].stats["deaths"]
                a = match.rosters[team].participants[player].stats["assists"]
                builds = match.rosters[team].participants[player].stats["items"]
                print (name, hero, k, '/', d, '/', a, '/', builds)


#TestRun
getPlayerStats("Kashz,Coffee1,Shelbii")
