from tkinter import filedialog, messagebox


def save_image(main_window):
    """
    Fungsi untuk menyimpan gambar output dari MainWindow
    main_window: instance dari MainWindow
    """
    if main_window.output_image is None:
        messagebox.showwarning("Warning", "Tidak ada gambar output untuk disimpan!")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg"),
            ("BMP files", "*.bmp"),
            ("All files", "*.*"),
        ],
    )
    if not file_path:
        return

    try:
        main_window.output_image.save(file_path)
        messagebox.showinfo("Info", f"Gambar berhasil disimpan ke:\n{file_path}")
        main_window.status_bar.config(text=f"Saved: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan gambar:\n{str(e)}")
