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


expressions: list[str] = [expression.name for expression in QuantumExpression]
Converting_method: dict[QuantumExpression, list[QuantumExpression]] = {
    QuantumExpression.NONE: [QuantumExpression.NONE],
    QuantumExpression.CIRCUIT: [
        QuantumExpression.DIRAC,
        QuantumExpression.MATRIX,
    ],
    QuantumExpression.MATRIX: [QuantumExpression.CIRCUIT],
    QuantumExpression.DIRAC: [QuantumExpression.MATRIX],
}
