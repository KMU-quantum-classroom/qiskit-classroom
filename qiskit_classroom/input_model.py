"""moudle for input data classes"""
import random
import string


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


class QuantumCircuitInput(Input):
    """user input value for QuantumCircuit"""

    def __init__(self, value_name: str) -> None:
        super().__init__()
        self.value_name = value_name

    def __str__(self) -> str:
        return "value_name : " + self.value_name


class DiracInput(Input):
    """user input value for Dirac notation"""


class MatrixInput(Input):
    """user input value for Matrix"""

    def __init__(self, num_cubit: int, do_measure: bool) -> None:
        super().__init__()
        self.value_name = "".join(
            random.choice(string.ascii_letters) for _ in range(10)
        )
        self.num_cubit = num_cubit
        self.do_measure = do_measure
