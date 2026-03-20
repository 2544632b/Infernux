"""Centralized Notion-style theme system for the InfEngine launcher."""

class StyleManager:
    """Provides dynamic QSS stylesheets for light/dark modes."""

    @staticmethod
    def get_stylesheet(is_dark: bool) -> str:
        if is_dark:
            bg_base = "#191919"
            bg_surface = "#202020"
            bg_surface_hover = "#2a2a2a"
            bg_surface_selected = "#333333"
            bg_input = "#202020"
            text_primary = "#cfcfcf"
            text_secondary = "#707070"
            text_muted = "#555555"
            border = "#2f2f2f"
            accent = "#ffffff"
            accent_hover = "#e0e0e0"
            accent_text = "#191919"
            danger = "#eb5757"
            sidebar_bg = "#141414"
            sidebar_border = "#222222"
            nav_hover = "#1e1e1e"
            nav_active = "#252525"
            nav_indicator = "#ffffff"
        else:
            bg_base = "#ffffff"
            bg_surface = "#f7f7f5"
            bg_surface_hover = "#efefed"
            bg_surface_selected = "#e8e8e6"
            bg_input = "#f7f7f5"
            text_primary = "#37352f"
            text_secondary = "#787774"
            text_muted = "#9a9a97"
            border = "#e9e9e7"
            accent = "#37352f"
            accent_hover = "#2f2d28"
            accent_text = "#ffffff"
            danger = "#eb5757"
            sidebar_bg = "#f0f0ee"
            sidebar_border = "#e0e0de"
            nav_hover = "#e8e8e6"
            nav_active = "#e0e0de"
            nav_indicator = "#37352f"

        return f"""
            * {{
                font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
                color: {text_primary};
            }}
            QMainWindow, QWidget#central, QDialog {{
                background-color: {bg_base};
            }}
            QToolTip {{
                background-color: {bg_surface};
                color: {text_primary};
                border: 1px solid {border};
                padding: 4px 8px;
                border-radius: 4px;
            }}

            /* ── Sidebar ── */
            QWidget#sidebar {{
                background-color: {sidebar_bg};
                border-right: 1px solid {sidebar_border};
            }}
            QWidget#sidebarHeader {{
                background: transparent;
            }}
            QLabel#sidebarTitle {{
                font-size: 22px;
                font-weight: 700;
                color: {text_primary};
            }}
            QLabel#sidebarSubtitle {{
                font-size: 13px;
                font-weight: 400;
                color: {text_muted};
            }}
            QPushButton#navItem {{
                background: transparent;
                border: none;
                border-left: 3px solid transparent;
                border-radius: 0;
                text-align: left;
                padding: 0 20px;
                font-size: 15px;
                font-weight: 500;
                color: {text_secondary};
            }}
            QPushButton#navItem:hover {{
                background-color: {nav_hover};
                color: {text_primary};
            }}
            QPushButton#navItem[active="true"] {{
                background-color: {nav_active};
                border-left: 3px solid {nav_indicator};
                color: {text_primary};
                font-weight: 600;
            }}

            /* ── ScrollBar ── */
            QScrollBar:vertical {{
                background: transparent;
                width: 8px;
                margin: 0;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: {border};
                min-height: 30px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {text_muted};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: none; }}
            QScrollArea {{ border: none; background: transparent; }}

            /* ── Buttons ── */
            QPushButton {{
                background-color: {bg_surface};
                color: {text_primary};
                border: 1px solid {border};
                border-radius: 6px;
                padding: 6px 16px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {bg_surface_hover};
            }}
            QPushButton:pressed {{
                background-color: {bg_surface_selected};
            }}
            QPushButton#primaryBtn, QPushButton#createBtn {{
                background-color: {accent};
                color: {accent_text};
                border: none;
                font-weight: 600;
            }}
            QPushButton#primaryBtn:hover, QPushButton#createBtn:hover {{
                background-color: {accent_hover};
            }}
            QPushButton#dangerBtn {{
                color: {danger};
                border: 1px solid {danger};
                background: transparent;
            }}
            QPushButton#dangerBtn:hover {{
                background-color: {danger};
                color: #ffffff;
            }}
            QPushButton#iconBtn {{
                background: transparent;
                border: none;
                font-size: 18px;
                padding: 4px;
            }}
            QPushButton#iconBtn:hover {{
                background: {bg_surface_hover};
            }}

            /* ── Theme Label ── */
            QLabel#themeLabel {{
                font-size: 14px;
                color: {text_secondary};
            }}

            /* ── Inputs ── */
            QLineEdit {{
                background-color: {bg_input};
                color: {text_primary};
                border: 1px solid {border};
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border-color: {accent};
            }}
            QLineEdit::placeholder {{
                color: {text_muted};
            }}

            /* ── ComboBox ── */
            QComboBox {{
                background-color: {bg_input};
                color: {text_primary};
                border: 1px solid {border};
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 14px;
            }}
            QComboBox:hover {{
                border-color: {text_muted};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 24px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {bg_surface};
                color: {text_primary};
                border: 1px solid {border};
                selection-background-color: {bg_surface_selected};
            }}

            /* ── Project Card ── */
            QFrame#projectCard {{
                background-color: {bg_surface};
                border: 1px solid {border};
                border-radius: 8px;
            }}
            QFrame#projectCard:hover {{
                background-color: {bg_surface_hover};
            }}
            QFrame#projectCard[selected="true"] {{
                background-color: {bg_surface_selected};
                border: 1px solid {accent};
            }}
            QPushButton#cardAvatar {{
                background-color: {accent};
                color: {accent_text};
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
                border: 1px solid {accent};
                padding: 0;
                margin: 0;
            }}
            QLabel#cardName {{
                font-size: 15px;
                font-weight: 600;
            }}
            QLabel#cardPath {{
                font-size: 12px;
                color: {text_secondary};
            }}
            QLabel#cardDate {{
                font-size: 12px;
                color: {text_muted};
            }}
            QPushButton#cardOpenBtn {{
                background: transparent;
                color: {text_secondary};
                border: 1px solid {border};
                border-radius: 6px;
                font-size: 16px;
                padding: 0;
            }}
            QPushButton#cardOpenBtn:hover {{
                background: {bg_surface_hover};
                color: {text_primary};
            }}

            /* ── Version Card (Installs page) ── */
            QFrame#versionCard {{
                background-color: {bg_surface};
                border: 1px solid {border};
                border-radius: 8px;
            }}
            QFrame#versionCard:hover {{
                background-color: {bg_surface_hover};
            }}
            QLabel#versionBadge {{
                font-size: 16px;
                font-weight: 700;
                color: {text_primary};
                padding: 2px 10px;
                background-color: {bg_surface_selected};
                border-radius: 4px;
            }}

            /* ── Version Row (Install Editor dialog) ── */
            QFrame#versionRow {{
                background-color: {bg_surface};
                border: 1px solid transparent;
                border-radius: 6px;
            }}
            QFrame#versionRow:hover {{
                background-color: {bg_surface_hover};
            }}
            QFrame#versionRow[selected="true"] {{
                background-color: {bg_surface_selected};
                border: 1px solid {accent};
            }}
            QLabel#installedBadge {{
                font-size: 12px;
                color: {text_muted};
                font-style: italic;
            }}

            /* ── Page Title ── */
            QLabel#pageTitle {{
                font-size: 24px;
                font-weight: 700;
            }}

            /* ── Empty hint ── */
            QLabel#emptyHint {{
                font-size: 14px;
                color: {text_muted};
                padding: 40px;
            }}

            /* ── Header (legacy) ── */
            QLabel#mainTitle {{
                font-size: 28px;
                font-weight: 700;
            }}
            QLabel#subTitle {{
                font-size: 14px;
                color: {text_muted};
            }}

            /* ── Progress ── */
            QProgressBar {{
                background-color: {bg_surface};
                border: 1px solid {border};
                border-radius: 4px;
                height: 6px;
            }}
            QProgressBar::chunk {{
                background-color: {accent};
                border-radius: 3px;
            }}
        """
