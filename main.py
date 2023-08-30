"""
entry point for gui application
"""
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


def move_center(window: QMainWindow):
    """move window to center of screen

    Args:
        window (QMainWindow): main window
    """
    frame = window.frameGeometry()
    center_position = window.screen().availableGeometry().center()

    frame.moveCenter(center_position)
    window.move(frame.topLeft())


async def main():
    """
    main for app
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


if __name__ == "__main__":
    if sys.version_info.major == 3 and sys.version_info.minor == 11:
        # this code run on 3.11
        # pylint: disable=protected-access
        with qasync._set_event_loop_policy(qasync.DefaultQEventLoopPolicy()):
            runner = asyncio.runners.Runner()
            try:
                runner.run(main())
            except asyncio.exceptions.CancelledError:
                sys.exit(0)
            finally:
                runner.close()
    else:
        try:
            qasync.run(main())
        except asyncio.exceptions.CancelledError:
            sys.exit(0)
