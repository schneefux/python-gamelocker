#!/usr/bin/python

import os
import pytest
import requests
import gamelocker
import datetime

class TestGamelocker:
    @pytest.fixture
    def api(self):
        return gamelocker.Gamelocker(os.environ["GAMELOCKER_APIKEY"]).Vainglory()

    def test_req(self, api):
        with pytest.raises(requests.exceptions.HTTPError):
            assert api._req("foobar")
        assert type(api._req("status")) is dict

        assert api.status()["data"]["attributes"]["version"]

    def test_map(self):
        assert gamelocker.datatypes.modulemap()["match"] is gamelocker.datatypes.Match

    def test_match(self, api):
        match = api.match("0955b904-fb19-11e6-802d-0667892d829e")
        assert isinstance(match.gameMode, str)
        assert isinstance(match.rosters[0], gamelocker.datatypes.Roster)
        assert isinstance(match.rosters[0].participants[0], gamelocker.datatypes.Participant)
        assert isinstance(match.rosters[0].participants[0].player, gamelocker.datatypes.Player)
        assert isinstance(match.rosters[0].participants[0].player.name, str)
        assert isinstance(match.rosters[0].participants[0].actor, str)
        assert isinstance(match.rosters[0].stats["acesEarned"], int)
        assert isinstance(match.rosters[0].participants[0].stats["items"][0], str)

    def test_matches(self, api):
        matches = api.matches(params={
           "filter[createdAt-start]": "2017-02-12T00:00:00Z",
           "filter[playerNames]": "Kraken"
        })
        assert len(matches) > 0
        assert isinstance(matches[0], gamelocker.datatypes.Match)
        assert matches[0].duration > 0

    def test_asset(self, api):
        match = api.match(elid="f73274b2-0a7f-11e7-a28f-0206eb3a2f5b",
                          region="eu")
        assert isinstance(match.assets[0].url, str)

    def test_region(self, api):
        assert len(api.matches(region="na",
                               params={
                                   "filter[createdAt-start]": "2017-02-12T00:00:00Z",
                                   "filter[playerNames]": "Kraken"
                               })) > 0
        assert len(api.matches(region="eu",
                               params={
                                   "filter[createdAt-start]": "2017-02-12T00:00:00Z",
                                   "filter[playerNames]": "shutterfly"
                               })) > 0
        assert len(api.matches(region="sg",
                               params={
                                   "filter[createdAt-start]": "2017-02-12T00:00:00Z",
                                   "filter[playerNames]": "idmonfish"
                               })) > 0

    def test_matchesfilters(self, api):
        matches1 = api.matches({
            "filter[createdAt-start]": "2017-02-12T00:00:00Z",
            "filter[playerNames]": "Kraken",
            "page[limit]": 3
        })
        assert len(matches1) == 3
        matches2 = api.matches({
            "filter[createdAt-start]": "2017-02-12T00:00:00Z",
            "filter[playerNames]": "Kraken",
            "page[limit]": 3,
            "page[offset]": 1
        })

        commons = 0  # 3 matches each, offset 1 -> 2 overlap
        for match1 in matches1:
            for match2 in matches2:
                if match1.id == match2.id:
                    commons += 1
        assert commons == 2

        assert len(api.matches(region="eu", params={
            "filter[createdAt-start]": "2017-02-12T00:00:00Z",
            "filter[playerNames]": "shutterfly",
            "page[limit]": 9
        })) == 9

        def fromiso(s):
            return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")

        start = "2017-02-20T02:25:00Z"
        end = "2017-02-22T02:30:00Z"
        matches = api.matches({
            "filter[playerNames]": "Kraken",
            "filter[createdAt-start]": start,
            "filter[createdAt-end]": end
        })
        for match in matches:
            assert fromiso(end) >= fromiso(match.createdAt) >= fromiso(start)

        nick = "MMotooks123"
        matches = api.matches({
            "filter[createdAt-start]": "2017-02-10T00:00:00Z",
            "page[limit]": 5,
            "filter[playerNames]": nick
        })
        for match in matches:
            success = False
            for roster in match.rosters:
                for participant in roster.participants:
                    if participant.player.name == nick:
                        success = True
                        break
            assert success

        team = "3TB3"
        matches = api.matches(region="na", params={
            "filter[createdAt-start]": "2017-02-10T00:00:00Z",
            "page[limit]": 5,
            "filter[teamNames]": team
        })
        for match in matches:
            success = False
            for roster in match.rosters:
                if roster.team:
                    if roster.team.name == team:
                        success = True
                        break
            assert success

    def test_player(self, api):
        assert api.player("57342aac-7ff5-11e5-98bf-0628b69bf6d1").name == "oldchoas"
        assert "lossStreak" in api.player("57342aac-7ff5-11e5-98bf-0628b69bf6d1").stats
