from PIL import Image
from tkinter import messagebox
import numpy as np
from collections import deque


def apply_region_growing(main_window, seed=None, threshold=15, return_image=False):
    """
    Region Growing Segmentation:
    - seed: koordinat awal (x, y), default di tengah gambar
    - threshold: toleransi perbedaan intensitas
    - return_image: jika True -> return hasil image tanpa update UI
    """
    input_img = main_window.get_input_image()
    # input_img = main_window.get_output_image() or main_window.get_input_image()
    if input_img is None:
        if not return_image:
            messagebox.showwarning("No Image", "Please open an image first!")
            main_window.status_bar.config(text="No image loaded")
        return None

    if not return_image:
        main_window.show_progress("Applying Region Growing...")
        main_window.root.update()  # supaya progress langsung tampil

    img_gray = input_img.convert("L")
    img_array = np.array(img_gray, dtype=np.int32)
    height, width = img_array.shape
    total_pixels = height * width

    # Tentukan seed default di tengah gambar jika tidak ada
    if seed is None:
        seed = (width // 2, height // 2)

    visited = np.zeros_like(img_array, dtype=bool)
    result = np.zeros_like(img_array, dtype=np.uint8)

    # Ambil nilai intensitas seed
    seed_value = img_array[seed[1], seed[0]]

    # BFS queue
    q = deque()
    q.append(seed)
    visited[seed[1], seed[0]] = True

    # 8-neighborhood
    neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    processed_pixels = 0

    while q:
        x, y = q.popleft()
        result[y, x] = 255  # set pixel sebagai bagian region
        processed_pixels += 1

        for dx, dy in neighbors:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and not visited[ny, nx]:
                if abs(int(img_array[ny, nx]) - int(seed_value)) <= threshold:
                    q.append((nx, ny))
                    visited[ny, nx] = True

        if not return_image and processed_pixels % 1000 == 0:
            progress = int((processed_pixels / total_pixels) * 100)
            main_window.status_bar.config(text=f"Region Growing... {progress}%")
            main_window.root.update_idletasks()

    output_img = Image.fromarray(result)

    if return_image:
        return output_img  # dipakai untuk view_all_segmentations

    # Update ke UI
    main_window.set_output_image(output_img)
    main_window.hide_progress()
    main_window.status_bar.config(
        text=f"Region Growing applied (seed={seed}, threshold={threshold})"
    )
    return None
