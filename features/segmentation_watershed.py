from PIL import Image
from tkinter import messagebox
import numpy as np
from skimage import segmentation, color, filters, util


def apply_watershed(main_window, return_image=False):
    """
    Watershed Segmentation:
    - return_image: jika True -> return PIL.Image tanpa update UI
    """
    input_img = main_window.get_input_image()
    if input_img is None:
        if not return_image:
            messagebox.showwarning("No Image", "Please open an image first!")
            main_window.status_bar.config(text="No image loaded")
        return None

    if not return_image:
        main_window.show_progress("Applying Watershed Segmentation...")

    try:
        # 1. Convert ke grayscale array
        img_gray = input_img.convert("L")
        img_array = np.array(img_gray)

        # 2. Normalisasi ke float [0..1]
        img_float = util.img_as_float(img_array)

        # 3. Hitung gradient pakai Sobel (lebih jelas untuk watershed)
        gradient = filters.sobel(img_float)

        # 4. Threshold Otsu → buat markers
        thresh_val = filters.threshold_otsu(img_float)
        markers = np.zeros(img_float.shape, dtype=np.int32)
        markers[img_float < thresh_val * 0.5] = 1  # background marker
        markers[img_float > thresh_val * 1.0] = 2  # object marker

        # 5. Pastikan array contiguous (mencegah error Cython)
        gradient = np.ascontiguousarray(gradient)
        markers = np.ascontiguousarray(markers)

        # 6. Jalankan watershed
        ws_labels = segmentation.watershed(gradient, markers)

        # 7. Konversi hasil label → RGB
        ws_rgb = color.label2rgb(ws_labels, bg_label=0)
        ws_rgb_img = Image.fromarray((ws_rgb * 255).astype(np.uint8))

    except Exception as e:
        if not return_image:
            main_window.hide_progress()
            main_window.status_bar.config(text="Watershed failed")
        messagebox.showerror("Watershed Error", f"Watershed failed:\n{e}")
        return None

    if return_image:
        return ws_rgb_img  # dipakai di "view_all_segmentations"

    # Update ke UI
    main_window.set_output_image(ws_rgb_img)
    main_window.hide_progress()
    main_window.status_bar.config(text="Watershed Segmentation applied")
    return None
