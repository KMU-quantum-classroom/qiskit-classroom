'''
    presenter for converter view
'''


import asyncio
from typing import TYPE_CHECKING
from .expression_enum import QuantumExpression, expressions

if TYPE_CHECKING:
    from .converter_model import ConverterModel
    from .converter_view import ConverterView


class ConverterPresenter():
    '''
        presenter for converter
    '''

    def __init__(self, view: 'ConverterView', model: 'ConverterModel') -> None:
        self.view = view
        self.view.set_presenter(self)
        self.model = model
        self.view.from_combo.currentTextChanged.connect(self.on_from_combo_changed)

    def on_filepath_inputed(self, filepath: str) -> None:
        self.model.soucecode_path = filepath
        self.view.set_droparea_imported()

    def on_from_combo_changed(self) -> None:
        '''
            
        '''
        self.model.from_expression = self.view.from_combo.currentText()
        if self.model.from_expression == QuantumExpression.MATRIX.name:
            self.view.set_to_dropdowm_items([QuantumExpression.CIRCUIT.name])
        else:
            self.view.set_to_dropdowm_items(expressions)

    def on_to_combo_changed(self) -> None:
        '''
            
        '''
        self.model.to_experssion = self.view.to_combo.currentText()