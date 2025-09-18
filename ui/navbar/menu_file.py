import os
from tkinter import Menu
from PIL import Image, ImageTk


def create_file_menu(parent, main_window, icons):
    """Membuat File menu"""
    file_menu = Menu(parent, tearoff=0, relief="flat", bd=0)
    file_menu.config(
        bg="white",
        fg="black",
        activebackground="#0078d4",
        activeforeground="white",
        selectcolor="#0078d4",
    )

    file_menu.add_command(
        label="Open",
        command=main_window.open_image_wrapper,
        image=icons.get("open"),
        compound="left",
    )
    file_menu.add_command(
        label="Save",
        command=main_window.save_image_wrapper,
        image=icons.get("save"),
        compound="left",
    )
    file_menu.add_separator()
    file_menu.add_command(
        label="Exit",
        command=main_window.root.quit,
        image=icons.get("exit"),
        compound="left",
    )
    return file_menu
