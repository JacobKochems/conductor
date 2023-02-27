conductor
=========
Conductor orchestrates your bootstrap-/setup-/config-scripts'
execution order by recursively resolving the in-script declared
dependencies into a dependency ordered list and executes it.

Caution
-------
This is a very early version. Something I cobbled together on a weekend.
It has seen very little real application yet. **Use it at your own risk.**

Installation
------------
**General**
```shell
curl -fLo /your/custom/path https://raw.githubusercontent.com/JacobKochems/conductor/main/conductor.py && chmod a+x /your/custom/path
```
**yadm** - as a [bootstraper](https://yadm.io/docs/bootstrap) for the yadm dotfile manager
```shell
curl -fLo ~/.config/yadm/bootstrap https://raw.githubusercontent.com/JacobKochems/conductor/main/conductor.py && chmod a+x ~/.config/yadm/bootstrap && mkdir ~/.config/yadm/bootstrap.d
```

Usage
-----
1. Choose a name for the conductor script, let's say: `setup`
2. Create a directory in the same folder named: `setup.d`
3. You declare what a given script depends on by adding the keyphrase
`!depends_on:` followed by its dependencies, somewhere in the script.

For example, a shell scripts' dependency declaration might look like this:
```shell
#!/usr/bin/env bash
#!depends_on: foo.sh, bar.sh
echo "Hello Conductor!"
```
4. Profit.  ..um, I mean run it via `./setup` or invoke it from wherever.
