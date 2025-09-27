from PIL import ImageOps
from tkinter import messagebox


def histogram_equalization(main_window):
    input_img = main_window.get_output_image() or main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    # Tampilkan loading bar
    main_window.show_progress("Applying Histogram Equalization...")
    main_window.root.update()

    # Pastikan grayscale
    img_gray = input_img.convert("L")

    # Histogram equalization pakai PIL
    equalized = ImageOps.equalize(img_gray)

    # Set output image
    main_window.set_output_image(equalized)

    # Sembunyikan progress bar
    main_window.hide_progress()
