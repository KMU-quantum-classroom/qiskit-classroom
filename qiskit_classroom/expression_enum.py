"""
    module for Expression enum
"""


import enum


class QuantumExpression(enum.Enum):
    """
    Quantum expression enumerate
    """

    CIRCUIT = (1,)
    DIRAC = (2,)
    MATRIX = (3,)
    NONE = -1


expressions = [expression.name for expression in QuantumExpression]
