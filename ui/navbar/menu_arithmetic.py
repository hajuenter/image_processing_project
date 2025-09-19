from tkinter import Menu
from features.arithmetic import arithmetic_operation


def create_arithmetic_menu(parent, main_window):
    menu = Menu(parent, tearoff=0, relief="flat", bd=0)
    menu.config(
        bg="white",
        fg="black",
        activebackground="#0078d4",
        activeforeground="white",
    )

    menu.add_command(
        label="Arithmetic Operation",
        command=lambda: arithmetic_operation(main_window),
    )

    return menu
