python-gamelocker
===

[Private mirror](https://git.schneefux.xyz/schneefux/python-gamelocker) [GitHub mirror](https://github.com/schneefux/python-gamelocker)

Python 3 wrapper for the Gamelocker API. Currently supports [Vainglory](https://developers.vainglorygame.com). Install with PyPi: `pip install python-gamelocker`.

[Private docs mirror](https://docs.schneefux.xyz/python-gamelocker/gamelocker.html#module-gamelocker.api)

Example usage:
```python
>>> import gamelocker
>>> APIKEY = "aaa.bbb.ccc"
>>> api = gamelocker.Gamelocker(APIKEY).Vainglory()
>>> m = api.matches({"page[limit]": 2, "filter[playerNames]": "TheLegend27"})
>>> m
[<gamelocker.datatypes.Match object at 0x7f2682314ac8>, <gamelocker.datatypes.Match object at 0x7f26823d3c50>]
>>> m.rosters[0].participants[0].player.name
"iiDruid"
>>> m.rosters[0].participants[0].stats["kills"]
10
>>> m.rosters[0].stats["acesEarned"]
2
```

[More examples](/examples)
