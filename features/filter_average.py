from PIL import ImageFilter
from tkinter import messagebox


def apply_average_filter(main_window):
    input_img = main_window.get_output_image() or main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    main_window.show_progress("Applying Average Filter...")
    main_window.root.update()

    # Kernel rata-rata 3x3
    kernel = (1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9, 1 / 9)
    avg_img = input_img.filter(ImageFilter.Kernel((3, 3), kernel, scale=sum(kernel)))

    main_window.set_output_image(avg_img)
    main_window.hide_progress()
