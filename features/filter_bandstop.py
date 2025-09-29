from PIL import ImageFilter, ImageChops
from tkinter import messagebox


def apply_bandstop_filter(main_window):
    # input_img = main_window.get_output_image() or main_window.get_input_image()
    input_img = main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    main_window.show_progress("Applying Bandstop Filter...")
    main_window.root.update()

    # Low-pass (blur)
    low = input_img.filter(ImageFilter.GaussianBlur(radius=2))
    # High-pass (edge emphasis)
    high = input_img.filter(
        ImageFilter.Kernel((3, 3), (-1, -1, -1, -1, 8, -1, -1, -1, -1), scale=1)
    )
    # Bandstop = original - high (hapus frekuensi menengah/tinggi)
    bandstop_img = ImageChops.subtract(low, high)

    main_window.set_output_image(bandstop_img)
    main_window.hide_progress()
