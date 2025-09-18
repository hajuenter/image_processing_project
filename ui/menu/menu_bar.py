import os
from tkinter import Menu
from PIL import Image, ImageTk

from ui.navbar.menu_file import create_file_menu
from ui.navbar.menu_view import create_view_menu
from ui.navbar.menu_colors import create_colors_menu
from ui.navbar.menu_about import create_about_menu
from ui.navbar.menu_processing import create_processing_menu
from ui.navbar.menu_arithmetic import create_arithmetic_menu
from ui.navbar.menu_filter import create_filter_menu
from ui.navbar.menu_edge import create_edge_menu
from ui.navbar.menu_morfologi import create_morfologi_menu


class MenuBar:
    def __init__(self, main_window):
        self.main_window = main_window
        self.root = main_window.root
        self.menubar = None
        self.icons = {}
        self._load_icons()
        self._create_menu()

    def _file_exists(self, path):
        return os.path.exists(path)

    def _load_icons(self):
        """Load semua icon yang dibutuhkan untuk menu"""

        def load_icon(path, size=(16, 16)):
            try:
                img = Image.open(path).convert("RGBA")
                img = img.resize(size, Image.LANCZOS)
                return ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Icon loading error: {e}")
                return None

        self.icons["open"] = (
            load_icon("icons/open.png") if self._file_exists("icons/open.png") else None
        )
        self.icons["save"] = (
            load_icon("icons/save.png") if self._file_exists("icons/save.png") else None
        )
        self.icons["exit"] = (
            load_icon("icons/exit.png") if self._file_exists("icons/exit.png") else None
        )

    def _create_menu(self):
        self.menubar = Menu(self.root, relief="flat", borderwidth=0)

        # File
        self.menubar.add_cascade(
            label="File",
            menu=create_file_menu(self.menubar, self.main_window, self.icons),
        )

        # View
        self.menubar.add_cascade(
            label="View", menu=create_view_menu(self.menubar, self.main_window)
        )

        # Colors
        self.menubar.add_cascade(
            label="Colors", menu=create_colors_menu(self.menubar, self.main_window)
        )
        # About
        about = create_about_menu(self.menubar)
        self.menubar.add_command(label=about["label"], command=about["command"])

        self.menubar.add_cascade(
            label="Image Processing",
            menu=create_processing_menu(self.menubar, self.main_window),
        )
        self.menubar.add_cascade(
            label="Arithmetical Operation",
            menu=create_arithmetic_menu(self.menubar, self.main_window),
        )
        self.menubar.add_cascade(
            label="Filter", menu=create_filter_menu(self.menubar, self.main_window)
        )
        self.menubar.add_cascade(
            label="Edge Detection",
            menu=create_edge_menu(self.menubar, self.main_window),
        )
        self.menubar.add_cascade(
            label="Morfologi",
            menu=create_morfologi_menu(self.menubar, self.main_window),
        )

        # Set ke root
        self.root.config(menu=self.menubar)
