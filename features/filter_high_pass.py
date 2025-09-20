from PIL import ImageFilter
from tkinter import messagebox


def apply_highpass_filter(main_window):
    input_img = main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    main_window.show_progress("Applying High Pass Filter...")
    main_window.root.update()

    # Kernel high-pass 3x3
    kernel = (-1, -1, -1, -1, 8, -1, -1, -1, -1)
    high_img = input_img.convert("L").filter(
        ImageFilter.Kernel((3, 3), kernel, scale=1)
    )

    main_window.set_output_image(high_img)
    main_window.hide_progress()
