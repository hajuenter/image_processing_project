from tkinter import messagebox


def create_about_menu(parent):
    """Membuat menu Tentang"""
    return {
        "label": "Tentang",
        "command": lambda: messagebox.showinfo(
            "Tentang", "Aplikasi GUI Python\nVersion 1.0"
        ),
    }
