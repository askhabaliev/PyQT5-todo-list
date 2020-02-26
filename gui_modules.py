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
        
    def prepare(self, sm, widget_params, confirm_params):
        self.widget_params = dict(widget_params)
        self.confirm_params = dict(confirm_params)
        self.sm = sm
        self.widget = QWidget(self.core_screen)
        self.widget.setFixedSize(self.widget_params["width"], self.widget_params["height"])
        self.widget.move(self.widget_params["x"], self.widget_params["y"])

        for k in self.sm:
            m_name = list(self.sm[k])[0]
            sm_name = dict(self.sm[k][m_name])
            index = list(self.sm).index(k)
            lbl = QLabel()
            lbl.setText(m_name)
            lbl.setStyleSheet("color: %s; font-size: %s; text-transform: %s; font-weight: %s;" % (self.widget_params["color"], self.widget_params["font_size"], self.widget_params["text_transform"], self.widget_params["font_weight"]))
            self.combo[m_name] = QComboBox()
            self.combo[m_name].addItems(sm_name.values())
            self.grid.addWidget(self.combo[m_name], index, 0)
            self.grid.addWidget(lbl, index, 1)
            self.combo[m_name].currentIndexChanged.connect(self.prep_confirm)

        self.widget.setLayout(self.grid)


    def prep_confirm(self, index):
        currentText = self.widget.sender()
        self.node_choice = None
        self.current_sm = None

        for k in self.combo:
            self.combo[k].setEnabled(False)

        layout = QVBoxLayout()

        btn_ok = QPushButton()
        btn_ok.setText("Подтвердить")
        btn_ok.setStyleSheet("color: %s; background: %s; text-transform: %s;" % (self.confirm_params["color"], self.confirm_params["background_ok"], self.confirm_params["text_transform"]))
        btn_ok.resize(100,100)
        btn_ok.move(100,100)

        btn_no = QPushButton()
        btn_no.setText("Отмена")
        btn_no.setStyleSheet("color: %s; background: %s; text-transform: %s;" % (self.confirm_params["color"], self.confirm_params["background_no"], self.confirm_params["text_transform"]))
        btn_no.resize(100,100)
        btn_no.move(100,100)

        for key, val in self.combo.items():
            if val == currentText:
                sm_name = [list(self.sm[k][key]) for k in self.sm if list(self.sm[k])[0] == key][0]
                self.current_sm = sm_name[index]
                self.node_choice = [ k for k in self.sm if list(self.sm[k])[0] == key ][0]

        btn_ok.clicked.connect(self.btn_ok_clicked)
        btn_no.clicked.connect(self.btn_no_clicked)

        layout.addWidget(btn_ok)
        layout.addWidget(btn_no)

        self.confirm.setLayout(layout)
        self.confirm.setFixedSize(300, 90)
        self.confirm.setStyleSheet("background: %s;" % (self.confirm_params["background"]))
        self.confirm.setWindowFlags(Qt.CustomizeWindowHint)
        self.confirm.setWindowOpacity(1)
        self.confirm.show()

    def btn_ok_clicked(self):
        vehid = self.core.watched_vehid or self.core.in_rc_vehid
        print(self.node_choice, self.current_sm)
        self.core.output_data = {vehid: {"set_state": {"sm_name": self.node_choice, "state_name": self.current_sm}}}
        self.confirm.hide()
        for k in self.combo:
            self.combo[k].setEnabled(True)

    def btn_no_clicked(self):
        self.confirm.hide()
        for k in self.combo:
            self.combo[k].setEnabled(True)

    def start(self):
        pass