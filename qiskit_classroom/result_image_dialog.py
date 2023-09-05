"""
    image dialog
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

# pylint: disable=no-name-in-module
from PySide6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class ResultImageDialog(QDialog):
    """
    show image which converted
    """

    def __init__(self, parent) -> None:
        super().__init__(parent)
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
        self.image_label.show()
        self.show()

    def hideEvent(self, event) -> None:  # pylint: disable=invalid-name
        """remove image

        Args:
            event (_type_): default event argument
        """
        self.image_label.clear()
        return super().hideEvent(event)
