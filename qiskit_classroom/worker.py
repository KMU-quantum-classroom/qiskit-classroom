"""
    worker for convert and visualize expressions
"""

import asyncio
import datetime
import random
import os
from shutil import copyfile
import string
import sys
import re
import matplotlib as mpl
import matplotlib.pyplot as plt
from .expression_enum import QuantumExpression

mpl.rcParams["font.size"] = 12
mpl.rcParams["text.usetex"] = True
mpl.rcParams["text.latex.preamble"] = r"\usepackage{{amsmath}}"

LATEX_MATRIX_PATTERN = (
    r"\\begin{bmatrix}\s*((?:\d+\s*&\s*)+\d+\s*\\\\\s*)+\\end{bmatrix}"
)


class MatrixNotFound(Exception):
    """raise when there is no Matrix in output

    Args:
        Exception (str): output message
    """

    def __init__(self, output) -> None:
        super().__init__(output)


class ConverterWorker:
    """worker for convert expression and visualize expression"""

    from_expression: QuantumExpression
    to_expression: QuantumExpression
    sourcecode_path: str
    __injected_sourcecode_path: str
    value_name: str

    def __init__(
        self,
        from_expression: QuantumExpression,
        to_expression: QuantumExpression,
        sourcode_path: str,
        value_name: str,
    ) -> None:
        self.from_expression = from_expression
        self.to_expression = to_expression
        self.sourcecode_path = sourcode_path
        self.__injected_sourcecode_path = (
            self.sourcecode_path
            + "".join(random.choice(string.ascii_letters) for _ in range(10))
            + ".py"
        )
        self.value_name = value_name

    def __code_inject(self):
        copyfile(self.sourcecode_path, self.__injected_sourcecode_path)
        with open(
            self.__injected_sourcecode_path, mode="a", encoding="UTF-8"
        ) as injected_file:
            # write converting codes
            injected_file.write(
                "from qiskit_class_converter import ConversionService\n"
                + "from qiskit.visualization import array_to_latex"
            )
            injected_file.write(self.__convert_code())
            injected_file.write(self.__drawing_code())
            injected_file.close()

    def __convert_code(self) -> str:
        if self.to_expression == self.from_expression:
            return ""
        first_line = (
            "\nconverter = ConversionService(conversion_type="
            + f"'{self.from_expression.value[1]}_TO_{self.to_expression.value[1]}')"
        )
        next_line = f"\nresult = converter.convert(input_value={self.value_name})"
        if self.from_expression is QuantumExpression.MATRIX:
            pass

        return first_line + next_line

    def __drawing_code(self) -> str:
        if self.to_expression is QuantumExpression.MATRIX:
            return "\nsource = array_to_latex(result['result'], source=True)\nprint(source)"

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
            print(f"err {stderr.decode()}")
        print("end at ")
        print(datetime.datetime.now().time())

        # remove injected source code
        os.remove(self.__injected_sourcecode_path)

        if self.to_expression is QuantumExpression.MATRIX:
            # filtering latex syntax
            return self.matrix_draw(latex=output)

        return self.__injected_sourcecode_path + ".jpg"

    def matrix_draw(self, latex: str) -> str:
        """
        render latex to image and save as file.

        Args:
            latex (str): latex matrix code

        Raises:
            MatrixNotFound: when latex not have matrix

        Returns:
            str: image file path
        """
        pattern = re.compile(LATEX_MATRIX_PATTERN)
        result = pattern.search(latex)
        if result is None:
            raise MatrixNotFound(latex)

        # this code avoid latex runtime error (\n ocurse error)
        latex = result.group().replace("\n", " ")

        fig = plt.figure()
        fig.text(0, 0, f"${latex}$")
        output = self.__injected_sourcecode_path + ".png"
        fig.savefig(output, dpi=300, bbox_inches="tight")
        plt.close()
        return output
