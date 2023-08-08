"""
    image dialog
"""

from PySide6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap


class ResultImageDialog(QDialog):
    """
    show image which converted
    """

    def __init__(self, parent) -> None:
        super(ResultImageDialog, self).__init__(parent)
        self.setWindowTitle("Result Image")
        self.setContentsMargins(50, 50, 50, 50)

        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(10, 10, 10, 10)
        self.image_label = QLabel()
        vbox.addWidget(self.image_label)

        self.close_button = QPushButton("close")
        self.close_button.clicked.connect(self.close)
        vbox.addWidget(self.close_button)

    def show_image(self, image_path: str) -> None:
        """show image

        Args:
            image_path (str): image path
        """
        img = QPixmap(image_path)
        self.image_label.setPixmap(img)
        self.image_label.show()
        self.show()

    def hideEvent(self, event) -> None:
        self.image_label.clear()
        return super().hideEvent(event)