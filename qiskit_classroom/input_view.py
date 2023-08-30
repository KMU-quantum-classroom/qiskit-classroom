"""Widget for converting informations"""

# pylint: disable=no-name-in-module
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QFileDialog,
    QCheckBox,
)
from PySide6.QtCore import Qt, Signal

from .expression_enum import QuantumExpression
from .input_model import Input, QuantumCircuitInput, DiracInput, MatrixInput


EXPRESSION_PLACEHOLDERS: dict[QuantumExpression:str] = {
    QuantumExpression.CIRCUIT: """from qiskit import QuantumCircuit
quantum_circuit = QuantumCircuit(2, 2)
quantum_circuit.x(0)
quantum_circuit.cx(0, 1)
""",
    QuantumExpression.DIRAC: "sqrt(2)*|00>/2+sqrt(2)*|11>/2",
    QuantumExpression.MATRIX: """[[1, 0, 0, 0],
[0, 0, 0, 1],
[0, 0, 1, 0],
[0, 1, 0, 0]]""",
    QuantumExpression.NONE: "",
}


class ExpressionPlainText(QPlainTextEdit):
    """
    ExpressionPlainText
    """

    file_dropped = Signal(object)

    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        self.setAcceptDrops(True)
        self.set_ui()

    def set_ui(self) -> None:
        """
        set UI
        """
        self.setFixedHeight(250)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        # pylint: disable=invalid-name
        """
        handle drag event and accept only url
        """
        if event.mimeData().hasUrls():
            event.accept()
            self.setText("drop here")
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        # pylint: disable=invalid-name
        """
        handle drop event and emit file imported event
        """
        if event.mimeData().hasUrls():
            files = [u.toLocalFile() for u in event.mimeData().urls()]
            self.file_dropped.emit(files)
            event.accept()

    def set_placeholder_text(self, expression: QuantumExpression) -> None:
        """set placeholder for expression plain text

        Args:
            expression (QuantumExpression): selection
        """
        self.setPlaceholderText("")
        self.setPlaceholderText(EXPRESSION_PLACEHOLDERS[expression])


class InputWidget(QWidget):
    """Widget group for certain input"""

    def set_ui(self) -> None:
        """show widgets"""

    def get_input(self) -> Input:
        """return user input

        Returns:
            Input: user input class
        """
        return Input


class QuantumCircuitInputWidget(InputWidget):
    """Widget group for QuantumCircuit Input"""

    file_imported = Signal(str)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.set_ui()

    def set_ui(self):
        """set ui for QuantumCircuitInputWidget"""
        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        value_name_box = QHBoxLayout()
        value_name_label = QLabel("value name")
        value_name_box.addWidget(value_name_label)
        self.value_name_text = QLineEdit()
        self.value_name_text.setPlaceholderText("input value name of quantum circuit")
        value_name_box.addWidget(self.value_name_text)

        load_box = QHBoxLayout()
        load_box.addStretch()
        self.load_push_button = QPushButton("or load...")
        self.load_push_button.setMinimumWidth(150)
        self.load_push_button.clicked.connect(self.on_file_load_clicked)
        load_box.addWidget(self.load_push_button)

        vbox.addLayout(value_name_box)
        vbox.addLayout(load_box)

    def on_file_load_clicked(self) -> None:
        """
        handling file dialog
        """
        filename = QFileDialog.getOpenFileName(
            self, "Open .py", "", "python3 script (*.py)"
        )[0]
        self.file_imported.emit(filename)

    def get_input(self) -> QuantumCircuitInput:
        user_input = QuantumCircuitInput(
            self.value_name_text.text().strip(),
        )
        return user_input


class DiracInputWidget(InputWidget):
    """Widget group for Dirac Notaion input"""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.set_ui()

    def get_input(self) -> DiracInput:
        return DiracInput()


class MatrixInputWidget(InputWidget):
    """Widget group for matrix input"""

    matrix_plain_text: QPlainTextEdit
    num_cubit_text: QLineEdit
    do_measure_checkbox: QCheckBox

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.set_ui()

    def set_ui(self):
        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        hbox = QHBoxLayout(self)
        num_cubit_label = QLabel("number of cubit")
        self.num_cubit_text = QLineEdit(self)
        self.num_cubit_text.setToolTip("input 3 digits number")
        self.do_measure_checkbox = QCheckBox("do measure this circuit?", self)
        self.do_measure_checkbox.setToolTip("do measure all qubits")

        hbox.addWidget(num_cubit_label)
        hbox.addWidget(self.num_cubit_text)
        hbox.addWidget(self.do_measure_checkbox)
        vbox.addLayout(hbox)

    def get_input(self) -> Input:
        return MatrixInput(
            int(self.num_cubit_text.text()), self.do_measure_checkbox.isChecked()
        )
