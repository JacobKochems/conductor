# -----------------------------------------------------------------------------
# Conductor - orchestrate your scripts' execution
# Copyright (C) 2023  Jacob Kochems
# SPDX-License-Identifier: GPL-3.0-or-later
# -----------------------------------------------------------------------------

import os
import stat
from conductor import KEYPHRASE, get_files_recursively, get_playbook, \
                      get_playlist

# ---( setup test environment )------------------------------------------------
DIRECTORY = 'conductor.d/'
os.makedirs(DIRECTORY, exist_ok=True)
files_and_content = {  # create files a..g with dependency content
    'a': f'#!/bin/bash\n#{KEYPHRASE} d,e,c  \necho a\n',
    'b': f'#!/bin/bash\n#{KEYPHRASE}d,f     \necho b\n',
    'c': f'#!/bin/bash\n#{KEYPHRASE} d,e, f \necho c\n',
    'd':  '#!/bin/bash\n#leaf               \necho d\n',
    'e': f'#!/bin/bash\n#leaf\n# {KEYPHRASE}\necho e\n',
    'f': f'#!/bin/bash\n#leaf\n#{KEYPHRASE} \necho f\n',
    'g':  '#!/bin/bash\nexit 1',
    'h':  '#!/bin/bash\necho $0\n',
}
for file, content in files_and_content.items():
    path = DIRECTORY+file
    with open(path, "w") as f:
        f.write(content)
    os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)


# ---( run the tests )---------------------------------------------------------
def test_get_files_recursively():
    files = get_files_recursively(DIRECTORY)
    # check a sample item
    assert f'{DIRECTORY}a' in files
    # check for expected number of items
    assert len(files) == len(files_and_content)


def test_get_playbook():
    assert f'{DIRECTORY}d' in get_playbook(DIRECTORY)[f'{DIRECTORY}a']


def test_get_playlist():
    playlist = [DIRECTORY+file
                for file in ['d', 'e', 'f', 'c', 'a', 'b', 'g', 'h']]
    playbook = get_playbook(DIRECTORY)
    assert get_playlist(playbook.keys(), playbook) == playlist
