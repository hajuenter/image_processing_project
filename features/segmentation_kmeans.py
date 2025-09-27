from PIL import Image
from tkinter import messagebox
import numpy as np


def apply_kmeans(main_window, k=3, max_iter=10, return_image=False):
    """
    K-Means Segmentation:
    - k: jumlah cluster
    - max_iter: jumlah iterasi maksimal
    - return_image: jika True -> return hasil image (tanpa update UI)
    """
    input_img = main_window.get_output_image() or main_window.get_input_image()
    if input_img is None:
        if not return_image:
            messagebox.showwarning("No Image", "Please open an image first!")
            main_window.status_bar.config(text="No image loaded")
        return None

    if not return_image:
        main_window.show_progress(f"Applying K-Means (k={k})...")
        main_window.root.update()  # paksa redraw supaya progress bar langsung tampil

    # Convert ke RGB
    img = input_img.convert("RGB")
    img_array = np.array(img, dtype=np.float32)
    height, width, channels = img_array.shape

    # Reshape jadi 2D array (pixel x 3)
    pixels = img_array.reshape((-1, 3))

    # Inisialisasi centroid secara acak
    np.random.seed(42)
    centroids = pixels[np.random.choice(pixels.shape[0], k, replace=False)]

    for iteration in range(max_iter):
        # Hitung jarak pixel ke centroid
        distances = np.linalg.norm(pixels[:, None] - centroids[None, :], axis=2)
        labels = np.argmin(distances, axis=1)

        # Update centroid
        for i in range(k):
            if np.any(labels == i):
                centroids[i] = pixels[labels == i].mean(axis=0)

        if not return_image:
            # Update progress status tiap iterasi
            main_window.status_bar.config(
                text=f"K-Means iteration {iteration+1}/{max_iter}"
            )
            main_window.root.update_idletasks()

    # Buat image hasil segmentasi
    segmented_pixels = centroids[labels].reshape((height, width, 3)).astype(np.uint8)
    output_img = Image.fromarray(segmented_pixels)

    if return_image:
        return output_img  # dipakai di view_all_segmentations

    # Update UI
    main_window.set_output_image(output_img)
    main_window.hide_progress()
    main_window.status_bar.config(text=f"K-Means applied (k={k}, iter={max_iter})")
    return None
