from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect, QPoint, QPointF, QTimer
from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QPushButton,
                             QGridLayout, QRadioButton,
                             QSlider, QSizePolicy, QWidget, QSpacerItem,
                             QGraphicsScene, QGraphicsView, QMainWindow, QDesktopWidget, QHBoxLayout,
                             QTextBrowser, QComboBox)

import threading


class MachineStateManagement(object):
    def __init__(self, core):
        super().__init__()
        self.combo = {}
        self.grid = QGridLayout()
        self.core = core
        self.killed = False
        self.core_screen = core.main_screen
        self.confirm = QWidget()

    def kill(self):
        self.killed = True
        
    def prepare(self, main_sm, color, font_size, text_transform, font_weight):
        self.main_sm = main_sm
        self.widget = QWidget(self.core_screen)
        self.widget.setFixedSize(500,250)
        self.widget.move(400,250)

        for k, position in zip(self.main_sm, range(5)):
            lbl = QLabel()
            lbl.setText(k)
            lbl.setStyleSheet("color: %s; font-size: %s; text-transform: %s; font-weight: %s;" % (color, font_size, text_transform, font_weight))
            self.combo[k] = QComboBox()
            self.combo[k].addItems(list(self.main_sm[k].values()))
            self.grid.addWidget(self.combo[k], position, 0)
            self.grid.addWidget(lbl, position, 1)
            self.combo[k].currentIndexChanged.connect(self.widn)

        self.widget.setLayout(self.grid)


    def getKey(self, text):
        currentText = self.widget.sender()
        for key, val in self.combo.items():
            if val == currentText:
                print(list(self.main_sm[key])[text])


    def widn(self):
        self.core.output_data = {"local_sim": {"set_state": {"sm_name": "TowerControllerNode", "state_name": "tilt_regulation"}}}
        for k in self.combo:
            self.combo[k].setEnabled(False)

        layout = QVBoxLayout()
        btn_ok = QPushButton()
        btn_ok.setText("Подтвердить")
        btn_ok.setStyleSheet("background: #009B76; color: #fff; text-transform: uppercase;")
        btn_ok.resize(100,100)
        btn_ok.move(100,100)


        btn_no = QPushButton()
        btn_no.setText("Отмена")
        btn_no.setStyleSheet("background: #E32636; color: #fff; text-transform: uppercase;")
        btn_no.resize(100,100)
        btn_no.move(100,100)

        btn_ok.clicked.connect(self.buttonClicked1)
        btn_no.clicked.connect(self.buttonClicked2)

        layout.addWidget(btn_ok)
        layout.addWidget(btn_no)
        self.confirm.setLayout(layout)
        self.confirm.setFixedSize(300, 90)
        self.confirm.setStyleSheet("background: #4E5754;")
        self.confirm.setWindowOpacity(1)
        self.confirm.setWindowFlags(Qt.CustomizeWindowHint)
        self.confirm.show()

    def buttonClicked1(self):
        self.confirm.hide()
        for k in self.combo:
            self.combo[k].setEnabled(True)

    def buttonClicked2(self):
        self.confirm.hide()
        for k in self.combo:
            self.combo[k].setEnabled(True)

    def start(self):
        update_thread = threading.Thread(target=self.update, args=())
        update_thread.start()

    def update(self):
    	pass