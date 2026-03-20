"""Notion-themed 'Create New Project' dialog."""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFileDialog, QComboBox
)
from PySide6.QtCore import Qt, QSettings

from model.new_project_model import NewProjectModel
from viewmodel.new_project_viewmodel import NewProjectViewModel
from hub_utils import is_frozen


class NewProjectView(QDialog):
    SETTINGS_GROUP = "NewProjectDialog"
    LAST_PATH_KEY = "lastProjectPath"

    def __init__(self, version_manager=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Project")
        self.setMinimumWidth(480)
        self._version_manager = version_manager

        self.settings = QSettings("InfernuxEngine", "InfernuxEngine")

        # MVVM setup
        self.model = NewProjectModel()
        self.viewmodel = NewProjectViewModel(self.model)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        # Project name input
        name_layout = QVBoxLayout()
        name_label = QLabel("Project Name:")
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter a name for your project")
        self.name_edit.textChanged.connect(self.viewmodel.set_name)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        # Path chooser
        path_layout = QVBoxLayout()
        path_label = QLabel("Project Location:")
        chooser_row = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        self.path_edit.setPlaceholderText("No path selected")
        path_button = QPushButton("Browse...")
        path_button.setObjectName("normalBtn")
        path_button.clicked.connect(self._on_choose_path)
        chooser_row.addWidget(self.path_edit)
        chooser_row.addWidget(path_button)
        path_layout.addWidget(path_label)
        path_layout.addLayout(chooser_row)
        layout.addLayout(path_layout)

        # Load last path if available
        last_path = self.settings.value(f"{self.SETTINGS_GROUP}/{self.LAST_PATH_KEY}", "")
        if last_path:
            self.path_edit.setText(last_path)
            self.viewmodel.set_path(last_path)

        # Engine version selector
        ver_layout = QVBoxLayout()
        ver_label = QLabel("Engine Version:")
        self.version_combo = QComboBox()
        self.version_combo.setFixedHeight(32)
        self._populate_versions()
        ver_layout.addWidget(ver_label)
        ver_layout.addWidget(self.version_combo)
        layout.addLayout(ver_layout)

        # Button row
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("normalBtn")
        btn_cancel.clicked.connect(self.reject)

        btn_create = QPushButton("Create")
        btn_create.setObjectName("createBtn")
        btn_create.clicked.connect(self.accept)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_create)
        layout.addLayout(btn_layout)

    def _populate_versions(self):
        """Fill the version combo box."""
        if self._version_manager is not None:
            installed = self._version_manager.installed_versions()
            if installed:
                for v in installed:
                    self.version_combo.addItem(v, v)
            else:
                self.version_combo.addItem("(no versions installed)", "")

        if not is_frozen():
            # Dev mode: add a "dev (current env)" option at the top
            self.version_combo.insertItem(0, "dev (current environment)", "")
            self.version_combo.setCurrentIndex(0)

    def _on_choose_path(self):
        current_path = self.path_edit.text() or ""
        folder = QFileDialog.getExistingDirectory(self, "Choose Project Location", current_path)
        if folder:
            self.path_edit.setText(folder)
            self.viewmodel.set_path(folder)
            self.settings.setValue(f"{self.SETTINGS_GROUP}/{self.LAST_PATH_KEY}", folder)

    def get_data(self):
        name, path = self.viewmodel.get_data()
        version = self.version_combo.currentData() or ""
        return name, path, version
