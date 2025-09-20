from PIL import ImageFilter
from tkinter import messagebox


def apply_lowpass_filter(main_window):
    input_img = main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    main_window.show_progress("Applying Low Pass Filter...")
    main_window.root.update()

    # Low pass pakai blur
    low_img = input_img.filter(ImageFilter.BLUR)

    main_window.set_output_image(low_img)
    main_window.hide_progress()
