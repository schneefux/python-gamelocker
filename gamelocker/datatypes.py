#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
"""
gamelocker.datatypes

(internal) Classes and utility functions to map API responses to objects.
"""

import inspect
import sys
from gamelocker.janus import DataMessage, Attribute


def attr(typ, key, relation=False):
    """Convenience function to specify an attribute or a relation.

    :param typ: Allowed data type or class.
    :type typ: object
    :param key: Object name, mapping name and key mapping name.
    :type key: str
    :param link: (optional) Whether this is a relation.
    :return: `DataMessage` `Attribute` class.
    :rtype: :class:`Attribute`
    """
    if relation:
        return Attribute(value_type=typ, name=key,
                         mapping=key, key_mapping=key)
    else:
        return Attribute(value_type=typ, name=key,
                         mapping=key)


def rel(typ, key):
    """Convenience function to specify a relation.
       See `attr()`.
    """
    return attr(typ, key, True)


class Asset(DataMessage):
    type_name = "asset"
    key_id = attr(str, "id")

    url = attr(str, "URL")
    content_type = attr(str, "contentType")
    created_at = attr(str, "createdAt")
    description = attr(str, "description")
    filename = attr(str, "filename")
    name = attr(str, "name")


class Player(DataMessage):
    type_name = "player"
    key_id = attr(str, "id")

    name = attr(str, "name")
    stats = attr(dict, "stats")


class Participant(DataMessage):
    type_name = "participant"
    key_id = attr(str, "id")

    actor = attr(str, "actor")
    stats = attr(dict, "stats")

    player = rel(Player, "player")


class Team(DataMessage):
    type_name = "team"
    key_id = attr(str, "id")

    name = rel(str, "name")


class Roster(DataMessage):
    type_name = "roster"
    key_id = attr(str, "id")

    stats = attr(dict, "stats")

    participants = rel(Participant, "participants")
    team = rel(Team, "team")


class Match(DataMessage):
    type_name = "match"
    key_id = attr(str, "id")

    createdAt = attr(str, "createdAt")
    duration = attr(int, "duration")
    gameMode = attr(str, "gameMode")
    patchVersion = attr(str, "patchVersion")
    region = attr(str, "region")
    stats = attr(dict, "stats")

    rosters = rel(Roster, "rosters")
    assets = rel(Asset, "assets")


def modulemap():
    """Returns a dictionary where `type_name`s are mapped
       to corresponding classes from `gamelocker.datatypes`.

    :return: A dictionary with keys of `type_name`
             and values of :class:`DataMessage` subclasses.
    :rtype: :class:`gamelocker.janus.DataMessage`
    """
    typemap = dict()
    classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    for name, value in classes:
        if name == "Attribute" or name == "DataMessage":
            continue
        typemap[value.type_name] = value

    return typemap


def data_to_object(data):
    """Given a data dictionary from the API, returns mapped objects or None.

    :param data: Dictionary from API request.
    :type data: dict
    :return: An object.
    :rtype: :class:`gamelocker.janus.DataMessage`
    """
    # find the appropriate class from /datatypes.py
    typemap = modulemap()
    datatype = None
    for key, dataclass in typemap.items():
        if key == data["type"]:
            datatype = dataclass
    if datatype is None:
        raise NotImplementedError(
            "Data type " + data["type"] + " is not implemented yet.")

    # load data into class
    element = datatype()
    element.map_message(data)

    return element


def link_to_object(obj, relations):
    """Replaces references in `obj`
       by their corresponding objects from `relations`.

    :param obj: Master object to populate.
    :type obj: :class:`gamelocker.janus.DataMessage`
    :param relations: Object pool to populate from.
    :type obj: list of :class:`gamelocker.janus.DataMessage`
    :return: The populated master object.
    :rtype: :class:`gamelocker.janus.DataMessage`
    """
    for att in dir(obj):
        # loop through all relations that object could possibly have
        if not(isinstance(object.__getattribute__(obj, att), Attribute) and
               issubclass(
                   object.__getattribute__(obj, att).value_type, DataMessage)
               and not att.startswith("__")):
            continue

        # try to get the objects that are being linked to
        children = object.__getattribute__(obj, att).value
        if children is None:
            # there is no reference -> master class has object
            # but it was not populated with data
            # so it is (hopefully) optional.
            continue

        # can either be a reference or a list of references
        if isinstance(children, (list, tuple)):
            newlist = []
            for child in children:
                # replaces every element
                for relation in relations:
                    # see below
                    if relation.id == child.id:
                        relation = link_to_object(relation, relations)
                        newlist.append(relation)
                        break
            object.__setattr__(obj, att, newlist)
        else:
            for relation in relations:
                if relation.id == children.id:
                    # replace unpopulated relation
                    # with object from `relations` that has data
                    # also, replace all references in that object (recursively)
                    relation = link_to_object(relation, relations)
                    object.__setattr__(obj, att, relation)
                    break

    return obj
