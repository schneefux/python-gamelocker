#!/usrz/bin/python

#
#How to access Telemetry using python - gamelocker#
#
import gamelocker
vgApiKey = ''
api = gamelocker.Gamelocker(vgApiKey).Vainglory()


# Get telemetry URL for a particular match played by IGN.
def getTelemetryInfo(IGN):
    try:
        matches = api.matches({
            "sort": "-createdAt",
            "filter[playerNames]": IGN,
            "filter[createdAt-start]": "2017-03-10T00:00:00Z",
            "page[limit]": "1"
        })

        if (matches == False):
            print("No Matches found")
        else :
            match = matches[0]
        print('Time Played: ', match.createdAt)
        print('GameMode: ', match.gameMode)
        print(match.assets[0].name, match.assets[0].url)
    except:
        print("Invalid Name")

getTelemetryInfo("IGN")