#!/usr/bin/python

import pytest
import requests
import gamelocker
import datetime

class TestGamelocker:
    apikey = "aaa.bbb.ccc"

    @pytest.fixture
    def api(self):
        return gamelocker.Gamelocker(self.apikey).Vainglory()

    def test_req(self, api):
        with pytest.raises(requests.exceptions.HTTPError):
            assert api._req("foobar")
        assert type(api._req("status")) is dict

        assert api.status()["data"]["attributes"]["version"]

    def test_map(self):
        assert gamelocker.datatypes.modulemap()["match"] is gamelocker.datatypes.Match

    def test_strings(self, api):
        stats = gamelocker.strings.Stats({"foo": 1, "bar": 2, "baz": {"deep": True}})
        assert stats.foo == 1
        assert stats.baz.deep == True

        taka = gamelocker.strings.Hero("*Sayoc*")
        assert taka == "*Sayoc*"
        assert taka.pretty() == "Taka"
        assert gamelocker.strings.Hero("notexisting") == "notexisting"

        assert gamelocker.strings.Item("Boots2").pretty() == "Travel Boots"
        assert gamelocker.strings.Item("*1032_Item_TravelBoots*").pretty() == "Travel Boots"
        assert gamelocker.strings.Item("unknowntestitem").pretty() == "unknowntestitem"

        assert gamelocker.strings.LazyObject("Boots2").pretty() == "Travel Boots"
        assert gamelocker.strings.LazyObject("*Sayoc*").pretty() == "Taka"

        match = api.match("91cf2ee4-d7d0-11e6-ad79-062445d3d668")
        assert isinstance(match.rosters[0].participants[0].actor, gamelocker.strings.Hero)

        assert isinstance(match.rosters[0].stats.acesEarned, int)
        assert isinstance(match.rosters[0].participants[0].stats.items[0], gamelocker.strings.LazyObject)
        assert isinstance(match.rosters[0].participants[0].stats.items[0].pretty(), str)

    def test_match(self, api):
        match = api.match("91cf2ee4-d7d0-11e6-ad79-062445d3d668")
        assert match.gameMode == "casual"
        assert isinstance(match.rosters[0], gamelocker.datatypes.Roster)
        assert isinstance(match.rosters[0].participants[0], gamelocker.datatypes.Participant)
        assert isinstance(match.rosters[0].participants[0].player, gamelocker.datatypes.Player)
        assert isinstance(match.rosters[0].participants[0].player.name, str)

    def test_matches(self, api):
        matches = api.matches()
        assert len(matches) > 0
        assert isinstance(matches[0], gamelocker.datatypes.Match)
        assert matches[0].duration > 0

    def test_matchesfilters(self, api):
        matches1 = api.matches(limit=3)
        assert len(matches1) == 3
        matches2 = api.matches(limit=3, offset=1)

        commons = 0  # 3 matches each, offset 1 -> 2 overlap
        for match1 in matches1:
            for match2 in matches2:
                if match1.id == match2.id:
                    commons += 1
        assert commons == 2

        assert len(api.matches(limit=52)) == 52

        # TODO uncomment as soon as the API is up
#        matches = api.matches(limit=10, sort="duration")
#        assert matches[0].duration < matches[9].duration

        def fromiso(s):
            return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")

        start = "2017-01-10T02:25:00Z"
        end = "2017-01-12T02:30:00Z"
        matches = api.matches(createdAtStart=start, createdAtEnd=end)
        for match in matches:
            assert fromiso(end) >= fromiso(match.createdAt) >= fromiso(start)

#        nick = "MMotooks123"
#        matches = api.matches(limit=5, player=nick)
#        for match in matches:
#            success = False
#            for roster in match.rosters:
#                for participant in roster.participants:
#                    if participant.player.name == nick:
#                        success = True
#                        break
#            assert success
#
#        team = "HALO"
#        matches = api.matches(limit=5, team=team)
#        for match in matches:
#            success = False
#            for roster in match.rosters:
#                if roster.team:
#                    if roster.team.name == team:
#                        success = True
#                        break
#            assert success

    def test_player(self, api):
        assert api.player("6abb30de-7cb8-11e4-8bd3-06eb725f8a76").name == "boombastic04"
        assert "lossStreak" in api.player("6abb30de-7cb8-11e4-8bd3-06eb725f8a76").stats
