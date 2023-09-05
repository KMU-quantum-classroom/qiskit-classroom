"""
entry point for gui application
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

import sys
import asyncio
import functools
from PySide6.QtWidgets import QMainWindow, QStatusBar
from qiskit_classroom.converter_view import ConverterView
from qiskit_classroom.converter_model import ConverterModel
from qiskit_classroom.converter_presenter import ConverterPresenter
from qiskit_classroom import QISKIT_CLASSROOM_CONVERTER_VERSION_STR

# rearranged it to tell qasync to use PySide6
# pylint: disable=wrong-import-order
import qasync
from qasync import QApplication

__app_name__ = "Qiskit-Classroom"
__author__ = "KMU-quantum-classroom"
__license__ = "Apache License"
__copyright__ = "2023 " + __author__
__version__ = "0.0.1"
__email__ = "jinseok1001@outlook.com"


def move_center(window: QMainWindow):
    """move window to center of screen

    Args:
        window (QMainWindow): main window
    """
    frame = window.frameGeometry()
    center_position = window.screen().availableGeometry().center()

    frame.moveCenter(center_position)
    window.move(frame.topLeft())


async def async_main():
    """
    async main for app
    """

    def close_future(future: asyncio.Future, loop):
        loop.call_later(10, future.cancel)
        future.cancel()
        # remove remain image
        model.remove_result_img_path()

    loop = asyncio.get_event_loop()
    future = asyncio.Future()

    app = QApplication.instance()
    if hasattr(app, "aboutToQuit"):
        getattr(app, "aboutToQuit").connect(
            functools.partial(close_future, future, loop)
        )

    main_window = QMainWindow(None)
    main_window.setWindowTitle("Qiskit_classroom")
    version_bar = QStatusBar(main_window)
    version_bar.showMessage("running on " + QISKIT_CLASSROOM_CONVERTER_VERSION_STR)
    main_window.setStatusBar(version_bar)

    model = ConverterModel()
    view = ConverterView()

    main_window.setCentralWidget(view)

    presenter = ConverterPresenter(view, model)
    view.set_presenter(presenter=presenter)

    main_window.show()
    move_center(main_window)

    await future
    return True


def main():
    """main for app"""
    if sys.version_info.major == 3 and sys.version_info.minor == 11:
        # this code run on 3.11
        # pylint: disable=protected-access
        with qasync._set_event_loop_policy(qasync.DefaultQEventLoopPolicy()):
            runner = asyncio.runners.Runner()
            try:
                runner.run(async_main())
            except asyncio.exceptions.CancelledError:
                sys.exit(0)
            finally:
                runner.close()
    else:
        try:
            qasync.run(async_main())
        except asyncio.exceptions.CancelledError:
            sys.exit(0)


if __name__ == "__main__":
    main()
