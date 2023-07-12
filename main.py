import sys

from PyQt6.QtWidgets import QApplication
from qiskit_classroom.converter_view import ConverterView


if __name__ == '__main__':

    app = QApplication(sys.argv)
    # model = ConverterModel()
    w = ConverterView()

    # presenter = ConverterPresenter(w, model)
    # w.setPresenter(presenter=presenter)

    w.show()
    sys.exit(app.exec())
