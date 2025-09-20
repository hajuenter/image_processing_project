from tkinter import Menu
from features.erosion import apply_erosion
from features.dilation import apply_dilation
from features.opening import apply_opening
from features.closing import apply_closing


def create_morfologi_menu(parent, main_window):
    menu = Menu(parent, tearoff=0, relief="flat", bd=0)
    menu.config(
        bg="white",
        fg="black",
        activebackground="#0078d4",
        activeforeground="white",
    )

    # Erosion submenu
    erosion_menu = Menu(
        menu,
        tearoff=0,
        relief="flat",
        bd=0,
        bg="white",
        fg="black",
        activebackground="#0078d4",
        activeforeground="white",
    )
    erosion_menu.add_command(
        label="Square 3", command=lambda: apply_erosion(main_window, "square", 3)
    )
    erosion_menu.add_command(
        label="Square 5", command=lambda: apply_erosion(main_window, "square", 5)
    )
    erosion_menu.add_command(
        label="Cross 3", command=lambda: apply_erosion(main_window, "cross", 3)
    )
    menu.add_cascade(label="Erosion", menu=erosion_menu)

    # Dilation submenu
    dilation_menu = Menu(
        menu,
        tearoff=0,
        relief="flat",
        bd=0,
        bg="white",
        fg="black",
        activebackground="#0078d4",
        activeforeground="white",
    )
    dilation_menu.add_command(
        label="Square 3", command=lambda: apply_dilation(main_window, "square", 3)
    )
    dilation_menu.add_command(
        label="Square 5", command=lambda: apply_dilation(main_window, "square", 5)
    )
    dilation_menu.add_command(
        label="Cross 3", command=lambda: apply_dilation(main_window, "cross", 3)
    )
    menu.add_cascade(label="Dilation", menu=dilation_menu)

    # Opening submenu (Square 9)
    opening_menu = Menu(
        menu,
        tearoff=0,
        relief="flat",
        bd=0,
        bg="white",
        fg="black",
        activebackground="#0078d4",
        activeforeground="white",
    )
    opening_menu.add_command(
        label="Square 9", command=lambda: apply_opening(main_window, "square", 9)
    )
    menu.add_cascade(label="Opening", menu=opening_menu)

    # Closing submenu (Square 9)
    closing_menu = Menu(
        menu,
        tearoff=0,
        relief="flat",
        bd=0,
        bg="white",
        fg="black",
        activebackground="#0078d4",
        activeforeground="white",
    )
    closing_menu.add_command(
        label="Square 9", command=lambda: apply_closing(main_window, "square", 9)
    )
    menu.add_cascade(label="Closing", menu=closing_menu)

    return menu
