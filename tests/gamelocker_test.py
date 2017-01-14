#!/usr/bin/python

import pytest
import requests
import gamelocker

class TestGamelocker:
    apikey = "aaa.bbb.ccc"

    @pytest.fixture
    def api(self):
        return gamelocker.Gamelocker(self.apikey).vainglory()

    def test_req(self, api):
        with pytest.raises(requests.exceptions.HTTPError):
            assert api._req("foobar")
        assert type(api._req("status")) is dict

        assert "status" in api.status()

    def test_map(self):
        assert gamelocker.datatypes.modulemap()["match"] is gamelocker.datatypes.Match

    def test_match(self, api):
        match = api.match("91cf2ee4-d7d0-11e6-ad79-062445d3d668")
        assert match.gameMode == "casual"
        assert isinstance(match.rosters[0], gamelocker.datatypes.Roster)
        assert isinstance(match.rosters[0].participants[0], gamelocker.datatypes.Participant)
        assert isinstance(match.rosters[0].participants[0].player, gamelocker.datatypes.Player)
        assert isinstance(match.rosters[0].participants[0].player.name, str)

        matches = api.matches()
        assert len(matches) > 0
        assert isinstance(matches[0], gamelocker.datatypes.Match)
        assert matches[0].duration > 0

        assert len(api.matches(limit=5)) == 5

    def test_player(self, api):
        assert api.player("6abb30de-7cb8-11e4-8bd3-06eb725f8a76").name == "boombastic04"
        assert "lossStreak" in api.player("6abb30de-7cb8-11e4-8bd3-06eb725f8a76").stats
