#!/usr/bin/python
# -*- coding: utf-8 -*-

import itertools
from flask import Flask, render_template, session, redirect
from werkzeug.contrib.cache import SimpleCache
import gamelocker

import ads
import config

app = Flask(__name__)
cache = SimpleCache()


@app.route("/")
def index():
    if "ads" not in session:
        session["ads"] = True
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
    api = gamelocker.Gamelocker("aaa.bbb.ccc").vainglory()
    data["number"] = 50
    matches = api.matches(data["number"])

    gameModes = dict()
    durations = dict()
    players = dict()
    heroes = dict()
    picks = dict()
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

                if participant.actor not in picks[match.gameMode]:
                    picks[match.gameMode][participant.actor] = 0
                picks[match.gameMode][participant.actor] += 1

                if participant.actor not in heroes:
                    heroes[participant.actor] = 0

    data["gameModes"] = [{"name": k, "y": v} for k, v in gameModes.items()]
    data["durations"] = [{"name": k, "data": list(zip([list(durations.keys()).index(k)]*len(v), v))} for k, v in durations.items()]

    data["picks"] = [{"name": k, "data": list(v.values())} for k, v in picks.items()]
    data["heroes"] = list(heroes.keys())

    players = sorted(players.items(), key=lambda x: x[1])[:5]
    data["players"] = [{"name": k, "data": [v]} for k, v in players]

    cache.set("data", data, timeout=10*60)

    return render_template("stats.js", stats=data)

if __name__ == "__main__":
    app.secret_key = config.secret_key
    app.run(debug=config.debug)
