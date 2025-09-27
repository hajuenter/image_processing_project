from tkinter import Toplevel, Label, Button, Frame, messagebox
from PIL import Image, ImageTk
import numpy as np


def arithmetic_operation(main_window):
    img1 = main_window.get_input_image()
    img2 = main_window.get_output_image()

    if img1 is None and img2 is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        return

    # fallback: kalau output image belum ada, pakai input image juga
    if img2 is None:
        img2 = img1.copy()

    # Samakan ukuran gambar biar bisa dioperasikan
    img2 = img2.resize(img1.size)

    # Convert ke array numpy (pakai float biar pembagian lebih halus)
    arr1 = np.array(img1.convert("RGB"), dtype=np.float32)
    arr2 = np.array(img2.convert("RGB"), dtype=np.float32)

    # Buat window baru
    win = Toplevel(main_window.root)
    win.title("Arithmetic Operations")

    # Frame utama untuk gambar (horizontal)
    img_frame = Frame(win)
    img_frame.pack(pady=10)

    # --- Input 1 ---
    Label(img_frame, text="Input 1").grid(row=0, column=0, pady=5)
    img1_resized = img1.resize((200, 200))
    img1_tk = ImageTk.PhotoImage(img1_resized)
    Label(img_frame, image=img1_tk).grid(row=1, column=0, padx=10)

    # --- Input 2 ---
    Label(img_frame, text="Input 2").grid(row=0, column=1, pady=5)
    img2_resized = img2.resize((200, 200))
    img2_tk = ImageTk.PhotoImage(img2_resized)
    Label(img_frame, image=img2_tk).grid(row=1, column=1, padx=10)

    # --- Output ---
    Label(img_frame, text="Output").grid(row=0, column=2, pady=5)
    # Placeholder abu-abu 200x200
    placeholder = Image.new("RGB", (200, 200), color=(200, 200, 200))
    placeholder_tk = ImageTk.PhotoImage(placeholder)
    preview_label = Label(img_frame, image=placeholder_tk)
    preview_label.grid(row=1, column=2, padx=10)

    # Frame untuk tombol operasi
    button_frame = Frame(win)
    button_frame.pack(pady=10)

    def show_result(result_arr):
        result_arr = np.clip(result_arr, 0, 255).astype(np.uint8)
        result_img = Image.fromarray(result_arr)
        tk_img = ImageTk.PhotoImage(result_img.resize((200, 200)))
        preview_label.config(image=tk_img)
        preview_label.image = tk_img
        main_window.set_output_image(result_img)

    def divide_arrays(a, b):
        result = np.zeros_like(a, dtype=np.float32)
        mask = b != 0
        result[mask] = a[mask] / b[mask] * 255  # skala ke 0–255
        return result

    # Tombol operasi
    Button(
        button_frame, text="Add", width=12, command=lambda: show_result(arr1 + arr2)
    ).grid(row=0, column=0, padx=5)
    Button(
        button_frame,
        text="Subtract",
        width=12,
        command=lambda: show_result(arr1 - arr2),
    ).grid(row=0, column=1, padx=5)
    Button(
        button_frame,
        text="Multiply",
        width=12,
        command=lambda: show_result(arr1 * arr2 / 255.0),
    ).grid(row=0, column=2, padx=5)
    Button(
        button_frame,
        text="Divide",
        width=12,
        command=lambda: show_result(divide_arrays(arr1, arr2)),
    ).grid(row=0, column=3, padx=5)

    # Simpan reference biar tidak ke-garbage collect
    win.img1_tk = img1_tk
    win.img2_tk = img2_tk
    win.placeholder_tk = placeholder_tk
