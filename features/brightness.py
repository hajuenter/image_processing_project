import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageEnhance


def adjust_brightness(main_window):
    """Popup slider untuk brightness"""
    input_img = main_window.get_output_image() or main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    window = tk.Toplevel(main_window.root)
    window.title("Brightness")
    window.geometry("350x120")
    window.resizable(False, False)

    brightness_var = tk.DoubleVar(value=1.0)
    brightness_str = tk.StringVar(value="1.00")

    # Label
    tk.Label(window, text="Brightness").grid(
        row=0, column=0, padx=10, pady=10, sticky="w"
    )

    # Slider
    slider = ttk.Scale(
        window,
        from_=0.1,
        to=5.0,
        orient="horizontal",
        variable=brightness_var,
        command=lambda v: brightness_str.set(f"{float(v):.2f}"),  # update entry
    )
    slider.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    # Entry angka di samping slider
    entry = ttk.Entry(window, textvariable=brightness_str, width=6)
    entry.grid(row=0, column=2, padx=10)

    # Agar slider melar
    window.grid_columnconfigure(1, weight=1)

    # Entry → slider
    def update_from_entry(*args):
        try:
            val = float(brightness_str.get())
            brightness_var.set(val)
            slider.set(val)
        except ValueError:
            pass

    brightness_str.trace_add("write", update_from_entry)

    # Apply
    def apply_changes():
        main_window.show_progress("Adjusting Brightness...")
        try:
            enhancer = ImageEnhance.Brightness(input_img)
            output_img = enhancer.enhance(brightness_var.get())
            main_window.set_output_image(output_img)
        finally:
            main_window.hide_progress()
        window.destroy()

    ttk.Button(window, text="Apply", command=apply_changes).grid(
        row=1, column=0, columnspan=3, pady=10
    )


def adjust_contrast(main_window):
    """Popup slider untuk contrast"""
    input_img = main_window.get_output_image() or main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    window = tk.Toplevel(main_window.root)
    window.title("Contrast")
    window.geometry("350x120")
    window.resizable(False, False)

    contrast_var = tk.DoubleVar(value=1.0)
    contrast_str = tk.StringVar(value="1.00")

    tk.Label(window, text="Contrast").grid(
        row=0, column=0, padx=10, pady=10, sticky="w"
    )

    slider = ttk.Scale(
        window,
        from_=0.1,
        to=5.0,
        orient="horizontal",
        variable=contrast_var,
        command=lambda v: contrast_str.set(f"{float(v):.2f}"),
    )
    slider.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    entry = ttk.Entry(window, textvariable=contrast_str, width=6)
    entry.grid(row=0, column=2, padx=10)

    window.grid_columnconfigure(1, weight=1)

    def update_from_entry(*args):
        try:
            val = float(contrast_str.get())
            contrast_var.set(val)
            slider.set(val)
        except ValueError:
            pass

    contrast_str.trace_add("write", update_from_entry)

    def apply_changes():
        main_window.show_progress("Adjusting Contrast...")
        try:
            enhancer = ImageEnhance.Contrast(input_img)
            output_img = enhancer.enhance(contrast_var.get())
            main_window.set_output_image(output_img)
        finally:
            main_window.hide_progress()
        window.destroy()

    ttk.Button(window, text="Apply", command=apply_changes).grid(
        row=1, column=0, columnspan=3, pady=10
    )
