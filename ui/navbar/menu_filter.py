from tkinter import Menu

from features.filter_identity import apply_identity_filter
from features.filter_edge_detection import apply_edge_filter
from features.filter_sharpen import apply_sharpen_filter
from features.filter_gaussian import apply_gaussian_filter
from features.filter_unsharp_masking import apply_unsharp_filter
from features.filter_average import apply_average_filter
from features.filter_low_pass import apply_lowpass_filter
from features.filter_high_pass import apply_highpass_filter
from features.filter_bandstop import apply_bandstop_filter


def create_filter_menu(parent, main_window):
    menu = Menu(parent, tearoff=0, relief="flat", bd=0)
    menu.config(
        bg="white",
        fg="black",
        activebackground="#0078d4",
        activeforeground="white",
    )

    # Placeholder
    menu.add_command(
        label="Identity", command=lambda: apply_identity_filter(main_window)
    )

    # Submenu Edge Detection
    edge_menu = Menu(
        menu,
        tearoff=0,
        relief="flat",
        bd=0,
        bg="white",
        fg="black",
        activebackground="#0078d4",
        activeforeground="white",
    )
    edge_menu.add_command(
        label="Edge Detection 1", command=lambda: apply_edge_filter(main_window, 1)
    )
    edge_menu.add_command(
        label="Edge Detection 2", command=lambda: apply_edge_filter(main_window, 2)
    )
    edge_menu.add_command(
        label="Edge Detection 3", command=lambda: apply_edge_filter(main_window, 3)
    )
    menu.add_cascade(label="Edge Detection", menu=edge_menu)

    menu.add_command(label="Sharpen", command=lambda: apply_sharpen_filter(main_window))

    # Submenu Gaussian Blur
    gauss_menu = Menu(
        menu,
        tearoff=0,
        relief="flat",
        bd=0,
        bg="white",
        fg="black",
        activebackground="#0078d4",
        activeforeground="white",
    )
    gauss_menu.add_command(
        label="Gaussian Blur 3x3", command=lambda: apply_gaussian_filter(main_window, 3)
    )
    gauss_menu.add_command(
        label="Gaussian Blur 5x5", command=lambda: apply_gaussian_filter(main_window, 5)
    )
    menu.add_cascade(label="Gaussian Blur", menu=gauss_menu)

    menu.add_command(
        label="Unsharp Masking", command=lambda: apply_unsharp_filter(main_window)
    )
    menu.add_command(
        label="Avarage Filter", command=lambda: apply_average_filter(main_window)
    )
    menu.add_command(
        label="Low Pass Filter", command=lambda: apply_lowpass_filter(main_window)
    )
    menu.add_command(
        label="High Pass Filter", command=lambda: apply_highpass_filter(main_window)
    )
    menu.add_command(
        label="Bandstop Filter", command=lambda: apply_bandstop_filter(main_window)
    )

    return menu
