"""
    worker for convert and visualize expressions
"""

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

mpl.rcParams["font.size"] = 12
mpl.rcParams["text.usetex"] = True
mpl.rcParams["text.latex.preamble"] = r"\usepackage{{amsmath}}\usepackage{{qcircuit}}"


def add_new_line(strings: list[str]) -> str:
    """add \\n between every line

    Args:
        strings (list[str]): list of line

    Returns:
        str: joined string with \\n
    """
    return "\n".join(strings)


class ConverterWorker:
    """worker for convert expression and visualize expression"""

    def __init__(
        self,
        from_expression: QuantumExpression,
        to_expression: QuantumExpression,
        input_data: Input,
        expression_text: str,
    ) -> None:
        self.from_expression = from_expression
        self.to_expression = to_expression
        self.__injected_sourcecode_path = ConverterWorker.generate_random_file_name()

        # copy text
        self.expression_text = "" + expression_text
        self.input_data = input_data

    @staticmethod
    def generate_random_file_name() -> str:
        """return generated file name

        Returns:
            str: generated file name
        """
        return "".join(random.choice(string.ascii_letters) for _ in range(10)) + ".py"

    @staticmethod
    def write_converting_code(file_path: str, code: str) -> bool:
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

    def __code_inject(self):
        expression_text = self.expression_text
        if self.from_expression is QuantumExpression.MATRIX:
            input_data: MatrixInput = self.input_data
            expression_text = f"{input_data.value_name}={expression_text}"
        ConverterWorker.write_converting_code(
            self.__injected_sourcecode_path,
            add_new_line(
                [
                    expression_text,
                    "from qiskit_class_converter import ConversionService",
                    "from qiskit.visualization import array_to_latex",
                    self.__convert_code(),
                    self.__drawing_code(),
                ]
            ),
        )

    def __convert_code(self) -> str:
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
                    f"quantum_circuit = QuantumCircuit({matrix_input.num_cubit})",
                    f"quantum_circuit.append(result, {list(range(matrix_input.num_cubit))})",
                    "quantum_circuit.measure_all()" if matrix_input.do_measure else "",
                ]
            )

        return add_new_line([first_line, next_line])

    def __drawing_code(self) -> str:
        if self.to_expression is QuantumExpression.MATRIX:
            return add_new_line(
                [
                    "source = array_to_latex(result['result'], source=True)",
                    "print(source)",
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
        return ""

    async def run(self) -> str:
        """inject expression convert code to user's source code and create
        subprocess for drawing converted expresion

        Returns:
            str: path of subprocess created image
        """
        print("now running")
        print(datetime.datetime.now().time())
        self.__code_inject()
        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            self.__injected_sourcecode_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        await proc.wait()
        output: str = ""

        if stdout:
            output = stdout.decode()
            print(f"output {output}")
        if stderr:
            print(f"error {stderr.decode()}")
        print("end at ")
        print(datetime.datetime.now().time())

        # remove injected source code
        os.remove(self.__injected_sourcecode_path)

        if self.to_expression is QuantumExpression.CIRCUIT:
            return self.__injected_sourcecode_path + ".png"

        return self.draw_latex(latex=output)

    def draw_latex(self, latex: str) -> str:
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
        fig.savefig(output, dpi=300, bbox_inches="tight")
        plt.close()
        return output
