from PIL import ImageFilter
from tkinter import messagebox


def apply_unsharp_filter(main_window, radius=2, percent=150, threshold=3):
    # input_img = main_window.get_output_image() or main_window.get_input_image()
    input_img = main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    # Tampilkan loading
    main_window.show_progress("Applying Unsharp Masking...")
    main_window.root.update()

    # Terapkan Unsharp Mask
    unsharp_img = input_img.filter(
        ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold)
    )

    # Set ke output
    main_window.set_output_image(unsharp_img)

    # Sembunyikan progress
    main_window.hide_progress()
