"""
    module for Expression enum
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

import enum


class QuantumExpression(enum.Enum):
    """
    Quantum expression enumerate
    """

    CIRCUIT = (1, "QC")
    DIRAC = (2, "BRA_KET")
    MATRIX = (3, "MATRIX")
    NONE = -1


expressions: list[str] = [expression.name for expression in QuantumExpression]
Converting_method: dict[QuantumExpression, list[QuantumExpression]] = {
    QuantumExpression.NONE: [QuantumExpression.NONE],
    QuantumExpression.CIRCUIT: [
        QuantumExpression.DIRAC,
        QuantumExpression.MATRIX,
    ],
    QuantumExpression.MATRIX: [QuantumExpression.CIRCUIT],
    QuantumExpression.DIRAC: [QuantumExpression.MATRIX],
}
