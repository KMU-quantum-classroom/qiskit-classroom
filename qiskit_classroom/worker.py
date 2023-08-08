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
import matplotlib as mpl
import matplotlib.pyplot as plt
from .expression_enum import QuantumExpression

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
                add_new_line(
                    [
                        "from qiskit_class_converter import ConversionService",
                        "from qiskit.visualization import array_to_latex",
                        self.__convert_code(),
                        self.__drawing_code(),
                    ]
                )
            )
            injected_file.close()

    def __convert_code(self) -> str:
        if self.to_expression == self.from_expression:
            return ""
        option = (
            '{"print" : "raw"}'
            if self.to_expression is QuantumExpression.DIRAC
            else "None"
        )
        first_line = (
            "converter = ConversionService(conversion_type="
            + f"'{self.from_expression.value[1]}_TO_{self.to_expression.value[1]}', "
            + f"option={option})"
        )
        next_line = f"result = converter.convert(input_value={self.value_name})"
        if self.from_expression is QuantumExpression.MATRIX:
            pass

        return add_new_line([first_line, next_line])

    def __drawing_code(self) -> str:
        if self.to_expression is QuantumExpression.MATRIX:
            return add_new_line(
                [
                    "source = array_to_latex(result['result'], source=True)",
                    "print(source)",
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
        stdout, _ = await proc.communicate()

        await proc.wait()
        output: str = ""

        if stdout:
            output = stdout.decode()
            print(f"output {output}")
        print("end at ")
        print(datetime.datetime.now().time())

        # remove injected source code
        os.remove(self.__injected_sourcecode_path)

        if self.to_expression is not QuantumExpression.CIRCUIT:
            # filtering latex syntax
            return self.draw_latex(latex=output)

        return self.__injected_sourcecode_path + ".png"

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
