from PIL import Image
import time
from tkinter import messagebox


def apply_color_filter(main_window, color):
    input_img = main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    # Tampilkan loading bar
    main_window.show_progress(f"Applying {color} filter...")
    main_window.root.update()  # paksa UI redraw supaya loading muncul

    img = input_img.convert("RGB")
    pixels = img.load()

    color_masks = {
        "Yellow": (255, 255, 0),
        "Orange": (255, 165, 0),
        "Cyan": (0, 255, 255),
        "Purple": (128, 0, 128),
        "Grey": (128, 128, 128),
        "Brown": (139, 69, 19),
        "Red": (255, 0, 0),
    }

    if color not in color_masks:
        main_window.status_bar.config(text="Unknown color filter")
        main_window.hide_progress()
        return

    mask = color_masks[color]

    total_pixels = img.height * img.width
    processed_pixels = 0

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            avg = (r + g + b) // 3
            pixels[x, y] = tuple(min(255, (avg + m) // 2) for m in mask)

            processed_pixels += 1

            # Update progress setiap 1000 pixels untuk performa yang lebih baik
            if processed_pixels % 1000 == 0:
                main_window.root.update_idletasks()

    # Set output image
    main_window.set_output_image(img)

    # Sembunyikan progress bar
    main_window.hide_progress()

    # Status sudah diupdate di set_output_image, tidak perlu pesan tambahan
