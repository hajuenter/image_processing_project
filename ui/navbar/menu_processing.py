from tkinter import Menu
from features.fuzzy import fuzzy_grayscale, fuzzy_rgb
from features.histogram_equalization import histogram_equalization


def create_processing_menu(parent, main_window):
    """Membuat Processing menu"""
    processing_menu = Menu(parent, tearoff=0, relief="flat", bd=0)
    processing_menu.config(
        bg="white",
        fg="black",
        activebackground="#0078d4",
        activeforeground="white",
    )

    # Histogram Equalization
    processing_menu.add_command(
        label="Histogram Equalization",
        command=lambda: histogram_equalization(main_window),
    )

    # Submenu Fuzzy
    fuzzy_menu = Menu(processing_menu, tearoff=0, relief="flat", bd=0)
    fuzzy_menu.add_command(
        label="Fuzzy HE RGB",
        command=lambda: fuzzy_rgb(main_window),
    )
    fuzzy_menu.add_command(
        label="Fuzzy Grayscale",
        command=lambda: fuzzy_grayscale(main_window),
    )
    processing_menu.add_cascade(label="Fuzzy", menu=fuzzy_menu)

    return processing_menu
