from PIL import Image
from tkinter import messagebox


def apply_grayscale(main_window, method="Average"):
    input_img = main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    # Tampilkan loading bar
    main_window.show_progress(f"Converting to Grayscale ({method})...")
    main_window.root.update()

    img = input_img.convert("RGB")
    pixels = img.load()

    total_pixels = img.width * img.height
    processed_pixels = 0

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]

            if method == "Average":
                gray = (r + g + b) // 3
            elif method == "Lightness":
                gray = (max(r, g, b) + min(r, g, b)) // 2
            elif method == "Luminance":
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            else:
                gray = (r + g + b) // 3  # fallback

            pixels[x, y] = (gray, gray, gray)

            processed_pixels += 1
            if processed_pixels % 1000 == 0:
                main_window.root.update_idletasks()

    # Set output ke main_window
    main_window.set_output_image(img)

    # Tutup loading bar
    main_window.hide_progress()
