# -----------------------------------------------------------------------------
# Conductor - orchestrate your scripts' execution
# Copyright (C) 2023  Jacob Kochems
# SPDX-License-Identifier: GPL-3.0-or-later
# -----------------------------------------------------------------------------

import os
import stat
import shutil
import pytest
from conductor import KEYPHRASE, CACHE_SUFFIX, get_files_recursively, \
                      get_playbook, get_playlist, main

NAME = 'conductor'
APP = f'./{NAME}'
BIN_DIR = f'./{NAME}.d'
CACHE = f'{APP}{CACHE_SUFFIX}'


# ---( Functions for Test Environment Setup and Teardown )---------------------
def write_to_files(files_and_content: dict[str, str]):
    os.makedirs(BIN_DIR, exist_ok=True)
    for file, content in files_and_content.items():
        path = f'{BIN_DIR}/{file}'
        with open(path, "w") as f:
            f.write(content)
        os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)


def delete_files_in(dir: str):
    shutil.rmtree(dir)


@pytest.fixture(scope='class')
def files_and_content():
    return {  # create files a..g with dependency content
            'a': f'#!/bin/bash\n#{KEYPHRASE} d,e,c  \necho a\n',
            'b': f'#!/bin/bash\n#{KEYPHRASE}d,f     \necho b\n',
            'c': f'#!/bin/bash\n#{KEYPHRASE} d,e, f \necho c\n',
            'd':  '#!/bin/bash\n#leaf               \necho d\n',
            'e': f'#!/bin/bash\n#leaf\n# {KEYPHRASE}\necho e\n',
            'f': f'#!/bin/bash\n#leaf\n#{KEYPHRASE} \necho f\n',
            'g':  ''}


@pytest.fixture(autouse=True, scope='class')
def write_scripts(files_and_content):
    write_to_files(files_and_content)
    yield
    delete_files_in(BIN_DIR)


@pytest.fixture(autouse=True, scope='module')
def clean_up():
    yield
    if os.path.exists(CACHE):
        os.remove(CACHE)


# ---( The Tests )-------------------------------------------------------------
class TestUnits:
    def test_get_files_recursively(self, files_and_content):
        files = get_files_recursively(BIN_DIR)
        # check a sample item
        assert f'{BIN_DIR}/a' in files
        # check for expected number of items
        assert len(files) == len(files_and_content)

    def test_get_playbook(self):
        assert f'{BIN_DIR}/d' in get_playbook(BIN_DIR)[f'{BIN_DIR}/a']

    def test_get_playlist(self):
        playlist = [f'{BIN_DIR}/{file}'
                    for file in ['d', 'e', 'f', 'c', 'a', 'b', 'g']]
        playbook = get_playbook(BIN_DIR)
        assert get_playlist(playbook.keys(), playbook) == playlist


class TestIntegration:
    @pytest.fixture()
    def _files_and_content(self, files_and_content):
        return files_and_content.copy()

    def test_all_jobs_complete(self):
        assert main(APP) is True

    def test_a_job_fails(self, _files_and_content):
        # make a job fail
        _files_and_content['a'] += 'exit 1\n'
        write_to_files(_files_and_content)
        # first encounter of failed job should result in abort ..
        assert main(APP) is False
        # .. and produce a cache file of remaining jobs
        assert os.path.exists(CACHE)
        # if failed job continues to fail we expect the same outcome
        assert main(APP) is False
        assert os.path.exists(CACHE)
        # make the failed job pass trivially
        _files_and_content['a'] = ''
        write_to_files(_files_and_content)
        # now we expect success for all remaining jobs ..
        assert main(APP) is True
        # .. and the cache file to be removed
        assert not os.path.exists(CACHE)
