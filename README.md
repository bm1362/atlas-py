atlas-py
========

CS 4398.S13: Software Engineering Project

Windows Installation
====================

- Install Python 2.7
- Add python to path
- Download source
- http://pyglet.googlecode.com/files/pyglet-1.1.4.tar.gz
- Extract
- Run `python setup.py build`
- Run `python setup.py install`
    - This should install pyglet into the python runtime currently being used.
    - To test this, open up a command prompt and type: `python` to open the python interpreter `import pyglet` to import pyglet
    - if nothing happens and you see the prompt then the install was successful- you may see errors.
- Clone the git repo
- Run `python Simulation.py` from the atlas directory

Linux Installation
==================
- Install Python 2.7
- Install pip
- Run `sudo pip install pyglet`
- Clone the git repo
- Run `python Simulation.py` from the atlas directory