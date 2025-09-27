from PIL import Image
from tkinter import messagebox
import numpy as np


def apply_adaptive_thresholding(main_window, block_size=15, C=10, return_image=False):
    """
    Adaptive Thresholding:
    - block_size: ukuran blok lokal (harus ganjil)
    - C: nilai dikurangi dari rata-rata blok
    - return_image: jika True -> return hasil image saja (tanpa update UI)
    """
    input_img = main_window.get_output_image() or main_window.get_input_image()
    if input_img is None:
        if not return_image:
            messagebox.showwarning("No Image", "Please open an image first!")
            main_window.status_bar.config(text="No image loaded")
        return None

    if not return_image:
        # Tampilkan progress bar (pakai konsep color_filter)
        main_window.show_progress("Applying Adaptive Thresholding...")
        main_window.root.update()  # paksa redraw supaya progress bar muncul

    # Pastikan grayscale
    img_gray = input_img.convert("L")
    img_array = np.array(img_gray, dtype=np.uint8)

    # Padding agar blok di tepi tetap bisa dihitung
    pad = block_size // 2
    padded_img = np.pad(img_array, pad, mode="reflect")
    result = np.zeros_like(img_array)

    height, width = img_array.shape
    for y in range(height):
        for x in range(width):
            local_block = padded_img[y : y + block_size, x : x + block_size]
            local_thresh = local_block.mean() - C
            result[y, x] = 255 if img_array[y, x] >= local_thresh else 0

        # Supaya progress bar animasi, update tiap beberapa baris
        if not return_image and y % 20 == 0:
            main_window.root.update_idletasks()

    output_img = Image.fromarray(result)

    if return_image:
        return output_img  # return langsung (dipakai untuk view_all_segmentations)

    # Update ke UI
    main_window.set_output_image(output_img)

    # Tutup progress bar
    main_window.hide_progress()

    main_window.status_bar.config(
        text=f"Adaptive Thresholding applied (block_size={block_size}, C={C})"
    )
    return None
