#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods,fixme
# TODO: generate documentation

"""
requests.api

This module implements the Gamelocker API.
"""

import requests


class Utils(object):
    """Utility functions."""

    def search_dict(self, dic, attr, val):
        """Find a key-value pair recursively in a dictionary.

        :param dic: Dictionary to search.
        :type dic: dict
        :param attr: Key to look for.
        :type attr: str
        :param val: Value the key needs to have.
        :param val: object
        :returns: (bool) Whether the dictionary contains the pair.
        :rtype: bool
        """
        for key in dic:
            if isinstance(dic[key], dict):
                if self.search_dict(dic[key], attr, val):
                    return True
            else:
                if key == attr and dic[key] == val:
                    return True

        return False


class Response(object):
    """A generic API response object.

    :param errors: `errors` as returned by the API.
    :param data: `errors` as returned by the API.
    :param links: `links` as returned by the API.
    :param included: `included` as returned by the API.
    :param raw: Raw response.
    :type raw: dict
    """

    def __init__(self, data):
        """Constructs a :class:`Response <Response>`.

        :param data: Dictionary from API response JSON.
        :type data: dict
        :return: :class:`Response <Response>` object
        :rtype: gamelocker.Response
        """
        if "errors" in data:
            self.errors = data["errors"]
        else:
            self.errors = None
        if "data" in data:
            self.data = data["data"]
        else:
            self.data = None
        if "links" in data:
            self.links = data["links"]
        else:
            self.links = None
        if "included" in data:
            self.included = data["included"]
        else:
            self.included = None
        self.raw = data
        if self.errors:
            raise AttributeError(
                "API returned errors: {errors}".format(
                    errors=repr(self.errors)))

    def filter(self, fid, ftype):
        """Returns an element from `data` matching the criteria.

        :param fid: ID to look for.
        :type fid: str
        :param ftype: Obect type to look for.
        :type ftype: str
        :return: Element matching the filter criteria
        :rtype: dict
        """
        for include in self.included:
            if include["id"] == fid and include["type"] == ftype:
                return include
        for datum in self.data:
            if datum["id"] == fid and datum["type"] == ftype:
                return datum

        return None


# TODO: implement a Matches.players()
class Matches(object):
    """A collection of :class:`Match <Match>` objects.

    :param matches: A list of matches.
    :type matches: list
    :param length: The number of matches.
    :type length: int
    """

    def __init__(self, data, matches=None):
        """Constructs a :class:`Matches <Matches>`.

        :param data: API data.
        :type data: gamelocker.Response
        :param matches: (optional) List of matches to construct
                        collection from. Overrides `data` matches.
        :type matches: list of :class:`Matches`
        :return: :class:`Matches <Matches>` object
        :rtype: gamelocker.Matches
        """
        self._data = data
        self.matches = []
        if matches is not None:
            self.matches = matches
        else:
            for match in self._data.data:
                self.matches.append(Match(self._data, match["id"]))
        self.length = len(self.matches)

    def __getitem__(self, key):
        return self.matches[key]

    def where(self, attribute, value):
        """Searches for matches where the condition is met.

        :param attribute: Attribute to look for.
        :type attribute: str
        :param value: Requested value for that attribute.
        :type value: str, int, object
        :return: Collection of :class:`Match` matching the criteria.
        :rtype: gamelocker.Matches
        """
        matches = []
        for match in self.matches:
            if match.has(attribute, value):
                matches.append(match)
        return Matches(self._data, matches)


class Match(object):
    """A Match record.

    :param attributes: `attributes` as returned by the API.
    :param rosters: List of :class:`Roster <Roster>` objects
                    related to the match.
    :type rosters: list
    """

    def __init__(self, data, mid):
        """Constructs a :class:`Match <Match>` from a :class:`Response`.

        :param data: API data.
        :type data: gamelocker.Response
        :param mid: Match ID.
        :type mid: str
        :return: :class:`Match <Match>` object
        :rtype: gamelocker.Match
        """
        self._data = data
        self._id = mid
        match = self._data.filter(mid, "match")
        self.attributes = match["attributes"]
        self.rosters = [Roster(self._data, r["id"])
                        for r in match["relationships"]["rosters"]["data"]]

    # TODO refactor duplicated code
    def has(self, attribute, value, recurse=True):
        """Checks whether Match or (optionally) a child owns an `attribute`
           with `value`.

        :param attribute: Attribute to look for.
        :type attribute: str
        :param value: Requested value for that attribute.
        :type value: str, int, object
        :param recurse: Whether to search relationships or not.
        :type recurse: bool
        :return: bool
        :rtype: bool
        """
        if Utils().search_dict(self.attributes, attribute, value):
            return True
        if recurse:
            for roster in self.rosters:
                if roster.has(attribute, value):
                    return True

        return False


class Roster(object):
    """A Roster object.

    :param attributes: `attributes` as returned by the API.
    :param participants: List of :class:`Participant <Participant>` objects
                         related to the roster.
    :type rosters: list
    """

    def __init__(self, data, rid):
        """Constructs a specified :class:`Roster <Roster>` from a :class:`Response`.

        :param data: API data.
        :type data: gamelocker.Response
        :param rid: Roster ID.
        :type rid: str
        :return: :class:`Roster <Roster>` object
        :rtype: gamelocker.Roster
        """
        self._data = data
        self._id = rid
        roster = self._data.filter(rid, "roster")
        self.attributes = roster["attributes"]
        self.participants = [
            Participant(self._data, p["id"])
            for p in roster["relationships"]["participants"]["data"]
        ]

    def has(self, attribute, value, recurse=True):
        """Checks whether Roster or (optionally) a child owns an `attribute`
           with `value`.

        :param attribute: Attribute to look for.
        :type attribute: str
        :param value: Requested value for that attribute.
        :type value: str, int, object
        :param recurse: Whether to search relationships or not.
        :type recurse: bool
        :return: bool
        :rtype: bool
        """
        if Utils().search_dict(self.attributes, attribute, value):
            return True
        if recurse:
            for participant in self.participants:
                if participant.has(attribute, value):
                    return True

        return False


class Participant(object):
    """A Participant object.

    :param attributes: `attributes` as returned by the API.
    :param player: :class:`Player <Player>` object related to the participant.
    :type player: gamelocker.Player
    """

    def __init__(self, data, pid):
        """Constructs a specified :class:`Participant <Participant>`
           from a :class:`Response`.

        :param data: API data.
        :type data: gamelocker.Response
        :param pid: Participant ID.
        :type pid: str
        :return: :class:`Participant <Participant>` object
        :rtype: gamelocker.Participant
        """
        self._data = data
        self._id = pid
        participant = self._data.filter(pid, "participant")
        self.attributes = participant["attributes"]
        self.player = Player(self._data,
                             participant["relationships"]["player"]
                             ["data"]["id"])

    def has(self, attribute, value):
        """Checks whether Participant or (optionally) owns an `attribute`
           with `value`.

        :param attribute: Attribute to look for.
        :type attribute: str
        :param value: Requested value for that attribute.
        :type value: str, int, object
        :return: bool
        :rtype: bool
        """
        if Utils().search_dict(self.attributes, attribute, value):
            return True
        return False


class Player(object):
    """A Player object.

    :param attributes: `attributes` as returned by the API.
    """

    def __init__(self, data, pid):
        """Constructs a specified :class:`Player <Player>` from a :class:`Response`.

        :param data: API data.
        :type data: gamelocker.Response
        :param pid: Player ID.
        :type pid: str
        :return: :class:`Player <Player>` object
        :rtype: gamelocker.Player
        """
        self._data = data
        self._id = pid
        player = self._data.filter(pid, "player")
        self.attributes = player["attributes"]


class Gamelocker(object):
    """Implementation of the Gamelocker API.

    :param apikey: API key used.
    :type apikey: str
    :param title: Title data is fetched for.
    :type title: str
    """

    def __init__(self, apikey, datacenter="dc01"):
        """Constructs a :class:`Gamelocker <Gamelocker>`.

        :param apikey: API key to authenticate with.
        :type apikey: str
        :param datacenter: (optional) API endpoint datacenter to use.
        :type datacenter: str
        :return: :class:`Gamelocker <Gamelocker>` object
        :rtype: gamelocker.Gamelocker

        Usage::

            >>> import gamelocker
            >>> gamelocker.Gamelocker("getoffmylawn").status()
            "v1.0.5"
        """

        self.apikey = apikey
        self._apiurl = "https://api." + datacenter + ".gamelockerapp.com/"
        self.title = ""

    def _req(self, method, params=None):
        """Sends a GET request to the API endpoint.

        :param method: Method to query.
        :param params: (optional) Parameters to send.
        :return: Parsed JSON object.
        :rtype: dict
        """
        headers = {
            "Authorization": "Bearer " + self.apikey,
            "X-TITLE-ID": self.title,
            "Accept": "application/vnd.api+json"
        }
        http = requests.get(self._apiurl + method,
                            headers=headers,
                            params=params)
        http.raise_for_status()
        return Response(http.json())

    def vainglory(self):
        """Sets title to Vainglory.

        :return: :class:`Gamelocker <Gamelocker>` object
        :rtype: gamelocker.Gamelocker
        """
        self.title = "semc-vainglory"
        return self

    def status(self):
        """Returns the API version.

        :return: API version.
        :rtype: str
        """
        return self._req("status").raw["version"]

    def matches(self, limit=None, offset=None, sort=None):
        """Returns a list of recent matches.

        :param limit: Maximum number of matches to return.
        :type limit: int
        :param offset: Offset parameter for pagination.
        :type limit: int
        :param sort: Sort query to use.
        :type sort: str
        :return: List of matches.
        :rtype: list of dict
        """
        params = dict()
        # TODO: deprecate by ?limit=x&offset=y soon
        if limit:
            params["page[limit]"] = limit
        if offset:
            params["page[offset]"] = offset
        if sort:  # TODO make this nice and usable
            params["sort"] = sort
        return Matches(self._req("matches", params))
