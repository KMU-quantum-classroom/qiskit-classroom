'''
    conveter view class
'''


from typing import TYPE_CHECKING
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (QWidget, QLabel, QComboBox, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QFileDialog, QMessageBox)
from qasync import asyncSlot
from qiskit_classroom.expression_enum import expressions


if TYPE_CHECKING:
    from .converter_presenter import ConverterPresenter


class DropArea(QLabel):
    '''
        file drop area widget
    '''

    def __init__(self) -> None:
        super().__init__()
        self.set_ui()
        self.drop_handler = None

    def set_ui(self) -> None:
        '''
            set UI
        '''
        self.setFixedHeight(250)
        self.setStyleSheet("border-style: dashed; border-width: 2px; color: blue; border-color: red;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("drop .py file here")

    def set_drop_handler(self) -> None:
        '''
            pass file path to presenter
        '''
        pass


class ConverterView(QWidget):
    '''
        converter view class
    '''
    def __init__(self) -> None:
        super().__init__()
        self.presenter = None
        self.set_ui()
        self.center()

    def set_ui(self) -> None:
        '''
            set UI
        '''
        self.setWindowTitle("Converter")
        self.setContentsMargins(50, 50, 50, 50)
        self.setFixedSize(QSize(500, 600))

        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.setSpacing(30)

        self.droparea = DropArea()
        vbox.addWidget(self.droparea)

        load_box = QHBoxLayout()
        self.load_push_button = QPushButton("or load...")
        load_box.addWidget(self.load_push_button)

        value_name_box = QHBoxLayout()
        value_name_label = QLabel("value name")
        value_name_box.addWidget(value_name_label)
        self.value_name_text = QLineEdit()
        value_name_box.addWidget(self.value_name_text)

        converting_form_box = QHBoxLayout()
        converting_form_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        from_label = QLabel("from")
        to_label = QLabel("to")
        to_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.from_combo = QComboBox()
        self.from_combo.addItems(expressions)
        self.to_combo = QComboBox()
        self.to_combo.addItems(expressions)
        converting_form_box.addWidget(from_label)
        converting_form_box.addWidget(self.from_combo)
        converting_form_box.addWidget(to_label)
        converting_form_box.addWidget(self.to_combo)

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.on_convert_push_button_clicked)

        vbox.addLayout(load_box)
        vbox.addLayout(value_name_box)
        vbox.addLayout(converting_form_box)
        vbox.addWidget(self.convert_button)

    def center(self) -> None:
        '''
            move widget to center of screen
        '''
        frame = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        frame.moveCenter(cp)
        self.move(frame.topLeft())

    def set_presenter(self, presenter: 'ConverterPresenter') -> None:
        '''
            set presenter
        '''
        self.presenter = presenter

    def set_droparea_imported(self) -> None:
        '''
            change droparea text to "imported"
        '''
        self.droparea.setText("imported")
    
    def set_to_combo_items(self, items: list[str]) -> None:
        '''
            set to_combo items
        '''
        self.to_combo.clear()
        self.to_combo.addItems(items)

    def show_alert_message(self, message: str) -> None:
        '''
            show alert message to user
        '''
        QMessageBox.information(self, message, message)

    @asyncSlot()
    async def on_convert_push_button_clicked(self) -> None:
        '''
            proxy for ConvertPresenter.on_convert_button_clicked()
        '''
        await self.presenter.on_convert_button_clicked()
