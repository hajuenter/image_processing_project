import tkinter as tk
from tkinter import messagebox
import numpy as np
from PIL import Image


def apply_bit_depth(main_window, bits: int):
    """
    Ubah kedalaman bit gambar (1 - 8 bit).
    """
    input_img = main_window.get_output_image() or main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    main_window.show_progress(f"Applying {bits}-bit...")

    try:
        # Konversi ke grayscale dulu
        gray = input_img.convert("L")
        arr = np.array(gray)

        # Normalisasi nilai 0-255 ke level bit tertentu
        levels = 2**bits
        arr = np.floor(arr / (256 / levels)) * (256 / levels)
        arr = arr.astype(np.uint8)

        # Convert kembali ke PIL
        out_img = Image.fromarray(arr, mode="L")
        main_window.set_output_image(out_img)
    finally:
        main_window.hide_progress()
