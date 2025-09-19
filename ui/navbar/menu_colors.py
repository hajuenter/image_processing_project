from tkinter import Menu
from features.rgb import apply_color_filter
from features.rgb_to_grayscale import apply_grayscale
from features import brightness
from features.brightness_contrast import adjust_brightness_contrast
from features.gamma import adjust_gamma
from features.bit_depth import apply_bit_depth
from features.invert import apply_invert
from features.log_brightness import apply_log_brightness


def create_colors_menu(parent, main_window):
    """Membuat Colors menu"""
    colors_menu = Menu(parent, tearoff=0, relief="flat", bd=0)
    colors_menu.config(
        bg="white",
        fg="black",
        activebackground="#0078d4",
        activeforeground="white",
    )

    # Submenu RGB
    rgb_menu = Menu(colors_menu, tearoff=0, relief="flat", bd=0)
    for color in ["Yellow", "Orange", "Cyan", "Purple", "Grey", "Brown", "Red"]:
        rgb_menu.add_command(
            label=color,
            command=lambda c=color: apply_color_filter(main_window, c),
        )
    colors_menu.add_cascade(label="RGB", menu=rgb_menu)

    # Submenu RGB to Grayscale
    grayscale_menu = Menu(colors_menu, tearoff=0, relief="flat", bd=0)
    for method in ["Average", "Lightness", "Luminance"]:
        grayscale_menu.add_command(
            label=method,
            command=lambda m=method: apply_grayscale(main_window, m),
        )
    colors_menu.add_cascade(label="RGB to Grayscale", menu=grayscale_menu)

    # Submenu Brightness & Contrast
    brightness_menu = Menu(colors_menu, tearoff=0, relief="flat", bd=0)
    brightness_menu.add_command(
        label="Brightness",
        command=lambda: brightness.adjust_brightness(main_window),
    )
    brightness_menu.add_command(
        label="Contrast",
        command=lambda: brightness.adjust_contrast(main_window),
    )
    colors_menu.add_cascade(label="Brightness", menu=brightness_menu)

    # Combined Brightness - Contrast
    colors_menu.add_command(
        label="Brightness - Contrast",
        command=lambda: adjust_brightness_contrast(main_window),
    )

    # Invert
    colors_menu.add_command(
        label="Invert",
        command=lambda: apply_invert(main_window),
    )

    # Log Brightness
    colors_menu.add_command(
        label="Log Brightness",
        command=lambda: apply_log_brightness(main_window),
    )

    # Submenu Bit Depth
    bitdepth_menu = Menu(colors_menu, tearoff=0, relief="flat", bd=0)
    for i in range(1, 8):
        bitdepth_menu.add_command(
            label=f"{i} bit",
            command=lambda b=i: apply_bit_depth(main_window, b),
        )
    colors_menu.add_cascade(label="Bit Depth", menu=bitdepth_menu)

    # Gamma Correction
    colors_menu.add_command(
        label="Gamma Correction",
        command=lambda: adjust_gamma(main_window),
    )

    return colors_menu
