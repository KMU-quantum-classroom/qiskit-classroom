"""unittest for converter model"""

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
from qiskit_classroom.converter_model import ConverterModel, ConvertingRuleException
from qiskit_classroom.expression_enum import QuantumExpression


class TestConverterModel(unittest.TestCase):
    """unittest class for ConverterModel"""

    def setUp(self) -> None:
        self.model = ConverterModel()
        return super().setUp()

    def test_from_expression_setter(self) -> None:
        """testing setter raise ConvertingRuleException when model is MATRIX and DIRAC"""
        self.model.to_expression = QuantumExpression.DIRAC
        with self.assertRaises(ConvertingRuleException):
            self.model.from_expression = QuantumExpression.MATRIX

    def test_to_expression_setter(self) -> None:
        """testing setter raise ConvertingRuleException when model is MATRIX and DIRAC"""
        self.model.from_expression = QuantumExpression.MATRIX
        with self.assertRaises(ConvertingRuleException):
            self.model.to_expression = QuantumExpression.DIRAC

    def test_set_img_path(self) -> None:
        """test setter image_path"""
        self.model.result_img_path = "random_file.py.png"

        self.assertEqual(self.model.result_img_path, "random_file.py.png")
