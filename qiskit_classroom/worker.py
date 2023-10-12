"""
    worker for convert and visualize expressions
"""

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

import asyncio
import datetime
import random
import os
import string
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
from .expression_enum import QuantumExpression
from .input_model import Input, QuantumCircuitInput, MatrixInput

mpl.rcParams["font.size"] = 9
mpl.rcParams["text.usetex"] = True
mpl.rcParams["text.latex.preamble"] = r"\usepackage{{amsmath}}"

ARRAY_TO_LATEX_IMPORT = "from qiskit.visualization import array_to_latex"
CONVERTER_IMPORT = "from qiskit_class_converter import ConversionService"


def add_new_line(strings: list[str]) -> str:
    """add \\n between every line

    Args:
        strings (list[str]): list of line

    Returns:
        str: joined string with \\n
    """
    return "\n".join(strings)


# pylint: disable=too-many-instance-attributes
class ConverterWorker:
    """worker for convert expression and visualize expression"""

    def __init__(
        self,
        from_expression: QuantumExpression,
        to_expression: QuantumExpression,
        input_data: Input,
        expression_text: str,
        shows_result: bool,
    ) -> None:
        self.from_expression = from_expression
        self.to_expression = to_expression
        self.__injected_sourcecode_path = ConverterWorker.generate_random_file_name()

        # copy text
        self.expression_text = "" + expression_text
        self.input_data = input_data
        self.shows_result = shows_result

    @staticmethod
    def generate_random_file_name() -> str:  # pragma: no cover
        # this method implmented with random function
        """return generated file name

        Returns:
            str: generated file name
        """
        return (
            "/tmp/"
            + "".join(random.choice(string.ascii_letters) for _ in range(10))
            + ".py"
        )

    @staticmethod
    def write_converting_code(file_path: str, code: str) -> bool:  # pragma: no cover
        """write code to file_path

        Args:
            file_path (str): target
            code (str): contents

        Returns:
            bool: is succesful
        """
        try:
            with open(file_path, mode="w", encoding="UTF-8") as file:
                file.write(code)
        except FileNotFoundError:
            return False
        return True

    def __generate_code(self):  # pragma: no cover
        expression_text = self.expression_text
        if self.from_expression is QuantumExpression.MATRIX:
            input_data: MatrixInput = self.input_data
            expression_text = f"{input_data.value_name}={expression_text}"
        ConverterWorker.write_converting_code(
            self.__injected_sourcecode_path,
            add_new_line(
                [
                    expression_text,
                    CONVERTER_IMPORT,
                    ARRAY_TO_LATEX_IMPORT,
                    self.generate_conversion_code(),
                    self.generate_visualization_code(),
                ]
            ),
        )

    def generate_conversion_code(self) -> str:
        """generate the conversion code according to the conversion method.

        Returns:
            str: generated conversion code
        """
        if self.to_expression == self.from_expression:
            return ""
        matrix_to_qc_option: dict[str, str] = {"label": "unitary gate"}
        default_option: dict[str, str] = {"print": "raw"}

        option: dict[str, str] = {}
        if self.to_expression is QuantumExpression.CIRCUIT:
            option = matrix_to_qc_option
        else:
            option = default_option
        first_line = (
            "converter = ConversionService(conversion_type="
            + f"'{self.from_expression.value[1]}_TO_{self.to_expression.value[1]}', "
            + f"option={option})"
        )
        next_line: str = ""
        if self.from_expression is QuantumExpression.CIRCUIT:
            quantum_circuit_input: QuantumCircuitInput = self.input_data
            next_line = (
                "result = converter.convert"
                + f"(input_value={quantum_circuit_input.value_name})"
            )
        if self.from_expression is QuantumExpression.MATRIX:
            matrix_input: MatrixInput = self.input_data
            next_line = add_new_line(
                [
                    "from qiskit import QuantumCircuit",
                    ""
                    f"result = converter.convert(input_value={matrix_input.value_name})",
                    f"quantum_circuit = QuantumCircuit({matrix_input.num_qubits})",
                    "quantum_circuit.append(result, list(range(result.num_qubits)))",
                    "quantum_circuit.measure_all()" if matrix_input.do_measure else "",
                ]
            )

        return add_new_line([first_line, next_line])

    def generate_visualization_code(self) -> str:
        """generate visualiszation code according to the conversion method

        Returns:
            str: visualization code
        """
        if self.to_expression is not self.from_expression:
            if self.to_expression is QuantumExpression.MATRIX:
                return add_new_line(
                    [
                        "for gate, name in zip(reversed(result['gate']), reversed(result['name'])):",
                        "\totimes=' \\\\otimes '",
                        """\tprint('\\stackrel{' + otimes.join(name[1]) +'}' + f'{{{gate}}}')""",
                        "print(f\"= \\stackrel{{result}}{{{result['result']}}}\")"
                        if self.shows_result
                        else "",
                    ]
                )

            if self.to_expression is QuantumExpression.CIRCUIT:
                return add_new_line(
                    [
                        'quantum_circuit.draw(output="mpl")'
                        + f'.savefig("{self.__injected_sourcecode_path+".png"}", '
                        + 'bbox_inches="tight")'
                    ]
                )

            if self.to_expression is QuantumExpression.DIRAC:
                return add_new_line(["print(result)"])
        else:
            if self.to_expression is QuantumExpression.MATRIX:
                matrix_input: MatrixInput = self.input_data
                return add_new_line(
                    [f"print(array_to_latex({matrix_input.value_name}, source=True))"]
                )
            if self.to_expression is QuantumExpression.CIRCUIT:
                qunatum_input: QuantumCircuitInput = self.input_data
                return add_new_line(
                    [
                        f'{qunatum_input.value_name}.draw(output="mpl")'
                        + f'.savefig("{self.__injected_sourcecode_path+".png"}",'
                        + 'bbox_inches="tight")'
                    ]
                )
        return ""

    async def run(self) -> str:
        """inject expression convert code to user's source code and create
        subprocess for drawing converted expresion

        Returns:
            str: path of subprocess created image
        """
        print("now running")
        print(datetime.datetime.now().time())
        self.__generate_code()
        stdout, stderr = await self.run_subprocess()

        if stdout:
            print(f"output {stdout}")
        if stderr:
            stderr: str = stderr
            print(f"error {stderr}")
            if stderr.find("SyntaxError") != -1:
                raise SyntaxError
            if stderr.find("NameError") != -1:
                raise NameError
        print("end at ")
        print(datetime.datetime.now().time())

        # remove injected source code
        if not self.cleanup():
            print("error removing file")

        if self.to_expression is QuantumExpression.CIRCUIT:
            return self.__injected_sourcecode_path + ".png"

        return self.draw_latex(latex=stdout)

    async def run_subprocess(self) -> (str, str):
        """run generated script's subprocess

        Returns:
            (str, str): subprocess's stdout and stderr
        """
        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            self.__injected_sourcecode_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        await proc.wait()
        return (stdout.decode(), stderr.decode())

    def cleanup(self) -> bool:
        """remove generated script

        Returns:
            bool: result of removing file
        """
        try:
            os.remove(self.__injected_sourcecode_path)
        except FileNotFoundError:
            return False
        return True

    def draw_latex(self, latex: str) -> str:  # pragma: no cover
        """
        render latex to image and save as file.

        Args:
            latex (str): latex matrix code

        Raises:
            MatrixNotFound: when latex not have matrix

        Returns:
            str: image file path
        """

        # this code avoid latex runtime error (\n ocurse error)
        latex = latex.replace("\n", " ").strip()

        fig = plt.figure()
        fig.text(0, 0, f"${latex}$")
        output = self.__injected_sourcecode_path + ".png"
        fig.savefig(output, dpi=200, bbox_inches="tight")
        plt.close()
        return output
