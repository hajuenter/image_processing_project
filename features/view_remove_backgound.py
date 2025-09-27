from tkinter import messagebox
from PIL import Image
import io
from rembg import remove


def apply_remove_background(main_window):
    input_img = main_window.get_output_image() or main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    mode = input_img.mode
    main_window.show_progress(f"Removing background (mode: {mode})...")
    main_window.root.update()

    try:
        # ==== CASE 1: Grayscale ====
        if mode == "L":
            gray = input_img.convert("L")
            # Threshold: anggap pixel > 240 putih → transparan
            threshold = 240
            alpha = gray.point(lambda p: 0 if p > threshold else 255)
            result = Image.merge("LA", (gray, alpha))

        # ==== CASE 2: RGB / RGBA ====
        else:
            img_bytes = io.BytesIO()
            input_img.save(img_bytes, format="PNG")
            img_bytes = img_bytes.getvalue()

            output_bytes = remove(img_bytes)
            result = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

        main_window.set_output_image(result)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to remove background: {e}")
        main_window.status_bar.config(text=f"Error: {e}")
    finally:
        main_window.hide_progress()
