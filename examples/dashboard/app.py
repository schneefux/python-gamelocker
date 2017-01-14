#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import json
import gamelocker

app = Flask(__name__)

@app.route("/")
def index():
    api = gamelocker.Gamelocker("aaa.bbb.ccc").vainglory()
    number = 100
    matches = api.matches(number)

    # TODO this, is a mess.
    gameModes = []
    for match in matches:
        gmsuccess = False
        for mode in gameModes:
            if mode["name"] == match.gameMode:
                mode["y"] += 1
                gmsuccess = True
                break
        if gmsuccess == False:
            gameModes.append({"name": match.gameMode, "y": 1})

    players = []
    picks = dict()
    for match in matches:
        for roster in match.rosters:
            for participant in roster.participants:
                # --- player stats
                plsuccess = False
                for player in players:
                    if player["name"] == participant.player.name:
                        player["data"][0] += 1
                        plsuccess = True
                        break
                if plsuccess == False:
                    players.append({"name": participant.player.name, "data": [1]})

                # --- hero stats
                if match.gameMode not in picks:
                    picks[match.gameMode] = dict()
                if participant.actor not in picks[match.gameMode]:
                    picks[match.gameMode][participant.actor] = 0
                picks[match.gameMode][participant.actor] += 1

    for p in picks: # flatten
        heroes = list(picks[p].keys())
        picks[p] = list(picks[p].values())
    new_picks = []
    for k, v in picks.items():
        new_picks.append({"name": k, "data": v})
    picks = new_picks
        
    players = sorted(players, key=lambda k: k["data"][0])
    players = players[:5]

    return render_template("index.html", gameModeNum=number, gameModes=gameModes, players=players, picks=picks, heroes=heroes)

if __name__ == "__main__":
    app.run()
