"""Header bar for the Projects page."""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
)
from PySide6.QtCore import Qt


class ControlPane(QWidget):
    """Projects page header with title + action buttons."""

    def __init__(self, viewmodel, style=None, parent=None):
        super().__init__(parent)
        self.viewmodel = viewmodel

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ── Header row ──
        header = QHBoxLayout()
        header.setContentsMargins(4, 0, 0, 12)

        title = QLabel("Projects")
        title.setObjectName("pageTitle")
        header.addWidget(title, alignment=Qt.AlignmentFlag.AlignLeft)
        header.addStretch()

        # ── Action buttons (right-aligned) ──
        self.btn_delete = QPushButton("Delete")
        self.btn_delete.setObjectName("dangerBtn")
        self.btn_delete.setFixedHeight(36)
        self.btn_delete.setMinimumWidth(90)
        self.btn_delete.clicked.connect(lambda: self.viewmodel.delete_project(self))
        header.addWidget(self.btn_delete)

        spacer_label = QLabel("")
        spacer_label.setFixedWidth(8)
        header.addWidget(spacer_label)

        self.btn_new = QPushButton("+ New Project")
        self.btn_new.setObjectName("primaryBtn")
        self.btn_new.setFixedHeight(36)
        self.btn_new.setMinimumWidth(130)
        self.btn_new.clicked.connect(lambda: self.viewmodel.create_project(self))
        header.addWidget(self.btn_new)

        spacer_label2 = QLabel("")
        spacer_label2.setFixedWidth(8)
        header.addWidget(spacer_label2)

        self.btn_launch = QPushButton("▶  Launch")
        self.btn_launch.setObjectName("normalBtn")
        self.btn_launch.setFixedHeight(36)
        self.btn_launch.setMinimumWidth(110)
        self.btn_launch.clicked.connect(lambda: self.viewmodel.launch_project(self))
        header.addWidget(self.btn_launch)

        main_layout.addLayout(header)
