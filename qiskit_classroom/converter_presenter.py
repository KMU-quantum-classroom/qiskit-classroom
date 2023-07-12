'''
    presenter for converter view
'''

from .converter_view import ConverterView
from .converter_model import ConverterModel


class ConverterPresenter():
    '''
        presenter for converter
    '''

    model: ConverterModel
    view: ConverterView

    def __init__(self, view: ConverterView, model: ConverterModel) -> None:
        self.view = view
        self.model = model
