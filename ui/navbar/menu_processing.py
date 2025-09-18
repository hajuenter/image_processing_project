from tkinter import Menu


def create_processing_menu(parent, main_window):
    menu = Menu(parent, tearoff=0, relief="flat", bd=0)
    menu.config(
        bg="white",
        fg="black",
        activebackground="#0078d4",
        activeforeground="white",
    )

    # sementara placeholder
    menu.add_command(label="Dummy Processing", command=lambda: print("Processing..."))

    return menu
