#!/usr/bin/env python
# -*- coding: utf-8 -*-

import enum
import json
import os
from collections import defaultdict

import logging
import threading
import time
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel
from typing import Dict, Any

dir_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(dir_path, 'resources_settings.json')
with open(config_path, 'r') as config:
    RESOURCES_CONFIG = json.load(config)


class ThreadSafeDict(defaultdict):
    """
    Потокобезопасный словарь.
    """
    def __init__(self, lock: threading.RLock, *args, **kwargs):
        """
        :param lock: Объект синхронизации потоков
        """
        super(ThreadSafeDict, self).__init__(*args, **kwargs)
        self._lock = lock

    def __setitem__(self, key, item):
        with self._lock:
            super(ThreadSafeDict, self).__setitem__(key, item)

    def __getitem__(self, key):
        with self._lock:
            return super(ThreadSafeDict, self).__getitem__(key)

            
class Core(object):
    """
    Класс данных, использующийся для обмена данными
    между модулями.

    Подробное описание работы класса:
    https://bit.ly/2ItXDD6
    """
    def __init__(self, *args, **kwargs):
        # self.core_lock пока нельзя, дабы избежать вечной рекурсии.
        super(Core, self).__setattr__("core_lock", threading.RLock())

        self.initialize_screens()

    def initialize_screens(self):
        background_image_file_path = os.path.join(RESOURCES_CONFIG["images_folder"],
                                                  "dark_bg.jpg")
        bg = QPixmap(background_image_file_path)

        self.main_screen = QWidget()
        self.main_screen.move(70, 50)
        self.main_screen.setFixedSize(1300, 800)
        self.main_screen.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.main_screen.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        bgl1 = QLabel(self.main_screen)
        bgl1.setPixmap(bg)
        bgl1.show()
