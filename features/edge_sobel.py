import numpy as np
from PIL import Image
from tkinter import messagebox
from scipy.signal import convolve2d


def apply_sobel(main_window):
    # input_img = main_window.get_output_image() or main_window.get_input_image()
    input_img = main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    main_window.show_progress("Applying Sobel filter...")
    main_window.root.update()

    # Convert to grayscale
    gray = input_img.convert("L")
    img_array = np.array(gray, dtype=np.float32)

    # Sobel kernels
    kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)

    kernel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)

    # Convolve with SciPy
    gx = convolve2d(img_array, kernel_x, mode="same", boundary="symm")
    gy = convolve2d(img_array, kernel_y, mode="same", boundary="symm")

    g = np.sqrt(gx**2 + gy**2)

    # Normalize ke 0–255
    g = (g / g.max()) * 255
    g = g.astype(np.uint8)

    output_img = Image.fromarray(g)

    main_window.set_output_image(output_img)
    main_window.hide_progress()
