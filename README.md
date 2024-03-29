Conductor
=========
Conductor orchestrates your bootstrap-/setup-/config-scripts'
execution order by recursively resolving the in-script declared
dependencies into a dependency ordered list and executes it.

**Caution:** This is a very early version. Something I cobbled together on a
weekend. It has seen very little real application yet. Please use it at your
own risk.

Features
--------
 * **Resolve dependencies:** Conductor automatically resolves
dependencies declared within script files, ensuring that scripts are executed
in the correct order.

 * **Easy setup:** Simply create a directory for your conductor script and any
dependent scripts, add the appropriate `!depends_on:` lines to your scripts,
and you're ready to go.

 * **Portable:** Conductor is a simple Python script that can be run on any
platform with Python 3.9 (possibly 3.7, but untested yet) or higher installed,
making it easy to integrate into your existing setup.

 * **Caching:** Conductor can cache the list of jobs to be executed, allowing
you to easily resume a partially completed run if one of the scripts return
with a non-zero exit status

 * **Flexible:** Conductor can be used for any type of executable, be it a
shell script, a Python script or a binary

Installation
------------
**General**
```shell
curl -fLo /your/custom/path https://raw.githubusercontent.com/JacobKochems/conductor/main/conductor.py && chmod a+x /your/custom/path
```
**yadm** - as a [bootstraper](https://yadm.io/docs/bootstrap) for the yadm
dotfile manager
```shell
curl -fLo ~/.config/yadm/bootstrap https://raw.githubusercontent.com/JacobKochems/conductor/main/conductor.py && chmod a+x ~/.config/yadm/bootstrap && mkdir -p ~/.config/yadm/bootstrap.d
```

Usage
-----
1. Choose a name for the conductor script, let's say: `setup`
2. Create a directory in the same folder named: `setup.d`
3. Declare the dependencies for a given script by adding the keyphrase
`!depends_on:` followed by its dependencies, somewhere in the script.

For example, a shell script's dependency declaration might look like this:
```shell
#!/usr/bin/env bash
#!depends_on: foo.sh, bar.sh
echo "Hello Conductor!"
```
4. Profit.  ..um, I mean run it via `./setup` or invoke it from wherever you
want.

Conductor generates an ordered list of scripts and runs them. If an error
occurs during script execution, the remaining jobs, including the offending
one, are cached to the file `<scriptname>-job.cache` and conductor exits with
a non-zero exit status. If it finds the cache file on a subsequent run it will
try to finish the cached jobs.
