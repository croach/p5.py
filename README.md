processing.py
=============

A python-based implementation of the Processing visualization language
that runs in the browser


Installation
============

Create a new virtual env and set the virtual environment's project
directory to the cloned processing.py repo. Then, add the following
line to the virtual environment's postactivate script:

```bash
export PYTHONPATH="$PYTHONPATH:$(cat "$VIRTUAL_ENV/$VIRTUALENVWRAPPER_PROJECT_FILENAME")/lib"
```