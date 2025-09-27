from tkinter import Menu
from features.edge_prewitt import apply_prewitt
from features.edge_sobel import apply_sobel


def create_edge_menu(parent, main_window):
    menu = Menu(parent, tearoff=0, relief="flat", bd=0)
    menu.config(
        bg="white",
        fg="black",
        activebackground="#0078d4",
        activeforeground="white",
    )

    menu.add_command(label="Prewitt", command=lambda: apply_prewitt(main_window))
    menu.add_command(label="Sobel", command=lambda: apply_sobel(main_window))

    return menu
