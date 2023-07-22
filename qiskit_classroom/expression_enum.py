"""
    module for Expression enum
"""


import enum


class QuantumExpression(enum.Enum):
    """
    Quantum expression enumerate
    """

    CIRCUIT = (1, "QC")
    DIRAC = (2, "BRA_KET")
    MATRIX = (3, "MATRIX")
    NONE = -1


expressions = [expression.name for expression in QuantumExpression]
