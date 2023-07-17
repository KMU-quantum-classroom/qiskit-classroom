"""
    presenter for converter view
"""


import asyncio
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
        self.view.from_combo.currentTextChanged.connect(self.on_from_combo_changed)
        self.view.to_combo.currentTextChanged.connect(self.on_to_combo_changed)
        self.view.value_name_text.textChanged.connect(self.on_value_name_changed)
        self.view.droparea.file_imported.connect(self.on_file_path_droped)

    def on_filepath_inputed(self, filepath: str) -> None:
        """
        update sourcecode_path
        """
        self.model.soucecode_path = filepath
        self.view.set_droparea_imported(self.model.sourcecode_path)

    def on_from_combo_changed(self) -> None:
        """
        update from_expression
        """
        self.model.from_expression = self.view.from_combo.currentText()
        if self.model.from_expression == QuantumExpression.MATRIX.name:
            self.view.set_to_combo_items([QuantumExpression.CIRCUIT.name])
        else:
            self.view.set_to_combo_items(expressions)

    def on_to_combo_changed(self) -> None:
        """
        update to_expression
        """
        self.model.to_experssion = self.view.to_combo.currentText()

    def on_value_name_changed(self) -> None:
        """
        update expression_value_name
        """
        self.model.expression_value_name = self.view.value_name_text.text()

    def on_file_path_droped(self, files: "FileList") -> None:
        """
        update sourcecode_path
        """
        for file in files.files:
            print(file)

    async def on_convert_button_clicked(self) -> None:
        """
        convert expression and visualiazation
        update result file path
        """
        print("hello")
        await asyncio.sleep(0.5)
        self.view.show_alert_message("dd")
        print("world")
        await self.model.convert_and_draw()
