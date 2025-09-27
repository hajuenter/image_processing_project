from PIL import Image
from tkinter import messagebox


def apply_rotate(main_window, angle=90):
    """
    Rotasi gambar sesuai sudut (default 90 derajat).
    """
    input_img = main_window.get_output_image() or main_window.get_input_image()

    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    main_window.show_progress(f"Rotating {angle} degrees...")
    main_window.root.update()

    try:
        rotated = input_img.rotate(angle, expand=True)
        main_window.set_output_image(rotated)
    except Exception as e:
        main_window.status_bar.config(text=f"Error: {e}")
    finally:
        main_window.hide_progress()

