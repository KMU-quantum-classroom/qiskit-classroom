"""
module
"""
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


class SingleCircuit:
    """class"""

    def __init__(self):
        """init"""
        self.simulator = AerSimulator()
        self.circuit = QuantumCircuit(1, 1)
        self.circuit.metadata = {}

    def x_gate(self):
        """
        x gate
        :return:
        """
        self.circuit.x(0)

    def measure(self):
        """
        measure
        :return:
        """
        self.circuit.measure(0, 0)

    def __transpile(self):
        """
        __transpile
        :return:
        """
        return transpile(self.circuit, self.simulator)

    def create_job(self):
        """
        create_job
        :return:
        """
        job = self.simulator.run(self.__transpile(), shots=1000)
        result = job.result()
        counts = result.get_counts(self.__transpile())
        return counts
