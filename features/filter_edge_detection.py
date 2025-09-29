from PIL import Image, ImageFilter
from tkinter import messagebox


def apply_edge_filter(main_window, mode=1):
    # input_img = main_window.get_output_image() or main_window.get_input_image()
    input_img = main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    main_window.show_progress(f"Applying Edge Detection {mode}...")
    main_window.root.update()

    img = input_img.convert("L")  # ubah grayscale dulu
    kernel = None

    if mode == 1:  # Prewitt
        kernel = (-1, 0, 1, -1, 0, 1, -1, 0, 1)
    elif mode == 2:  # Sobel
        kernel = (-1, 0, 1, -2, 0, 2, -1, 0, 1)
    elif mode == 3:  # Laplacian
        kernel = (0, -1, 0, -1, 4, -1, 0, -1, 0)
    else:
        main_window.status_bar.config(text="Unknown edge detection mode")
        main_window.hide_progress()
        return

    # Terapkan kernel dengan PIL.ImageFilter.Kernel
    edge_img = img.filter(ImageFilter.Kernel((3, 3), kernel, scale=1, offset=0))

    main_window.set_output_image(edge_img)
    main_window.hide_progress()
