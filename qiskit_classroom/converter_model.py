'''
    module for ConverterModel
'''


from .expression_enum import QuantumExpression


class ConvertingRuleException(Exception):
    '''
    Exception class for converting rule
    matrix cannot convert to dirac notation directly
    '''
    def __init__(self) -> None:
        super().__init__("Expression converting rule error: Matrix cannot convert to dirac Notation directly.")


class ConverterModel():
    '''
    class for converter
    '''
    __from_expression: QuantumExpression
    __to_expression: QuantumExpression
    __expression_value_name: str
    __sourcecode_path: str
    __result_img_path: str

    def __init__(self) -> None:
        self.__from_expression = QuantumExpression.NONE
        self.__to_expression = QuantumExpression.NONE
        self.__expression_value_name = None
        self.__sourcecode_path = None
        self.__result_img_path = None

    @property
    def from_expression(self) -> QuantumExpression:
        '''
        property of __from_expression
        '''
        return self.__from_expression

    @from_expression.setter
    def from_expression(self, value: QuantumExpression) -> None:
        if value is QuantumExpression.MATRIX and self.__to_expression is QuantumExpression.DIRAC:
            raise ConvertingRuleException()

        self.__from_expression = value

    @property
    def to_expression(self) -> QuantumExpression:
        '''
        property of __to_expression
        '''
        return self.__to_expression

    @to_expression.setter
    def to_experssion(self, value: QuantumExpression) -> None:
        # cannot converte from matrix to dirac dicrectly
        if value is QuantumExpression.DIRAC and self.__from_expression is QuantumExpression.MATRIX:
            raise ConvertingRuleException()

        self.__to_expression = value

    @property
    def expression_value_name(self) -> str:
        '''
        property of __expresion_value_name
        '''
        return self.__expression_value_name

    @expression_value_name.setter
    def expression_value_name(self, value: str) -> None:
        self.__expression_value_name = value

    @property
    def sourcecode_path(self) -> str:
        '''
        property of __sourcecode_path
        '''
        return self.__sourcecode_path

    @sourcecode_path.setter
    def soucecode_path(self, value: str) -> None:
        self.__sourcecode_path = value

    @property
    def result_img_path(self) -> str:
        '''
        property of __result_img_path
        '''
        return self.__result_img_path

    @result_img_path.setter
    def result_img_path(self, value: str) -> str:
        self.__result_img_path = value

    async def convert_and_draw(self) -> None:
        '''
            convert expression and draw by subprocess
        '''
        raise NotImplementedError()
