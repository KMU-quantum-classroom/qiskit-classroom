"""
    conveter view class
"""


from typing import TYPE_CHECKING
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
)
from qasync import asyncSlot
from qiskit_classroom.expression_enum import expressions


if TYPE_CHECKING:
    from .converter_presenter import ConverterPresenter


class FileList:
    """
    file name list for drop event
    """
    def __init__(self, files: list[str]) -> None:
        self.files = files


class DropArea(QLabel):
    """
    file drop area widget
    """

    file_imported = pyqtSignal(FileList)

    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        self.setAcceptDrops(True)
        self.set_ui()

    def set_ui(self) -> None:
        """
        set UI
        """
        self.setWordWrap(True)
        self.setFixedHeight(250)
        self.setStyleSheet(
            "border-style: dashed; border-width: 2px; color: blue; border-color: red;"
        )
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("drop .py file here")

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """
        handle drag event and accept only url
        """
        if event.mimeData().hasUrls():
            event.accept()
            self.setText("drop here")
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        """
        handle drop event and emit file imported event
        """
        if event.mimeData().hasUrls():
            files = [u.toLocalFile() for u in event.mimeData().urls()]
            self.file_imported.emit(FileList(files=files))
            event.accept()


class ConverterView(QWidget):
    """
    converter view class
    """

    def __init__(self) -> None:
        super().__init__()
        self.presenter = None
        self.set_ui()
        self.center()
        self.setAcceptDrops(True)

    def set_ui(self) -> None:
        """
        set UI
        """
        self.setWindowTitle("Converter")
        self.setContentsMargins(50, 50, 50, 50)
        self.setFixedSize(QSize(500, 600))

        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.setSpacing(30)

        self.droparea = DropArea(self)
        vbox.addWidget(self.droparea)

        load_box = QHBoxLayout()
        self.load_push_button = QPushButton("or load...")
        self.load_push_button.clicked.connect(self.on_file_load_clicked)
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
        """
        move widget to center of screen
        """
        frame = self.frameGeometry()
        center_position = self.screen().availableGeometry().center()

        frame.moveCenter(center_position)
        self.move(frame.topLeft())

    def on_file_load_clicked(self) -> None:
        """
        handling file dialog
        """
        filename = QFileDialog.getOpenFileName(
            self, "Open .py", "", "python3 script (*.py)"
        )[0]
        self.presenter.on_filepath_inputed(filename)

    def set_presenter(self, presenter: "ConverterPresenter") -> None:
        """
        set presenter
        """
        self.presenter = presenter

    def set_droparea_imported(self, filepath: str) -> None:
        """
        change droparea text to "imported"
        """
        self.droparea.setText("imported: \n\n" + filepath)

    def set_to_combo_items(self, items: list[str]) -> None:
        """
        set to_combo items
        """
        self.to_combo.clear()
        self.to_combo.addItems(items)

    def show_alert_message(self, message: str) -> None:
        """
        show alert message to user
        """
        QMessageBox.information(self, message, message)

    @asyncSlot()
    async def on_convert_push_button_clicked(self) -> None:
        """
        proxy for ConvertPresenter.on_convert_button_clicked()
        """
        await self.presenter.on_convert_button_clicked()
