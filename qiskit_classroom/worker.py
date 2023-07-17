"""
    worker for convert and visualize expressions
"""

# todo migration to QProcess
import asyncio
import random
from shutil import copyfile
import string
from .expression_enum import QuantumExpression


class ConverterWorker:
    """ """

    from_expression: QuantumExpression
    to_expression: QuantumExpression
    sourcecode_path: str
    __injected_sourcecode_path: str

    def __init__(
        self,
        from_expression: QuantumExpression,
        to_expression: QuantumExpression,
        sourcode_path: str,
    ) -> None:
        self.from_expression = from_expression
        self.to_expression = to_expression
        self.sourcecode_path = sourcode_path
        self.__injected_sourcecode_path = "".join(
            random.choice(string.ascii_letters) for _ in range(10)
        )

    def __code_inject(self):
        copyfile(self.sourcecode_path, self.__injected_sourcecode_path)
        with open(
            self.__injected_sourcecode_path, mode="a", encoding="UTF-8"
        ) as injected_file:
            # write converting codes
            injected_file.write(
                "from qiskit_class_converter import ConversionService, ConversionType"
            )

    async def run(self) -> str:
        self.__code_inject()
        proc = await asyncio.create_subprocess_exec(
            f"python3 {self.sourcecode_path}.py",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        await proc.wait()

        if stdout:
            print(f"output {stdout.decode()}")
        if stderr:
            print(f"err {stderr.decode()}")

        return self.__injected_sourcecode_path + ".jpg"
