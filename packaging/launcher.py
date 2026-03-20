import sys
sys.dont_write_bytecode = True

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QSizePolicy, QStackedWidget,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFontDatabase

from ui_project_list import ProjectListPane
from database import ProjectDatabase
from style import StyleManager
from hub_resources import ICON_PATH, FONT_PATH
from version_manager import VersionManager

from model.project_model import ProjectModel
from viewmodel.control_pane_viewmodel import ControlPaneViewModel
from view.control_pane_view import ControlPane
from view.sidebar_view import SidebarView
from view.installs_view import InstallsView


class GameEngineLauncher(QMainWindow):
    def __init__(self) -> None:
        self._own_app = False
        if QApplication.instance() is None:
            self._own_app = True
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()

        super().__init__()

        # Load custom engine font
        font_id = QFontDatabase.addApplicationFont(FONT_PATH)
        if font_id >= 0:
            QFontDatabase.applicationFontFamilies(font_id)

        # Apply global dark theme
        self.app.is_dark_theme = True
        self.app.setStyleSheet(StyleManager.get_stylesheet(self.app.is_dark_theme))

        self.setWindowTitle("InfEngine Hub")
        self.setWindowIcon(QIcon(ICON_PATH))
        self.resize(1080, 720)

        # Database & version manager
        self.db = ProjectDatabase()
        self.version_manager = VersionManager()

        # ── Root layout: sidebar | content ───────────────────────────
        central = QWidget(self)
        central.setObjectName("central")
        self.setCentralWidget(central)
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Sidebar
        self.sidebar = SidebarView(parent=central)
        root_layout.addWidget(self.sidebar)

        # Stacked pages
        self.pages = QStackedWidget()
        root_layout.addWidget(self.pages, 1)

        # ── Page 0: Projects ─────────────────────────────────────────
        projects_page = QWidget()
        projects_layout = QVBoxLayout(projects_page)
        projects_layout.setContentsMargins(28, 24, 28, 24)
        projects_layout.setSpacing(16)

        self.project_list = ProjectListPane(self.db, parent=projects_page)
        model = ProjectModel(self.db, self.version_manager)
        viewmodel = ControlPaneViewModel(model, self.project_list, self.version_manager)
        self.controls = ControlPane(viewmodel, parent=projects_page)

        self.controls.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.project_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        projects_layout.addWidget(self.controls, 0)
        projects_layout.addWidget(self.project_list, 1)

        self.pages.addWidget(projects_page)

        # ── Page 1: Installs ─────────────────────────────────────────
        installs_page = QWidget()
        installs_layout = QVBoxLayout(installs_page)
        installs_layout.setContentsMargins(28, 24, 28, 24)
        installs_layout.setSpacing(0)

        self.installs_view = InstallsView(self.version_manager, parent=installs_page)
        installs_layout.addWidget(self.installs_view)

        self.pages.addWidget(installs_page)

        # ── Sidebar → page switching ─────────────────────────────────
        self.sidebar.page_changed.connect(self._on_page_changed)

        # Cleanup on close
        self.app.aboutToQuit.connect(self._on_close)

    def _on_page_changed(self, index: int):
        self.pages.setCurrentIndex(index)
        # Refresh installs when switching to that page
        if index == 1:
            self.installs_view.refresh()

    def run(self):
        self.show()
        if self._own_app:
            sys.exit(self.app.exec())

    def _on_close(self):
        self.db.close()


if __name__ == "__main__":
    launcher = GameEngineLauncher()
    launcher.run()
