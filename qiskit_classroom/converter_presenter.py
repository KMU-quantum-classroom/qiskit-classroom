"""
    presenter for converter view
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
from subprocess import TimeoutExpired
from typing import TYPE_CHECKING
from .expression_enum import QuantumExpression, Converting_method
from .input_model import Input
from .converter_model import ConvertingRuleException

if TYPE_CHECKING:
    from .converter_model import ConverterModel
    from .converter_view import ConverterView


def open_file(file_path: str) -> str:
    """open file and return contents

    Args:
        file_path (str): file path

    Returns:
        str: contents of file
    """
    try:
        with open(file_path, "r", encoding="UTF-8") as file:
            return file.read()
    except FileNotFoundError:
        return ""


class ConverterPresenter:
    """
    presenter for converter
    """

    def __init__(self, view: "ConverterView", model: "ConverterModel") -> None:
        self.view = view
        self.view.set_presenter(self)
        self.model = model

    def on_file_dropped(self, file_paths: list[str]) -> None:
        """handling file drag and drop event

        Args:
            file_paths (list[str]): file paths which Signal pass
        """
        for file_path in file_paths:
            if file_path.endswith(".py"):
                self.model.expression_text = open_file(file_path)
                self.view.set_expression_plain_text_text(self.model.expression_text)
                break

    def on_file_imported(self, file_path: str) -> None:
        """handling file imported event

        Args:
            file_path (str): file path whitch Signal pass
        """
        self.model.expression_text = open_file(file_path)
        self.view.set_expression_plain_text_text(self.model.expression_text)

    def on_from_combo_changed(self) -> None:
        """
        update from_expression
        """
        self.view.disable_from_combo_current_text_change()
        from_expression = QuantumExpression[self.view.get_from_expression()]
        if from_expression is QuantumExpression.DIRAC:
            self.view.show_alert_message("not supported")
            self.view.set_from_combo_current_index(3)
            from_expression = QuantumExpression.NONE

        try:
            self.model.from_expression = from_expression
        except ConvertingRuleException:
            self.model.to_expression = QuantumExpression.NONE
            self.model.from_expression = from_expression

        # this line prevent triggering to_combo.currentIndexChanged event multiple time
        # lock
        self.view.disable_to_combo_current_text_change()
        self.view.set_to_combo_items(
            [
                expression.name
                for expression in Converting_method[self.model.from_expression]
            ]
        )
        self.model.to_expression = Converting_method[self.model.from_expression][0]
        # unlock
        self.view.enable_to_combo_current_text_change()

        self.view.show_input_widget(self.model.from_expression)
        self.view.clear_expression_plain_text()
        self.view.set_placeholder(self.model.from_expression)

        self.view.enable_from_combo_current_text_change()

    def on_to_combo_changed(self) -> None:
        """
        update to_expression
        """
        self.model.to_expression = QuantumExpression[self.view.get_to_expression()]

    async def on_convert_button_clicked(self) -> None:
        """
        convert expression and visualiazation.
        update result file path
        """
        self.view.show_progress_bar()
        result = False
        self.model.expression_text = self.view.get_expression_plain_text_text().strip()
        input_data: Input = self.view.get_input(self.model.from_expression)

        self.model.input_data = input_data

        try:
            result = await self.model.convert_and_draw()
        except RuntimeError:
            self.view.show_alert_message("conversion processe error")
        except TimeoutExpired:
            self.view.show_alert_message("conversion process timeout error")
        except FileNotFoundError:
            self.view.show_alert_message("set file valid one")
        except AttributeError:
            self.view.show_alert_message("set input value")
        except SyntaxError:
            self.view.show_alert_message("syntax error with your code or expression")
        except NameError:
            self.view.show_alert_message("value_name or some value name not defined")
        finally:
            self.view.close_progress_bar()

        if result:
            # wait until file save
            await asyncio.sleep(0.5)
            self.view.show_result_image(self.model.result_img_path)

    def on_view_destoryed(self) -> None:
        """remove image file on view destryed"""
        self.model.remove_result_img_path()
