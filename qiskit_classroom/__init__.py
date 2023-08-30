"""init python script for this pacakge"""
from qiskit_class_converter import (
    __FULL_VERSION__ as qiskit_classroom_converter_version,
)

QISKIT_CLASSROOM_CONVERTER_VERSION_STR = " ".join(
    [f"{key}: {value}" for key, value in qiskit_classroom_converter_version.items()]
)
