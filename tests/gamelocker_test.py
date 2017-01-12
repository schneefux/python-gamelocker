#!/usr/bin/python

import pytest
import requests
import gamelocker

class TestGamelocker:
    apikey = "aaa.bbb.ccc"

    @pytest.fixture
    def api(self):
        return gamelocker.Gamelocker(self.apikey).vainglory()

    def test_utils(self):
        assert gamelocker.Utils().search_dict({"a": "b", "c": "d", "e": 2}, "e", 2) == True
        assert gamelocker.Utils().search_dict({"a": "b", "c": {"d":1, "e": 2}}, "e", 2) == True
        assert gamelocker.Utils().search_dict({"a": "b", "c": {"d":1, "e": 2}}, "f", 1) == False

    def test_req(self, api):
        with pytest.raises(requests.exceptions.HTTPError):
            assert api._req("foobar")
#        with pytest.raises(AttributeError):  # TODO write this test
#            pass
        assert api._req("status").raw["status"] == 200
        assert len(api._req("matches", {"page[limit]": 10}).raw["data"]) == 10

    def test_status(self, api):
        assert type(api.status()) is str

    def test_matches(self, api):
        assert gamelocker.Matches(None, []).length == 0
        assert gamelocker.Matches(None, [None, None]).length == 2

        matches = api.matches()
        assert type(matches) is gamelocker.Matches
        assert type(matches[0]) is gamelocker.Match
        assert type(matches[0].rosters[0]) is gamelocker.Roster
        assert type(matches[0].rosters[0].participants[0]) is gamelocker.Participant
        assert type(matches[0].rosters[0].participants[0].attributes["actor"]) is str
        assert type(matches[0].rosters[0].participants[0].player) is gamelocker.Player
        assert type(matches[0].rosters[0].participants[0].player.attributes["name"]) is str

    def test_filter(self, api):
        assert api.matches().where("gameMode", "ranked").length > 0
        assert api.matches().where("gameMode", "foobar").length == 0
        assert api.matches(3).where("side", "left/blue").length == 3
        # in 3 games, there were 3 teams who were on the left side ;)

    def test_pagination(self, api):
        assert api.matches(50).length <= 50
        assert api.matches(10).length <= 10
        assert api.matches(3).length == 3
        api.matches(10, offset=30)
