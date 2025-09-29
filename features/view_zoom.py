from PIL import Image
from tkinter import messagebox


def apply_zoom(main_window, mode="in"):
    """
    Zoom gambar:
    - mode='in'  : zoom in (crop tengah)
    - mode='out' : zoom out (perkecil dan beri padding putih)
    - mode='reset': kembalikan ke original
    """
    if main_window.original_image is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    if mode == "reset":
        main_window.set_output_image(main_window.original_image.copy())
        main_window.status_bar.config(text="Image reset to original")
        return
    input_img = main_window.get_input_image()
    # input_img = main_window.get_output_image() or main_window.get_input_image()
    main_window.show_progress(f"Zooming {mode}...")
    main_window.root.update()

    try:
        w, h = input_img.size

        if mode == "in":
            crop_w, crop_h = int(w * 0.8), int(h * 0.8)
            left = (w - crop_w) // 2
            top = (h - crop_h) // 2
            right = left + crop_w
            bottom = top + crop_h
            zoomed = input_img.crop((left, top, right, bottom))
            zoomed = zoomed.resize((w, h), Image.Resampling.LANCZOS)

        elif mode == "out":
            shrink = input_img.resize(
                (int(w * 0.8), int(h * 0.8)), Image.Resampling.LANCZOS
            )
            zoomed = Image.new("RGB", (w, h), "white")
            offset_x = (w - shrink.size[0]) // 2
            offset_y = (h - shrink.size[1]) // 2
            zoomed.paste(shrink, (offset_x, offset_y))

        main_window.set_output_image(zoomed)

    except Exception as e:
        main_window.status_bar.config(text=f"Error: {e}")
    finally:
        main_window.hide_progress()
