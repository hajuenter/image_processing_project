from tkinter import Menu


def create_arithmetic_menu(parent, main_window):
    menu = Menu(parent, tearoff=0, relief="flat", bd=0)
    menu.config(
        bg="white",
        fg="black",
        activebackground="#0078d4",
        activeforeground="white",
    )

    # sementara placeholder
    menu.add_command(label="Dummy Arithmetic", command=lambda: print("Arithmetic..."))

    return menu
