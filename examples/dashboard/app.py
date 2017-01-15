#!/usr/bin/python
# -*- coding: utf-8 -*-

import itertools
from flask import Flask, render_template, session, redirect
from werkzeug.contrib.cache import SimpleCache
import gamelocker

import ads
import config

app = Flask(__name__)
app.secret_key = config.secret_key
cache = SimpleCache()


@app.route("/")
def index():
    if "ads" not in session:
        session["ads"] = False
    return render_template("index.html", ads=ads.ads, useads=session["ads"])

@app.route("/ads-toggle")
def adswitch():
    session["ads"] = not session["ads"]
    return redirect("/")

@app.route("/stats.js")
def data():
    data = cache.get("data")
    if data is not None:
        return render_template("stats.js", stats=data)

    data = dict()
    api = gamelocker.Gamelocker("aaa.bbb.ccc").Vainglory()
    data["number"] = config.batchsize
    matches = api.matches(data["number"])

    playersactors = dict()
    gameModes = dict()
    durations = dict()
    players = dict()
    heroes = dict()
    picks = dict()
    sells = dict()
    minions = 0
    potions = 0
    cs = dict()
    boots = 0
    for match in matches:
        if match.gameMode not in gameModes:
            gameModes[match.gameMode] = 0
            durations[match.gameMode] = []
            picks[match.gameMode] = dict()
        gameModes[match.gameMode] += 1
        durations[match.gameMode] += [match.duration/60]

        for roster in match.rosters:
            for participant in roster.participants:
                if participant.player.name not in players:
                    players[participant.player.name] = 0
                players[participant.player.name] += 1

                if participant.actor.pretty() not in picks[match.gameMode]:
                    picks[match.gameMode][participant.actor.pretty()] = 0
                picks[match.gameMode][participant.actor.pretty()] += 1

                if participant.actor.pretty() not in heroes:
                    heroes[participant.actor.pretty()] = 0
                heroes[participant.actor.pretty()] += 1

                # TODO use id instead of name?
                playersactors[participant.player.name] = participant.actor.pretty()
                cs[participant.player.name] = participant.stats.minionKills / match.duration * 60
                minions += participant.stats.minionKills

                for item in participant.stats.items:
                    if item.pretty() in ["Sprint Boots", "Travel Boots", "Journey Boots", "War Treads", "Halcyon Chargers"]:
                        boots += 1

                for item in participant.stats.itemUses:
                    if gamelocker.strings.LazyObject(item).pretty() == "Halcyon Potion":
                        potions += participant.stats.itemUses[item]
                
                for sold in participant.stats.itemSells:
                    item = gamelocker.strings.LazyObject(sold).pretty()
                    if not item in sells:
                        sells[item] = 0
                    sells[item] += participant.stats.itemSells[sold]

    sells = sorted(sells.items(), key=lambda x: x[1], reverse=True)
    data["topsold"] = ", ".join([s[0] for s in sells[0:3]])

    cs = sorted(cs.items(), key=lambda x: x[1], reverse=True)
    data["topcs"] = dict()
    data["topcs"]["player"] = cs[0][0]
    data["topcs"]["cs"] = round(cs[0][1], 2)
    data["topcs"]["actor"] = playersactors[data["topcs"]["player"]]
    
    data["minions"] = minions
    data["boots"] = boots/len(matches)
    data["potions"] = round(60*sum(sum(durations.values(), []))/potions, 2)

    data["gameModes"] = [{"name": k, "y": v} for k, v in gameModes.items()]
    data["durations"] = [{"name": k, "data": list(zip([list(durations.keys()).index(k)]*len(v), v))} for k, v in durations.items()]

    data["picks"] = [{"name": k, "data": list(v.values())} for k, v in picks.items()]
    data["heroes"] = list(heroes.keys())

    players = sorted(players.items(), key=lambda x: x[1], reverse=True)[:5]
    data["players"] = [{"name": k, "data": [v]} for k, v in players]

    cache.set("data", data, timeout=10*60)

    return render_template("stats.js", stats=data)

if __name__ == "__main__":
    app.run(debug=config.debug)
