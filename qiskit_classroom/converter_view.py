'''
    conveter view class
'''

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QWidget, QLabel, QComboBox, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QFileDialog, QErrorMessage
from qiskit_classroom.expression_enum import expressions
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .converter_presenter import ConverterPresenter



class DropArea(QLabel):
    '''
        converter view class
    '''

    # presenter: ConverterPresenter

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Converter")
        self.setFixedSize(QtCore.QSize(500, 600))

        vbox = QVBoxLayout(self)
        vbox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("hello")

        vbox.addWidget(self.label)

        self.center()

    def center(self) -> None:
        frame = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        frame.moveCenter(cp)
        self.move(frame.topLeft())

    # def setPresenter(self, presenter: ConverterPresenter) -> None:
    #    self.presenter = presenter
