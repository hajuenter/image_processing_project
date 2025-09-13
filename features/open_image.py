from tkinter import filedialog, messagebox
from PIL import Image


def open_image(main_window):
    """
    Fungsi untuk membuka gambar dan update ke MainWindow
    main_window: instance dari MainWindow
    """
    file_path = filedialog.askopenfilename(
        title="Select Image File",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("BMP files", "*.bmp"),
            ("All files", "*.*"),
        ],
    )
    if not file_path:
        return

    try:
        img = Image.open(file_path)

        # Simpan gambar asli
        main_window.original_image = img.copy()
        main_window.current_image = img.copy()

        # Tampilkan gambar di input frame
        main_window._resize_and_display_image(main_window.current_image, "left")

        # Clear output frame
        main_window.output_image = None
        main_window.right_label.config(image="", text="Output Image")
        main_window.tk_img_right = None

        # Update status bar
        img_info = f"{img.size[0]}x{img.size[1]} - {img.mode}"
        main_window.status_bar.config(text=f"Opened: {file_path} | Size: {img_info}")

    except Exception as e:
        messagebox.showerror("Error", f"Gagal membuka gambar:\n{str(e)}")
