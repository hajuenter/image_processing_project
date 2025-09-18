from tkinter import Menu


def create_view_menu(parent, main_window):
    """Membuat View menu"""
    view_menu = Menu(parent, tearoff=0, relief="flat", bd=0)
    view_menu.config(
        bg="white", fg="black", activebackground="#0078d4", activeforeground="white"
    )

    histogram_menu = Menu(view_menu, tearoff=0, relief="flat", bd=0)
    histogram_menu.config(
        bg="white", fg="black", activebackground="#0078d4", activeforeground="white"
    )

    histogram_menu.add_command(
        label="Input", command=lambda: main_window.show_histogram("input")
    )
    histogram_menu.add_command(
        label="Output", command=lambda: main_window.show_histogram("output")
    )
    histogram_menu.add_command(
        label="Input dan Output",
        command=lambda: main_window.show_histogram("both"),
    )

    view_menu.add_cascade(label="Histogram", menu=histogram_menu)

    return view_menu
