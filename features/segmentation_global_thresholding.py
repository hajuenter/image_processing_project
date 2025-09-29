from PIL import Image
from tkinter import messagebox


def apply_global_thresholding(main_window, threshold=128, return_image=False):
    """
    Global Thresholding:
    - threshold: nilai ambang (0-255)
    - return_image: jika True -> return hasil image saja (tanpa update UI)
    """
    # input_img = main_window.get_output_image() or main_window.get_input_image()
    input_img = main_window.get_input_image()
    if input_img is None:
        if not return_image:  # hanya beri warning kalau dipanggil dari UI
            messagebox.showwarning("No Image", "Please open an image first!")
            main_window.status_bar.config(text="No image loaded")
        return None

    # Progress bar hanya muncul kalau dari UI
    if not return_image:
        main_window.show_progress("Applying Global Thresholding...")

    # Pastikan grayscale
    img_gray = input_img.convert("L")
    pixels = img_gray.load()

    # Proses thresholding
    for y in range(img_gray.height):
        for x in range(img_gray.width):
            pixels[x, y] = 255 if pixels[x, y] >= threshold else 0

    if return_image:
        return img_gray  # kembalikan hasil ke pemanggil (tidak update UI)

    # Update ke UI
    main_window.set_output_image(img_gray)
    main_window.hide_progress()
    main_window.status_bar.config(
        text=f"Global Thresholding applied (threshold={threshold})"
    )
    return None
