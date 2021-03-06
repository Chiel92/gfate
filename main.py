#!python3
"""Top level script which runs fate."""

import os
import sys

libs_path = os.path.dirname(os.path.abspath(__file__)) + '/libs/'
libs_path_fate = os.path.dirname(os.path.abspath(__file__)) + '/libs/fate/'
sys.path.insert(0, libs_path)
sys.path.insert(0, libs_path_fate)

# Make sure fate can be imported anywhere (also from the user script).
# This way we can:
# - run fate without having it installed
# - and thus easily test development source
# - have multiple fate packages, in case we would use multiple user interfaces.

import gui.main
import fate
import threading
import logging

# Create gfate
app = gui.main.main()

# Create fate
filenames = sys.argv[1:] or ['']
fate.document.Document.create_userinterface = app.mainWindow.addWin
for filename in filenames:
    doc = fate.document.Document(filename)
fate.document.documentlist[0].activate()

# Start fate
thread = threading.Thread(target=fate.run)
thread.start()

# Forward the fate logging to the standard out
logging.getLogger().addHandler(logging.StreamHandler())

# Start gfate
try:
    app.mainloop()
except:
    fate.commands.force_quit()
    raise

# TODO: at crash close eachother (double try catch)
