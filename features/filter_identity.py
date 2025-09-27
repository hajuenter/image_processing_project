from PIL import Image
from tkinter import messagebox


def apply_identity_filter(main_window):
    input_img = main_window.get_output_image() or main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    # Tampilkan loading bar
    main_window.show_progress("Applying Identity filter...")
    main_window.root.update()

    # Pastikan gambar dalam mode RGB
    img = input_img.convert("RGB").copy()

    # Simulasi progress supaya konsisten dengan filter lain
    width, height = img.size
    pixels = img.load()
    total_pixels = width * height
    processed_pixels = 0

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            # identity: tidak ada perubahan
            pixels[x, y] = (r, g, b)

            processed_pixels += 1
            if processed_pixels % 1000 == 0:
                main_window.root.update_idletasks()

    # Set output image
    main_window.set_output_image(img)

    # Sembunyikan progress bar
    main_window.hide_progress()
