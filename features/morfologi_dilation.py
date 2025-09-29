import numpy as np
from PIL import Image
from tkinter import messagebox
from scipy.ndimage import binary_dilation


def apply_dilation(main_window, kernel_type="square", size=3):
    # input_img = main_window.get_output_image() or main_window.get_input_image()
    input_img = main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    main_window.show_progress(f"Applying Dilation ({kernel_type} {size})...")
    main_window.root.update()

    # Convert ke grayscale lalu biner
    gray = input_img.convert("L")
    img_array = np.array(gray)
    binary = img_array > 128  # threshold sederhana

    # Buat structuring element
    if kernel_type == "square":
        selem = np.ones((size, size), dtype=bool)
    elif kernel_type == "cross":
        selem = np.zeros((size, size), dtype=bool)
        center = size // 2
        selem[center, :] = True
        selem[:, center] = True
    else:
        selem = np.ones((size, size), dtype=bool)

    # Apply dilation
    dilated = binary_dilation(binary, structure=selem).astype(np.uint8) * 255

    output_img = Image.fromarray(dilated)

    main_window.set_output_image(output_img)
    main_window.hide_progress()
