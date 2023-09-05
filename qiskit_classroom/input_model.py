"""moudle for input data classes"""

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
