#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import logging

from collections import OrderedDict
from importlib import import_module
from PyQt5.QtWidgets import QApplication

from core import Core

import PyQt5

dir_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(dir_path, 'modules.json')
with open(config_path, 'r') as modules_config:
    MODULES_CONFIG = json.load(modules_config, object_pairs_hook=OrderedDict)

def main():
	app = QApplication(sys.argv)
	core = Core()
	modules = []

	for module_id, args in MODULES_CONFIG.items():
	    is_active = args.get('is_active')
	    if not is_active:
	        continue


	    class_name = args.get('class_name')
	    init_args = args.get('init_args')
	    prep_args = args.get('prep_args')
	    file_name = args.get('file_name')

	    modules_file = import_module(file_name)
	    module_class = getattr(modules_file, class_name)
	    module = module_class(core=core, **init_args)
	    module.prepare(**prep_args)
	    modules.append(module)

	for module in modules:
		module.start()
	
	core.main_screen.show()

	sys.exit(app.exec_())

if __name__ == "__main__":
	main()