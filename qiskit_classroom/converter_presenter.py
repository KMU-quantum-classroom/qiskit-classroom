"""
    presenter for converter view
"""

from typing import TYPE_CHECKING
from .expression_enum import QuantumExpression, expressions

if TYPE_CHECKING:
    from .converter_model import ConverterModel
    from .converter_view import ConverterView, FileList


class ConverterPresenter:
    """
    presenter for converter
    """

    def __init__(self, view: "ConverterView", model: "ConverterModel") -> None:
        self.view = view
        self.view.set_presenter(self)
        self.model = model
        self.model.from_expression = QuantumExpression.CIRCUIT
        self.view.from_combo.currentTextChanged.connect(self.on_from_combo_changed)
        self.view.to_combo.currentTextChanged.connect(self.on_to_combo_changed)
        self.view.value_name_text.textChanged.connect(self.on_value_name_changed)
        self.view.droparea.file_imported.connect(self.on_file_path_droped)

    def on_filepath_inputed(self, filepath: str) -> None:
        """update sourcecode_path

        Args:
            filepath (str): filepath from view
        """
        self.model.sourcecode_path = filepath
        self.view.set_droparea_imported(self.model.sourcecode_path)

    def on_from_combo_changed(self) -> None:
        """
        update from_expression
        """
        self.model.from_expression = QuantumExpression[
            self.view.from_combo.currentText()
        ]
        if self.model.from_expression == QuantumExpression.MATRIX:
            self.view.set_to_combo_items([QuantumExpression.CIRCUIT.name])
        else:
            self.view.set_to_combo_items(expressions)

    def on_to_combo_changed(self) -> None:
        """
        update to_expression
        """
        if len(self.view.to_combo.currentText()) == 0:
            self.model.to_experssion = QuantumExpression.CIRCUIT
        else:
            self.model.to_experssion = QuantumExpression[
                self.view.to_combo.currentText()
            ]

    def on_value_name_changed(self) -> None:
        """
        update expression_value_name
        """
        self.model.expression_value_name = self.view.value_name_text.text()

    def on_file_path_droped(self, files: "FileList") -> None:
        """Choose the first one among multiple file addresses that end with .py

        Args:
            files (FileList): multiple file address
        """
        for file in files.files:
            if file.endswith(".py"):
                self.model.sourcecode_path = file
                self.view.set_droparea_imported(file)
                break

    async def on_convert_button_clicked(self) -> None:
        """
        convert expression and visualiazation.
        update result file path
        """
        print("hello")
        await asyncio.sleep(0.5)
        self.view.show_alert_message("dd")
        print("world")
        self.model.result_img_path = await self.model.convert_and_draw()
