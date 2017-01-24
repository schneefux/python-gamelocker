#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
gamelocker.api

This module implements the Gamelocker API.
"""

import datetime
import requests
import gamelocker.datatypes
import gamelocker.strings


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
        self.region = ""

    def _req(self, method, params=None):
        """Sends a GET request to the API endpoint.

        :param method: Method to query.
        :type method: str
        :param params: (optional) Parameters to send.
        :type params: dict
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
        return http.json()

    def _get(self, endpoint, elid="", params=None):
        """Returns an object or a list of objects from the API.

        :param endpoint: API slug to use.
        :type endpoint: str
        :param elid: (optional) ID of the object to query for.
        :type elid: str
        :param params: (optional) Parameters to pass with the http request.
        :type params: dict
        :return: Data object.
        :rtype: :class:`janus.DataMessage`
        """
        data = self._req("shards/" + self.region + "/" +
                         endpoint + "/" + elid, params=params)

        # collect related data
        includes = []
        if "included" in data:
            for incl in data["included"]:
                element = gamelocker.datatypes.data_to_object(incl)
                includes.append(element)

        # main data object
        if isinstance(data["data"], (list, tuple)):
            elements = []
            for dat in data["data"]:
                element = gamelocker.datatypes.data_to_object(dat)
                # link related data
                element = gamelocker.datatypes.link_to_object(
                    element, includes)
                elements.append(element)
            return elements
        else:
            element = gamelocker.datatypes.data_to_object(data["data"])
            # link related data
            element = gamelocker.datatypes.link_to_object(element, includes)
            return element

    def Vainglory(self, region="na"):
        """Sets title to Vainglory and data region.

        :param region: (optional) Data region (shard) to use. Defaults to NA.
        :type region: str
        :return: :class:`Gamelocker <Gamelocker>` object
        :rtype: gamelocker.Gamelocker
        """
        self.title = "semc-vainglory"
        self.region = region
        return self

    def status(self):
        """Returns the API status JSON string.

        :return: API status JSON.
        :rtype: str
        """
        return self._req("status")

    def match(self, elid):
        """Returns a match.

        :param elid: ID of the match.
        :type elid: str
        :return: A match with the given ID.
        :rtype: :class:`Match`
        """
        return self._get("matches", elid)

    def player(self, elid):
        """Returns a player.

        :param elid: ID of the player.
        :type elid: str
        :return: A player with the given ID.
        :rtype: :class:`Player`
        """
        return self._get("players", elid)

    def matches(self, params=None):
        """Returns a list of recent matches.

        :param params: (optional) Query parameters.
        :type params: dict
        :return: List of matches.
        :rtype: list of dict
        """
        return self._get("matches", params=params)


pretty = gamelocker.strings.pretty
