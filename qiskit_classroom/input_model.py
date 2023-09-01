"""moudle for input data classes"""
import random
import string


# pylint: disable=too-few-public-methods
class Input:
    """contain user input value"""

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        """return contents

        Returns:
            str: contents
        """
        return ""


# pylint: disable=too-few-public-methods
class QuantumCircuitInput(Input):
    """user input value for QuantumCircuit"""

    def __init__(self, value_name: str) -> None:
        super().__init__()
        self.value_name = value_name

    def __str__(self) -> str:
        return "value_name : " + self.value_name


# pylint: disable=too-few-public-methods
class DiracInput(Input):
    """user input value for Dirac notation"""


# pylint: disable=too-few-public-methods
class MatrixInput(Input):
    """user input value for Matrix"""

    def __init__(self, num_qubits: int, do_measure: bool) -> None:
        super().__init__()
        self.value_name = "".join(
            random.choice(string.ascii_letters) for _ in range(10)
        )
        self.num_qubits = num_qubits
        self.do_measure = do_measure
