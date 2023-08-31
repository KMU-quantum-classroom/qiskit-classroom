"""unittest for converter model"""
import unittest
from qiskit_classroom.converter_model import ConverterModel, ConvertingRuleException
from qiskit_classroom.expression_enum import QuantumExpression


class TestConverterModel(unittest.TestCase):
    """unittest class for ConverterModel"""

    def setUp(self) -> None:
        self.model = ConverterModel()
        return super().setUp()

    def test_from_expression_setter(self) -> None:
        """testing setter raise ConvertingRuleException when model is MATRIX and DIRAC"""
        self.model.to_expression = QuantumExpression.DIRAC
        with self.assertRaises(ConvertingRuleException):
            self.model.from_expression = QuantumExpression.MATRIX

    def test_to_expression_setter(self) -> None:
        """testing setter raise ConvertingRuleException when model is MATRIX and DIRAC"""
        self.model.from_expression = QuantumExpression.MATRIX
        with self.assertRaises(ConvertingRuleException):
            self.model.to_expression = QuantumExpression.DIRAC
