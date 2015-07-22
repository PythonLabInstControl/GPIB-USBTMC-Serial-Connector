#!/usr/bin/python

import sys
import os
from TermOut import Logging
import importlib

if sys.platform == "win32":
	Logging.error("Windows is not supported.")
	exit(1)

if len(sys.argv) == 2:
	if os.path.isfile(sys.argv[1]):
		import_path = os.path.dirname(sys.argv[1])
		sys.path.append(import_path)
		os.chdir(import_path)
		importlib.import_module(os.path.basename(os.path.splitext(sys.argv[1])[0]))
else:
	Logging.error("Specify python file as second argument")

