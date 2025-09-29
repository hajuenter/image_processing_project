from tkinter import messagebox
import numpy as np
from PIL import Image, ImageOps


def apply_invert(main_window):
    """Balikkan warna gambar (invert)"""
    # input_img = main_window.get_output_image() or main_window.get_input_image()
    input_img = main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    main_window.show_progress("Applying Invert...")

    try:
        # Konversi ke RGB biar konsisten
        img = input_img.convert("RGB")
        inverted_img = ImageOps.invert(img)
        main_window.set_output_image(inverted_img)
    finally:
        main_window.hide_progress()
