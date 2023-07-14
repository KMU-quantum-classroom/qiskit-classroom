'''
    presenter for converter view
'''

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
