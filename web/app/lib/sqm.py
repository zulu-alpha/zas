"""Library for extracting playable slots from an Arma mission.sqm file and validating that the
file is not Binerized
"""
__author__ = 'Adam Piskorski'

import re


def _whole_scope(raw, start_idx):
    """Returns all code that matches the scope of the starting index and deeper.

    :param raw: Mission.sqm text
    :param start_idx: Index to start searching from.
    :return: String of the starting index to the end of the current scope.
    """
    text = raw[start_idx:]
    depth = 0
    end = 0
    for idx, c in enumerate(text):
        if c == '{':
            depth += 1
            continue
        if c == '}':
            depth -= 1
            if depth == -1:
                end = idx
                break
            continue
    return text[:end]


def _all_scopes(raw, required_text):
    """Find all scopes in the given raw string that have the matching, required text in them.

    :param raw: String of Mission.sqm string
    :param required_text: Text that the scope must have and also marks the beginning of the scope.
    :return: List of all scopes that have the required text in them. Scopes start from that text.
    """
    scopes = []
    # Iterate through all scopes
    curr_idx = 0
    while True:
        curr_idx = raw.find(required_text, curr_idx)
        # Save to list and increment if found, else break
        if not curr_idx == -1:
            scope = _whole_scope(raw, curr_idx)
            scopes.append(scope)
            curr_idx += 1
        else:
            break
    return scopes


def _playable_from_group(group_raw):
    """Takes in a mission.sqm raw group code and returns a list of dictionaries containing all
    playable units rank, side and description. If there is no description then the unit type will
    be used.

    :param group_raw: String of group only scope from mission.sqm.
    :return: List of {side, description, rank}, else None
    """
    playables = []
    units = _all_scopes(group_raw, 'dataType="Object";')
    for unit in units:
        if unit.find('isPlayable=1;') > -1:
            playable = {}
            description = re.search('description="(.+)";', unit)
            if not description:
                description = re.search('type="(.+)";', unit)
            if description:
                playable['description'] = description.group(1)
            rank = re.search('rank="(.+)";', unit)
            if rank:
                playable['rank'] = rank.group(1)
            else:
                playable['rank'] = ''
            side = re.search('side="(.+)";', unit)
            if side:
                playable['side'] = side.group(1)
            if playable:
                playables.append(playable)
    if playables:
        return playables


def version_check(mission_raw, number=None):
    """Checks if the mission.sqm code has a version number (good for checking if the mission.sqm is
    binarized) and if a number parameter is provided checks if that version number matches the one
    in the mission.

    :param mission_raw: String of mission.sqm code
    :param number: (Optional) Int of the version number you are expecting
    :return: True if has version number or if version matches given number
    """
    version = re.search('version=(.+);', mission_raw)
    if not version:
        return False
    if number:
        version_number = int(version.group(1))
        return version_number == number
    return True


def all_slots(mission_raw):
    """Get's all playable slots from the given mission.sqm. Returns all slots sorted by side and in
    groups.

    :param mission_raw: String of Mission.sqm code
    :return: Dictionary containing lists of each group for each side
    """
    # Find all groups, then all playable objects and store them
    groups = _all_scopes(mission_raw, 'dataType="Group";')

    west_groups = []
    east_groups = []
    ind_groups = []
    civ_groups = []

    # Get playable units and sort groups by side
    for group in groups:
        slots = _playable_from_group(group)
        if not slots:
            continue
        # Sort by side
        if group.find('side="West";') > -1:
            west_groups.append(slots)
        if group.find('side="East";') > -1:
            east_groups.append(slots)
        if group.find('side="Independent";') > -1:
            ind_groups.append(slots)
        if group.find('side="Civilian";') > -1:
            civ_groups.append(slots)

    # Return a dictionary containing all slots
    return {'west': west_groups,
            'east': east_groups,
            'independent': ind_groups,
            'civilian': civ_groups}
