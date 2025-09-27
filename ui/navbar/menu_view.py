from tkinter import Menu, simpledialog
from features.view_flip_horizontal import apply_flip_horizontal
from features.view_flip_vertical import apply_flip_vertical
from features.view_rotate import apply_rotate
from features.view_translate import apply_translate
from features.view_zoom import apply_zoom
from features.view_crop import apply_crop


def create_view_menu(parent, main_window):
    view_menu = Menu(parent, tearoff=0, relief="flat", bd=0)
    view_menu.config(
        bg="white", fg="black", activebackground="#0078d4", activeforeground="white"
    )

    # Histogram submenu
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
        label="Input dan Output", command=lambda: main_window.show_histogram("both")
    )
    view_menu.add_cascade(label="Histogram", menu=histogram_menu)

    # Flip langsung
    view_menu.add_command(
        label="Flip Horizontal", command=lambda: apply_flip_horizontal(main_window)
    )
    view_menu.add_command(
        label="Flip Vertical", command=lambda: apply_flip_vertical(main_window)
    )

    # Rotate submenu
    rotate_menu = Menu(view_menu, tearoff=0, relief="flat", bd=0)
    rotate_menu.config(
        bg="white", fg="black", activebackground="#0078d4", activeforeground="white"
    )
    rotate_menu.add_command(label="90°", command=lambda: apply_rotate(main_window, 90))
    rotate_menu.add_command(
        label="180°", command=lambda: apply_rotate(main_window, 180)
    )
    rotate_menu.add_command(
        label="270°", command=lambda: apply_rotate(main_window, 270)
    )
    view_menu.add_cascade(label="Rotate", menu=rotate_menu)

    view_menu.add_command(
        label="Translate", command=lambda: apply_translate(main_window)
    )

    zoom_menu = Menu(view_menu, tearoff=0, relief="flat", bd=0)
    zoom_menu.add_command(label="In", command=lambda: apply_zoom(main_window, "in"))
    zoom_menu.add_command(label="Out", command=lambda: apply_zoom(main_window, "out"))
    view_menu.add_cascade(label="Zoom", menu=zoom_menu)
    view_menu.add_command(label="Crop", command=lambda: apply_crop(main_window))
    return view_menu
