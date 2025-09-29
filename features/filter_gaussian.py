from PIL import ImageFilter
from tkinter import messagebox


def apply_gaussian_filter(main_window, size=3):
    # input_img = main_window.get_output_image() or main_window.get_input_image()
    input_img = main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    # Tentukan radius berdasarkan size
    if size == 3:
        radius = 1
    elif size == 5:
        radius = 2
    else:
        messagebox.showwarning("Invalid Size", "Only 3x3 or 5x5 are supported")
        main_window.status_bar.config(text="Invalid Gaussian size")
        return

    # Tampilkan loading
    main_window.show_progress(f"Applying Gaussian Blur {size}x{size}...")
    main_window.root.update()

    # Terapkan Gaussian Blur
    blurred_img = input_img.filter(ImageFilter.GaussianBlur(radius=radius))

    # Set ke output
    main_window.set_output_image(blurred_img)

    # Sembunyikan progress
    main_window.hide_progress()
