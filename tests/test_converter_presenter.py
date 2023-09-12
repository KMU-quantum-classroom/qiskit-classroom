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
from unittest import mock
from qiskit_classroom.converter_model import ConverterModel
from qiskit_classroom.converter_presenter import ConverterPresenter
from qiskit_classroom.converter_view import ConverterView
from qiskit_classroom.expression_enum import QuantumExpression


PATH = ["not_python_script.txt", "ramdom_file.py"]


class ConverterPresenterTest(unittest.IsolatedAsyncioTestCase):
    """unittest class ConverterPresenter"""

    def setUp(self) -> None:
        self.view = mock.create_autospec(ConverterView)
        self.view.set_ui = mock.Mock(return_value=None)
        self.view.connect_signal = mock.Mock(return_value=None)
        self.view.set_expression_plain_text_text = mock.Mock(return_value=None)
        self.model = ConverterModel()
        self.presenter = ConverterPresenter(self.view, self.model)

    def test_on_file_dropped(self) -> None:
        """test on file dropped"""
        mock_file = mock.mock_open(read_data="hello world")
        with mock.patch("builtins.open", mock_file):
            self.presenter.on_file_dropped(PATH[:0])
            self.assertEqual(self.model.expression_text, "")

        mock_file = mock.mock_open(read_data="print('hello')")
        with mock.patch("builtins.open", mock_file):
            self.presenter.on_file_dropped(PATH)
            self.assertEqual(self.model.expression_text, "print('hello')")

    def test_on_file_imported(self) -> None:
        """test on file imported"""
        mock_file = mock.mock_open(read_data="print('hello')")
        with mock.patch("builtins.open", mock_file):
            self.presenter.on_file_imported(PATH[1])
            self.assertEqual(self.model.expression_text, "print('hello')")

    def test_on_from_combo_changed(self) -> None:
        """test from_combo item changed"""
        self.view.get_from_expression = mock.Mock(
            return_value=QuantumExpression.CIRCUIT.name
        )
        self.presenter.on_from_combo_changed()
        self.assertEqual(self.model.from_expression, QuantumExpression.CIRCUIT)
        self.assertEqual(self.model.to_expression, QuantumExpression.CIRCUIT)

        self.view.get_from_expression = mock.Mock(
            return_value=QuantumExpression.DIRAC.name
        )

        self.presenter.on_from_combo_changed()
        self.assertEqual(self.model.from_expression, QuantumExpression.NONE)

        self.model.to_expression = QuantumExpression.DIRAC
        self.view.get_from_expression = mock.Mock(
            return_value=QuantumExpression.MATRIX.name
        )

        self.presenter.on_from_combo_changed()

        self.assertEqual(self.model.to_expression, QuantumExpression.MATRIX)

    def test_on_to_combo_changed(self) -> None:
        """test on combo changed"""
        self.view.get_to_expression = mock.Mock(return_value="CIRCUIT")

        self.presenter.on_to_combo_changed()

        self.assertEqual(self.model.to_expression, QuantumExpression.CIRCUIT)
