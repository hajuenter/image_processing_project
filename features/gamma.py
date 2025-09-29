import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np


def adjust_gamma(main_window):
    """Tampilkan popup untuk Gamma Correction"""
    # input_img = main_window.get_output_image() or main_window.get_input_image()
    input_img = main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    popup = tk.Toplevel(main_window.root)
    popup.title("Gamma Correction")
    popup.geometry("400x180")
    popup.resizable(False, False)

    frame = ttk.Frame(popup, padding=10)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Gamma Correction").pack(anchor="w", pady=(0, 5))

    slider_frame = ttk.Frame(frame)
    slider_frame.pack(fill="x", pady=10)

    gamma_var = tk.DoubleVar(value=1.0)

    # Slider gamma (0.1 – 5.0)
    gamma_slider = ttk.Scale(
        slider_frame,
        from_=0.1,
        to=5.0,
        orient="horizontal",
        variable=gamma_var,
        length=250,
    )
    gamma_slider.pack(side="left", padx=(0, 10))

    gamma_entry = ttk.Entry(slider_frame, textvariable=gamma_var, width=6)
    gamma_entry.pack(side="left")

    # Sinkronisasi slider <-> entry
    def update_entry(*args):
        try:
            val = float(gamma_var.get())
            gamma_entry.delete(0, tk.END)
            gamma_entry.insert(0, f"{val:.2f}")
        except tk.TclError:
            pass

    def update_slider(event):
        try:
            val = float(gamma_entry.get())
            if 0.1 <= val <= 5.0:
                gamma_var.set(val)
        except ValueError:
            pass

    gamma_var.trace_add("write", update_entry)
    gamma_entry.bind("<Return>", update_slider)

    btn_frame = ttk.Frame(frame)
    btn_frame.pack(fill="x", pady=(15, 0))

    def apply_gamma():
        gamma = gamma_var.get()

        # Tampilkan progress di status bar
        main_window.show_progress("Applying Gamma Correction...")
        main_window.root.update()

        def process():
            invGamma = 1.0 / gamma
            table = [((i / 255.0) ** invGamma) * 255 for i in range(256)]
            table = np.array(table).clip(0, 255).astype("uint8")

            # perbaikan di sini
            img_corrected = input_img.point(table.tolist() * len(input_img.getbands()))

            main_window.set_output_image(img_corrected)
            main_window.hide_progress()
            popup.destroy()

        # bisa langsung panggil process() (sinkron)
        # atau tetap pakai after kalau mau non-blocking
        process()

    ttk.Button(btn_frame, text="Apply", command=apply_gamma).pack(
        side="left", expand=True, fill="x", padx=5
    )
    ttk.Button(btn_frame, text="Cancel", command=popup.destroy).pack(
        side="left", expand=True, fill="x", padx=5
    )
