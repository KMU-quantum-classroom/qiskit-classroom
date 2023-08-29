"""
    module for ConverterModel
"""

import os
from .expression_enum import QuantumExpression
from .worker import ConverterWorker
from .input_model import Input


class ConvertingRuleException(Exception):
    """
    Exception class for converting rule
    matrix cannot convert to dirac notation directly
    """

    def __init__(self) -> None:
        super().__init__(
            "Expression converting rule error: Matrix cannot convert to dirac Notation directly."
        )


# pylint: disable=too-many-instance-attributes
class ConverterModel:
    """
    class for converter
    """

    def __init__(self) -> None:
        self.__from_expression = None
        self.__to_expression = None
        self.__result_img_path = ""
        self.__input_data = None
        self.__expression_text = ""

    @property
    def from_expression(self) -> QuantumExpression:
        """
        property of __from_expression
        """
        return self.__from_expression

    @from_expression.setter
    def from_expression(self, value: QuantumExpression) -> None:
        if (
            value is QuantumExpression.MATRIX
            and self.__to_expression is QuantumExpression.DIRAC
        ):
            raise ConvertingRuleException()

        self.__from_expression = value
        print(f"from expression changed to {value}")

    @property
    def to_expression(self) -> QuantumExpression:
        """
        property of __to_expression
        """
        return self.__to_expression

    @to_expression.setter
    def to_experssion(self, value: QuantumExpression) -> None:
        # cannot converte from matrix to dirac dicrectly
        if (
            value is QuantumExpression.DIRAC
            and self.__from_expression is QuantumExpression.MATRIX
        ):
            raise ConvertingRuleException()

        self.__to_expression = value
        print(f"to exression changed to {value}")

    @property
    def result_img_path(self) -> str:
        """property of __result_img_path

        Returns:
            str: result_img_path
        """

        return self.__result_img_path

    @result_img_path.setter
    def result_img_path(self, value: str) -> None:
        self.__result_img_path = value
        print(f"result img path change to {value}")

    @property
    def input_data(self) -> Input:
        """property of __input_date

        Returns:
            Input: user input data
        """
        return self.__input_data

    @input_data.setter
    def input_data(self, value: Input) -> None:
        self.__input_data = value
        print(f"input_data change to {value}")

    @property
    def expression_text(self) -> str:
        """property of __expression_text

        Returns:
            str: expression text
        """
        return self.__expression_text

    @expression_text.setter
    def expression_text(self, value: str) -> None:
        self.__expression_text = value
        print(f"expression_text change to {value}")

    async def convert_and_draw(self) -> bool:
        """run worker to converting expression and visualizating expression

        Returns:
            bool: if converting and drawing was success return true
        """

        worker = ConverterWorker(
            self.from_expression,
            self.to_experssion,
            self.input_data,
            self.expression_text,
        )
        img_path = await worker.run()

        # replace image and remove previously generated image
        if img_path is not None:
            self.remove_result_img_path()
            self.result_img_path = img_path
        return True

    def remove_result_img_path(self) -> None:
        """remove generated img file"""
        if self.__result_img_path is not None:
            if os.path.isfile(self.__result_img_path):
                os.remove(self.__result_img_path)
                print(f"remove {self.result_img_path}")
