from tkinter import Menu


def create_edge_menu(parent, main_window):
    menu = Menu(parent, tearoff=0, relief="flat", bd=0)
    menu.config(
        bg="white",
        fg="black",
        activebackground="#0078d4",
        activeforeground="white",
    )

    menu.add_command(
        label="Dummy Edge Detection", command=lambda: print("Edge detection...")
    )

    return menu
