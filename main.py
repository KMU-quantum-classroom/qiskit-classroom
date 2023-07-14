import sys

from PyQt6.QtWidgets import QApplication
from qiskit_classroom.converter_view import ConverterView
from qiskit_classroom.converter_model import ConverterModel
from qiskit_classroom.converter_presenter import ConverterPresenter

if __name__ == '__main__':

    app = QApplication(sys.argv)
    model = ConverterModel()
    w = ConverterView()

    presenter = ConverterPresenter(w, model)
    w.set_presenter(presenter=presenter)

    w.show()
    sys.exit(app.exec())
