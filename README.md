p5.py
=============

A python-based implementation of the Processing visualization language
that runs in the browser.

Since p5.py works with the cpython interpreter, it can be used with 
any python-based library as well as c-based libraries such as Numpy,
Scipy, and matplotlib.

Installation
============

Create a new virtual env, activate it, and then add the p5.py lib 
folder to the `PYTHONPATH` variable with the following line. Note, 
this assumes that you are currently in the p5.py folder.

```bash
$ export PYTHONPATH="$PYTHONPATH:$(pwd)/lib"
```

Once you have the `PYTHONPATH` setup properly, you can test that 
the installation was succesful by running one of the examples. To
do so, simply execute any of the example files as you would any 
python script, for example:

```bash
$ python examples/circles.py
```
