#!/usr/bin/env python3

# -----------------------------------------------------------------------------
# Conductor - orchestrate your scripts' execution
# Copyright (C) 2023  Jacob Kochems
# SPDX-License-Identifier: GPL-3.0-or-later
# -----------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

import os
import sys
import re
from collections import OrderedDict

# this matches anywhere in a filename
EXCLUSION_PATTERN = ["##", "README", "readme"]

# this matches only at the end of a filename
EXCLUSION_SUFFIX = ["~", ".md", ".lst", ".off", ".false", ".disabled"]

KEYPHRASE = '!depends_on:'


def get_files_recursively(directory):
    paths = []
    for root, directories, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            paths.append(path)
    paths.sort()
    return paths


def get_dependencies(file, directory):
    with open(file, "r") as file:
        content = file.read()

    match = re.findall(fr"{KEYPHRASE}[ \t]*(\w+.+)\b", content)
    return [directory+dep
            for dep in re.split(r"[ ,\t]+", match[0])] if match else None


def get_playbook(directory):
    return OrderedDict(
           [(file, get_dependencies(file, directory))
            for file in get_files_recursively(directory)
            if not any(p in file for p in EXCLUSION_PATTERN)
            and not any(file.endswith(s) for s in EXCLUSION_SUFFIX)
            and os.access(file, os.X_OK)])


def get_playlist(plays, playbook, playlist=[]):
    candidates = []
    for play in plays:
        dependencies = playbook[play]
        if dependencies:
            candidates += get_playlist(dependencies, playbook, playlist)
        candidates += [play]
        playlist += [c for c in candidates if c not in playlist]
    return playlist


def main(name):
    playbook = get_playbook(name+'.d/')
    for play in get_playlist(playbook.keys(), playbook):
        os.system(play)


if __name__ == "__main__":
    main(sys.argv[0])
