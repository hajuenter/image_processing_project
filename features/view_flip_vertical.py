from PIL import Image
from tkinter import messagebox


def apply_flip_vertical(main_window):
    input_img = main_window.get_input_image()
    # input_img = main_window.get_output_image() or main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    main_window.show_progress("Flipping vertical...")
    main_window.root.update()

    try:
        flipped = input_img.transpose(Image.FLIP_TOP_BOTTOM)
        main_window.set_output_image(flipped)
    except Exception as e:
        main_window.status_bar.config(text=f"Error: {e}")
    finally:
        main_window.hide_progress()
