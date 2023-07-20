"""
entry point for gui application
"""
import sys
import asyncio
import functools
from qiskit_classroom.converter_view import ConverterView
from qiskit_classroom.converter_model import ConverterModel
from qiskit_classroom.converter_presenter import ConverterPresenter

# rearranged it to tell qasync to use PySide6
# pylint: disable=wrong-import-order
import qasync
from qasync import QApplication


async def main():
    """
    main for app
    """

    def close_future(future: asyncio.Future, loop):
        loop.call_later(10, future.cancel)
        future.cancel()

    loop = asyncio.get_event_loop()
    future = asyncio.Future()

    app = QApplication.instance()
    if hasattr(app, "aboutToQuit"):
        getattr(app, "aboutToQuit").connect(
            functools.partial(close_future, future, loop)
        )

    model = ConverterModel()
    view = ConverterView()

    presenter = ConverterPresenter(view, model)
    view.set_presenter(presenter=presenter)

    view.show()

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
