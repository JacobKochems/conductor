#------------------------------------------------------------------------------
# Conductor - orchestrate your scripts' execution
# Copyright (C) 2023  Jacob Kochems
# SPDX-License-Identifier: GPL-3.0-or-later
#------------------------------------------------------------------------------

all: poetry.lock

poetry.lock:
	. ./setup && setup_venv

.PHONY: clean
clean:
	. ./setup && setup_clean

.PHONY: purge
purge: clean
	. ./setup && setup_purge

