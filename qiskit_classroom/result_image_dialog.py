"""
    image dialog
"""

# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class ResultImageDialog(QDialog):
    """
    show image which converted
    """

    def __init__(self, parent) -> None:
        super(ResultImageDialog, self).__init__(parent)
        self.setWindowTitle("Result Image")
        self.setMinimumWidth(300)
        self.setMinimumHeight(200)

        vbox = QVBoxLayout(self)
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        # resize dialog by image size
        self.resize(img.width() + 100, img.height() + 150)
        self.show()

    def hideEvent(self, event) -> None:  # pylint: disable=invalid-name
        self.image_label.clear()
        return super().hideEvent(event)
