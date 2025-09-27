from tkinter import messagebox
import numpy as np
from PIL import Image


def apply_log_brightness(main_window, c=30):
    """Terapkan transformasi log brightness pada gambar"""
    input_img = main_window.get_output_image() or main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    main_window.show_progress("Applying Log Brightness...")

    try:
        img = input_img.convert("L")  # grayscale dulu
        arr = np.array(img, dtype=np.float32)

        # Transformasi log
        arr = c * np.log1p(arr)
        arr = np.clip(arr, 0, 255).astype(np.uint8)

        # Balik ke PIL Image
        log_img = Image.fromarray(arr, mode="L")
        main_window.set_output_image(log_img)
    finally:
        main_window.hide_progress()
