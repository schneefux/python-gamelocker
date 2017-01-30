import gamelocker
APIKEY = "aaa.bbb.ccc" #Default API key.
api = gamelocker.Gamelocker(APIKEY).Vainglory()
def getID(name):
    try:
        m = api.matches({"page[limit]": 2, "filter[playerNames]": name}) #Gets players matches.
        for i in m[0].rosters:
            for j in i.participants:
                if j.player.name == name:
                    return(j.player.id) #Returns  player id
    except:
        return("Invalid Name")
print(getID("CullTheMeek")) #>>> 8627889a-7263-11e4-a296-06d90c28bf1a
print(getID("RandomUsername999")) #>>> "Invalid Name"
