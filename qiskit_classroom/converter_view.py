"""
    conveter view class
"""


from typing import TYPE_CHECKING

# pylint: disable=no-name-in-module
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QProgressDialog,
)

from qiskit_class_converter import (
    __FULL_VERSION__ as qiskit_classroom_converter_version,
)
from qasync import asyncSlot
from qiskit_classroom.expression_enum import (
    expressions,
    Converting_method,
    QuantumExpression,
)
from qiskit_classroom.result_image_dialog import ResultImageDialog


if TYPE_CHECKING:
    from .converter_presenter import ConverterPresenter


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
        self.setMinimumSize(QSize(500, 600))

        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.setSpacing(30)

        self.droparea = DropArea(self)
        vbox.addWidget(self.droparea)

        load_box = QHBoxLayout()
        load_box.addStretch()
        self.load_push_button = QPushButton("or load...")
        self.load_push_button.setMinimumWidth(150)
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
        self.from_combo.setCurrentIndex(3)
        self.to_combo = QComboBox()
        self.to_combo.addItem(Converting_method[QuantumExpression.NONE][0].name)
        self.to_combo.setMinimumContentsLength(len(QuantumExpression.CIRCUIT.name))
        converting_form_box.addWidget(from_label)
        converting_form_box.addWidget(self.from_combo)
        converting_form_box.addWidget(to_label)
        converting_form_box.addWidget(self.to_combo)

        # todo add ask dialog
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.on_convert_push_button_clicked)

        version_label = QLabel(
            f"Run on [{QISKIT_CLASSROOM_CONVERTER_VERSION_STR}]", self
        )

        vbox.addLayout(load_box)
        vbox.addLayout(value_name_box)
        vbox.addLayout(converting_form_box)
        vbox.addWidget(self.convert_button)
        vbox.addWidget(version_label)

        # todo add abort feature
        self.progress_bar = QProgressDialog(
            "wait for progressing", "abort", 0, 0, parent=self
        )
        self.progress_bar.close()

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
        """set presenter

        Args:
            presenter (ConverterPresenter): presenter for ConverterView
        """
        self.presenter = presenter

    def set_droparea_imported(self, filepath: str) -> None:
        """change droparea text to "imported"

        Args:
            filepath (str): imported file path
        """

        self.droparea.setText("imported: \n\n" + filepath)

    def set_to_combo_items(self, items: list[str]) -> None:
        """set to_combo items

        Args:
            items (list[str]): string items
        """
        self.to_combo.clear()
        self.to_combo.addItems(items)

    def show_alert_message(self, message: str) -> None:
        """show alert message to user

        Args:
            message (str): message
        """
        QMessageBox.information(self, message, message)

    @asyncSlot()
    async def on_convert_push_button_clicked(self) -> None:
        """
        proxy for ConvertPresenter.on_convert_button_clicked()
        """
        await self.presenter.on_convert_button_clicked()

    def show_progress_bar(self) -> None:
        """
        show progress bar to user. show progress to user!
        """
        self.progress_bar.show()

    def close_progress_bar(self) -> None:
        """
        close progress bar dialog
        """
        self.progress_bar.close()

    def show_confirm_dialog(self) -> None:
        """take confirm to conversion"""
        result = QMessageBox.question(
            self, "Do convert?", "Conversion will process are you sure?"
        )

        if result == QMessageBox.StandardButton.Yes:
            self.on_convert_push_button_clicked()

    def show_result_image(self, image_path: str) -> None:
        """show result image by ResultImageDialog

        Args:
            image_path (str): image path want to show
        """
        ResultImageDialog(self).show_image(image_path=image_path)
