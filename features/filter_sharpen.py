from PIL import ImageFilter
from tkinter import messagebox


def apply_sharpen_filter(main_window):
    # input_img = main_window.get_output_image() or main_window.get_input_image()
    input_img = main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    # Tampilkan loading
    main_window.show_progress("Applying Sharpen filter...")
    main_window.root.update()

    # Terapkan sharpen
    sharpened_img = input_img.filter(ImageFilter.SHARPEN)

    # Set ke output
    main_window.set_output_image(sharpened_img)

    # Sembunyikan progress
    main_window.hide_progress()
