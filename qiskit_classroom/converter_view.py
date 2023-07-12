'''
    conveter view class
'''

from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QLabel, QComboBox, QVBoxLayout, QHBoxLayout, QFrame
# from .expression_enum import QuantumExpression
# from .converter_presenter import ConverterPresenter

class ConverterView(QWidget):
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
