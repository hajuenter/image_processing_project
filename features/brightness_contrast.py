import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageEnhance


def adjust_brightness_contrast(main_window):
    """
    Membuka jendela popup untuk atur Brightness & Contrast
    """
    # --- Cek apakah ada gambar input dulu ---
    input_img = main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    # --- Kalau ada gambar baru buka popup ---
    window = tk.Toplevel(main_window.root)
    window.title("Brightness & Contrast")
    window.geometry("350x180")
    window.resizable(False, False)

    # Variabel slider
    brightness_var = tk.DoubleVar(value=1.0)  # default 1.0 = normal
    contrast_var = tk.DoubleVar(value=1.0)

    # --- Brightness ---
    tk.Label(window, text="Brightness").grid(
        row=0, column=0, padx=10, pady=10, sticky="w"
    )

    brightness_slider = ttk.Scale(
        window, from_=0.1, to=3.0, orient="horizontal", variable=brightness_var
    )
    brightness_slider.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    brightness_entry = ttk.Entry(window, width=6)
    brightness_entry.grid(row=0, column=2, padx=10)

    # --- Contrast ---
    tk.Label(window, text="Contrast").grid(
        row=1, column=0, padx=10, pady=10, sticky="w"
    )

    contrast_slider = ttk.Scale(
        window, from_=0.1, to=3.0, orient="horizontal", variable=contrast_var
    )
    contrast_slider.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    contrast_entry = ttk.Entry(window, width=6)
    contrast_entry.grid(row=1, column=2, padx=10)

    window.grid_columnconfigure(1, weight=1)

    # --- Sinkronisasi angka <-> slider ---
    def update_entry(var, entry):
        try:
            entry.delete(0, tk.END)
            entry.insert(0, f"{var.get():.2f}")
        except tk.TclError:
            pass

    def update_var(entry, var, slider):
        try:
            val = float(entry.get())
            var.set(val)
            slider.set(val)
        except ValueError:
            pass

    update_entry(brightness_var, brightness_entry)
    update_entry(contrast_var, contrast_entry)

    brightness_var.trace_add(
        "write", lambda *args: update_entry(brightness_var, brightness_entry)
    )
    contrast_var.trace_add(
        "write", lambda *args: update_entry(contrast_var, contrast_entry)
    )

    brightness_entry.bind(
        "<KeyRelease>",
        lambda e: update_var(brightness_entry, brightness_var, brightness_slider),
    )
    contrast_entry.bind(
        "<KeyRelease>",
        lambda e: update_var(contrast_entry, contrast_var, contrast_slider),
    )

    # Fungsi Apply
    def apply_changes():
        main_window.show_progress("Applying Brightness & Contrast...")
        try:
            enhancer_b = ImageEnhance.Brightness(input_img)
            img_b = enhancer_b.enhance(brightness_var.get())

            enhancer_c = ImageEnhance.Contrast(img_b)
            img_c = enhancer_c.enhance(contrast_var.get())

            main_window.set_output_image(img_c)
        finally:
            main_window.hide_progress()

        window.destroy()

    # Fungsi Reset
    def reset_values():
        brightness_var.set(1.0)
        contrast_var.set(1.0)

    # Tombol
    button_frame = tk.Frame(window)
    button_frame.grid(row=2, column=0, columnspan=3, pady=15)

    ttk.Button(button_frame, text="Apply", command=apply_changes).pack(
        side="left", padx=10
    )
    ttk.Button(button_frame, text="Reset", command=reset_values).pack(
        side="left", padx=10
    )
