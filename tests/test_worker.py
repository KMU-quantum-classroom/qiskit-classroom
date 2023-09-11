"""test worker.py"""

#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import unittest
from unittest import mock
from qiskit_classroom.expression_enum import QuantumExpression
from qiskit_classroom.worker import ConverterWorker
from qiskit_classroom.input_model import QuantumCircuitInput, MatrixInput

VALUE_NAME = "value_name"
QUANTUM_CIRCUIT_CODE = """from qiskit import QuantumCircuit

quantum_circuit = QuantumCircuit(2, 2)
quantum_circuit.x(0)
quantum_circuit.cx(0, 1)"""

MATRIX_CODE = """[[1, 0, 0, 0],
[0, 0, 0, 1],
[0, 0, 1, 0],
[0, 1, 0, 0]]"""

RANDOM_FILE_NAME = "random_file_name"


QC_TO_MATRIX_EXPECTED = [
    "converter = ConversionService(conversion_type='QC_TO_MATRIX',"
    + " option={'print': 'raw'})\n"
    + f"result = converter.convert(input_value={VALUE_NAME})",
    "for gate, name in zip(result['gate'], result['name']):\n"
    + "\tprint(f'{gate.strip()}_{{{name}}}')",
]

MATRIX_TO_QC_EXPECTED = [
    "converter = ConversionService(conversion_type='MATRIX_TO_QC',"
    + " option={'label': 'unitary gate'})\n"
    + "from qiskit import QuantumCircuit\n"
    + f"""result = converter.convert(input_value={VALUE_NAME})
quantum_circuit = QuantumCircuit(2)
quantum_circuit.append(result, list(range(result.num_qubits)))
quantum_circuit.measure_all()""",
    f"""quantum_circuit.draw(output="mpl").savefig("{RANDOM_FILE_NAME + ".png"}", """
    + """bbox_inches="tight")""",
]


class ConverterWorkerTest(unittest.IsolatedAsyncioTestCase):
    """test converter worker"""

    def setUp(self):
        ConverterWorker.generate_random_file_name = mock.Mock(
            return_value=RANDOM_FILE_NAME
        )
        ConverterWorker.write_converting_code = mock.Mock(return_value=True)

        self.quantum_circuit_input = QuantumCircuitInput(VALUE_NAME)
        self.matrix_input = MatrixInput(2, True)
        self.matrix_input.value_name = VALUE_NAME

    def test_generate_conversion_code_quantum_circuit_to_matrix(self):
        """test generate_conversion_code
        Conversion method: QC_TO_MATRIX
        """
        worker = ConverterWorker(
            QuantumExpression.CIRCUIT,
            QuantumExpression.MATRIX,
            self.quantum_circuit_input,
            QUANTUM_CIRCUIT_CODE,
        )

        self.assertEqual(worker.generate_conversion_code(), QC_TO_MATRIX_EXPECTED[0])

    def test_generate_visualization_code_quantum_circuit_to_matrix(self):
        """test generate_visualization_code
        Conversion method: QC_TO_MATRIX
        """
        worker = ConverterWorker(
            QuantumExpression.CIRCUIT,
            QuantumExpression.MATRIX,
            self.quantum_circuit_input,
            QUANTUM_CIRCUIT_CODE,
        )

        self.assertEqual(worker.generate_visualization_code(), QC_TO_MATRIX_EXPECTED[1])

    def test_generate_conversion_code_matrix_to_quantum_circuit(self):
        """test generate_conversion_code
        Conversion method: MATRIX_TO_QC
        """
        worker = ConverterWorker(
            QuantumExpression.MATRIX,
            QuantumExpression.CIRCUIT,
            self.matrix_input,
            MATRIX_CODE,
        )

        self.assertEqual(worker.generate_conversion_code(), MATRIX_TO_QC_EXPECTED[0])

    def test_generate_visualiazation_code_matrix_to_quantum_circuit(self):
        """test generate_visualization_code
        Conversion method: MATRIX_TO_QC
        """
        worker = ConverterWorker(
            QuantumExpression.MATRIX,
            QuantumExpression.CIRCUIT,
            self.matrix_input,
            MATRIX_CODE,
        )

        self.assertEqual(worker.generate_visualization_code(), MATRIX_TO_QC_EXPECTED[1])

    def test_generate_conversion_code(self):
        """test generate_conversion_code
        test it return ""
        """
        worker = ConverterWorker(
            QuantumExpression.MATRIX, QuantumExpression.MATRIX, None, ""
        )
        self.assertEqual(worker.generate_conversion_code(), "")

    def test_generate_visualization_code(self):
        """test generated_visualization_code
        test case returns ""
        """
        worker = ConverterWorker(
            QuantumExpression.CIRCUIT, QuantumExpression.DIRAC, None, ""
        )
        self.assertEqual(worker.generate_visualization_code(), "print(result)")

        worker.to_expression = QuantumExpression.NONE

        self.assertEqual(worker.generate_visualization_code(), "")

        worker.to_expression = QuantumExpression.CIRCUIT
        worker.input_data = QuantumCircuitInput(VALUE_NAME)

        self.assertEqual(
            worker.generate_visualization_code(),
            f'{VALUE_NAME}.draw(output="mpl")'
            + f'.savefig("{RANDOM_FILE_NAME + ".png"}",'
            + 'bbox_inches="tight")',
        )
        worker.from_expression = QuantumExpression.MATRIX
        worker.to_expression = QuantumExpression.MATRIX
        worker.input_data: MatrixInput = MatrixInput(2, True)
        self.assertEqual(
            worker.generate_visualization_code(),
            f"print(array_to_latex({worker.input_data.value_name}, source=True))",
        )

    async def test_run_quantum_circuit_to_matrix(self):
        """test run method"""

        worker = ConverterWorker(
            QuantumExpression.CIRCUIT,
            QuantumExpression.MATRIX,
            self.quantum_circuit_input,
            QUANTUM_CIRCUIT_CODE,
        )
        worker.run_subprocess = mock.AsyncMock(return_value=(" ", " "))
        worker.cleanup = mock.Mock(return_value=True)
        worker.draw_latex = mock.Mock(return_value="")
        run_result = await worker.run()
        self.assertEqual(run_result, "")
        worker.cleanup.assert_called_once()
        worker.run_subprocess.assert_awaited_once()
        worker.draw_latex.assert_called_once()

    async def test_run_matrix_to_quantum_circuit(self):
        """test run matrix to quantum circuit"""
        worker = ConverterWorker(
            QuantumExpression.MATRIX,
            QuantumExpression.CIRCUIT,
            self.matrix_input,
            MATRIX_CODE,
        )
        worker.run_subprocess = mock.AsyncMock(return_value=(" ", " "))
        worker.cleanup = mock.Mock(return_value=True)
        run_result = await worker.run()
        self.assertEqual(run_result, f"{RANDOM_FILE_NAME}" + ".png")
        worker.cleanup.assert_called_once()
        worker.run_subprocess.assert_awaited_once()
