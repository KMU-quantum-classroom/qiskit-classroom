"""
    conveter view class
"""


from typing import TYPE_CHECKING

# pylint: disable=no-name-in-module
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QProgressDialog,
    QCheckBox,
)


from qasync import asyncSlot
from qiskit_classroom.expression_enum import (
    expressions,
    Converting_method,
    QuantumExpression,
)
from qiskit_classroom.result_image_dialog import ResultImageDialog
from qiskit_classroom.input_view import (
    ExpressionPlainText,
    QuantumCircuitInputWidget,
    DiracInputWidget,
    MatrixInputWidget,
    Input,
    InputWidget,
)


if TYPE_CHECKING:
    from .converter_presenter import ConverterPresenter


# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods
class ConverterView(QWidget):
    """
    converter view class
    """

    from_combo_currentTextChanged = Signal()
    to_combo_currentTextChanged = Signal()
    file_dropped = Signal(object)
    file_imported = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.presenter = None
        self.currently_showing_input = QuantumExpression.NONE
        self.set_ui()
        self.center()
        self.setAcceptDrops(True)

    def set_ui(self) -> None:
        """
        set UI
        """
        self.setWindowTitle("Converter")
        self.setContentsMargins(50, 50, 50, 50)
        self.setMinimumSize(QSize(500, 700))

        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.setSpacing(30)

        self.expression_plain_text = ExpressionPlainText(self)
        self.expression_plain_text.file_dropped.connect(self.__on_file_dropped)
        vbox.addWidget(self.expression_plain_text)

        converting_form_box = QHBoxLayout()
        converting_form_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        from_label = QLabel("from")
        to_label = QLabel("to")
        to_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.from_combo = QComboBox()
        self.from_combo.addItems(expressions)
        self.from_combo.setCurrentIndex(3)
        self.from_combo.currentTextChanged.connect(
            self.__on_from_combo_current_text_changed
        )
        self.to_combo = QComboBox()
        self.to_combo.addItem(Converting_method[QuantumExpression.NONE][0].name)
        self.to_combo.setMinimumContentsLength(len(QuantumExpression.CIRCUIT.name))
        self.to_combo.currentIndexChanged.connect(
            self.__on_to_combo_current_text_changed
        )
        converting_form_box.addWidget(from_label)
        converting_form_box.addWidget(self.from_combo)
        converting_form_box.addWidget(to_label)
        converting_form_box.addWidget(self.to_combo)

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.on_convert_push_button_clicked)

        self.inputs: dict[QuantumExpression, InputWidget] = {
            QuantumExpression.CIRCUIT: QuantumCircuitInputWidget(self),
            QuantumExpression.MATRIX: MatrixInputWidget(self),
            QuantumExpression.DIRAC: DiracInputWidget(self),
        }
        vbox.addLayout(converting_form_box)
        for expression, input_widget in self.inputs.items():
            if expression is QuantumExpression.CIRCUIT:
                input_widget: QuantumCircuitInputWidget = input_widget
                input_widget.file_imported.connect(self.__on_file_imported)
            vbox.addWidget(input_widget)
            input_widget.hide()

        self.shows_results = QCheckBox("let result state show?")
        vbox.addWidget(self.shows_results)

        vbox.addWidget(self.convert_button)
        vbox.addSpacing(50)

        self.progress_bar = QProgressDialog(
            "wait for progressing", "abort", 0, 0, parent=self
        )
        self.progress_bar.setMinimumWidth(300)
        self.progress_bar.setCancelButton(None)
        self.progress_bar.setWindowTitle("now converting")
        self.progress_bar.close()

    def connect_signal(self) -> None:
        """connect signals to presenters slots"""
        self.from_combo_currentTextChanged.connect(self.presenter.on_from_combo_changed)
        self.to_combo_currentTextChanged.connect(self.presenter.on_to_combo_changed)
        self.file_dropped.connect(self.presenter.on_file_dropped)
        self.file_imported.connect(self.presenter.on_file_imported)

    def center(self) -> None:
        """
        move widget to center of screen
        """
        frame = self.frameGeometry()
        center_position = self.screen().availableGeometry().center()

        frame.moveCenter(center_position)
        self.move(frame.topLeft())

    def __on_from_combo_current_text_changed(self) -> None:
        self.from_combo_currentTextChanged.emit()

    def disable_from_combo_current_text_change(self) -> None:
        """disable event handling from_combo_currentTextChanged"""
        self.from_combo_currentTextChanged.disconnect()

    def enable_from_combo_current_text_change(self) -> None:
        """endable event handling from_combo_currentTextChanged"""
        self.from_combo_currentTextChanged.connect(self.presenter.on_from_combo_changed)

    def __on_to_combo_current_text_changed(self) -> None:
        self.to_combo_currentTextChanged.emit()

    def disable_to_combo_current_text_change(self) -> None:
        """disable event handling to_combo_currentTextChanged"""
        self.to_combo_currentTextChanged.disconnect()

    def enable_to_combo_current_text_change(self) -> None:
        """endable event handling to_combo_currentTextChanged"""
        self.to_combo_currentTextChanged.connect(self.presenter.on_to_combo_changed)

    def __on_file_dropped(self, file_paths: list[str]) -> None:
        self.file_dropped.emit(file_paths)

    def __on_file_imported(self, file_path: str) -> None:
        self.file_imported.emit(file_path)

    def get_to_expression(self) -> str:
        """return to_combo current text

        Returns:
            str: current to_combo text
        """
        return self.to_combo.currentText()

    def get_from_expression(self) -> str:
        """return from_combo current text

        Returns:
            str: current from_combo text
        """
        return self.from_combo.currentText()

    def get_input(self, expression_selection: QuantumExpression) -> Input:
        """return Input class

        Args:
            expression (QuantumExpression): selection for expression

        Returns:
            Input: user input class QuantumCircuitInput for QuantumCircuit, MatrixInput for Matrix
            and DiracInput for Dirac noation
        """
        return self.inputs[expression_selection].get_input()

    def show_input_widget(self, expression_selection: QuantumExpression) -> None:
        """show input widget

        Args:
            expression_selection (QuantumExpression): select what want to show
        """
        for expression, input_widget in self.inputs.items():
            if expression is expression_selection:
                input_widget.show()
            else:
                input_widget.hide()

    def set_placeholder(self, expression: QuantumExpression) -> None:
        """set placehoder for expression_plain_text

        Args:
            expression (QuantumExpression): QuantumExpression enum
        """
        self.expression_plain_text.set_placeholder_text(expression=expression)

    def clear_expression_plain_text(self) -> None:
        """clear expression_plain_text"""
        self.expression_plain_text.clear()

    def set_from_combo_current_index(self, index: int) -> None:
        """set from combo current index by \"index\"

        Args:
            index (int): index
        """
        self.from_combo.setCurrentIndex(index)

    def set_expression_plain_text_text(self, text: str) -> None:
        """set expression_pain_text text

        Args:
            text (str): text
        """
        self.expression_plain_text.setPlainText(text)

    def get_expression_plain_text_text(self) -> str:
        """return expresion_plain_text text

        Returns:
            str: plainText
        """
        return self.expression_plain_text.toPlainText()

    def set_presenter(self, presenter: "ConverterPresenter") -> None:
        """set presenter

        Args:
            presenter (ConverterPresenter): presenter for ConverterView
        """
        self.presenter = presenter
        self.connect_signal()

    def set_to_combo_items(self, items: list[str]) -> None:
        """set to_combo items

        Args:
            items (list[str]): string items
        """
        self.to_combo.clear()
        self.to_combo.addItems(items)

    def get_shows_result(self) -> bool:
        """return show_result checked

        Returns:
            bool: show_result
        """

        return self.shows_results.isChecked()

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
