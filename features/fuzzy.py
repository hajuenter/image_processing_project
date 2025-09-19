from PIL import Image
import numpy as np
from tkinter import messagebox


def fuzzy_rgb(main_window):
    input_img = main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    main_window.show_progress("Applying Fuzzy RGB...")
    main_window.root.update()

    img = input_img.convert("RGB")
    arr = np.array(img).astype(np.float32) / 255.0

    # Fuzzy enhancement sederhana: gamma < 1 → lebih terang
    fuzzy = np.power(arr, 0.8)
    fuzzy = (fuzzy * 255).astype(np.uint8)
    out_img = Image.fromarray(fuzzy)

    main_window.set_output_image(out_img)
    main_window.hide_progress()


def fuzzy_grayscale(main_window):
    input_img = main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    main_window.show_progress("Applying Fuzzy Grayscale...")
    main_window.root.update()

    img = input_img.convert("L")
    arr = np.array(img).astype(np.float32) / 255.0

    # Fuzzy enhancement sederhana: gamma > 1 → lebih gelap
    fuzzy = np.power(arr, 1.2)
    fuzzy = (fuzzy * 255).astype(np.uint8)
    out_img = Image.fromarray(fuzzy)

    main_window.set_output_image(out_img)
    main_window.hide_progress()
