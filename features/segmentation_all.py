from features.segmentation_global_thresholding import apply_global_thresholding
from features.segmentation_adaptive_thresholding import apply_adaptive_thresholding
from features.segmentation_kmeans import apply_kmeans
from features.segmentation_watershed import apply_watershed
from features.segmentation_region_growing import apply_region_growing
from tkinter import Toplevel, Frame, Label, messagebox
from PIL import ImageTk


def view_all_segmentations(main_window):
    """
    Tampilkan hasil semua metode segmentasi dalam satu jendela baru,
    dengan progress bar hijau selama proses berjalan.
    Semua gambar ditampilkan horizontal dengan ukuran seragam dan center.
    """
    input_img = main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        return

    methods = [
        ("Global Thresholding", apply_global_thresholding),
        ("Adaptive Thresholding", apply_adaptive_thresholding),
        ("K-Means", apply_kmeans),
        ("Watershed", apply_watershed),
        ("Region Growing", apply_region_growing),
    ]
    total = len(methods)

    # --- Konfigurasi ukuran gambar ---
    img_width = 200
    padding = 30
    # ---------------------------------

    # Buat window baru
    new_win = Toplevel(main_window.root)
    new_win.title("All Segmentations")

    # Container utama
    container = Frame(new_win)
    container.pack(expand=True, fill="both")

    # Frame horizontal mulai dari kiri
    images_frame = Frame(container)
    images_frame.pack(side="top", anchor="w", pady=20)

    for i, (name, func) in enumerate(methods, start=0):
        main_window.show_progress(f"Applying {name} ({i+1}/{total})...")
        main_window.root.update_idletasks()

        result = func(main_window, return_image=True)
        if result is not None:
            # Resize hasil supaya seragam
            resized = result.resize((img_width, img_width))  # ukuran fix
            tk_img = ImageTk.PhotoImage(resized)

            # Frame tiap metode
            frame = Frame(images_frame, padx=15, pady=10)
            frame.pack(side="left")

            lbl_title = Label(frame, text=name, font=("Arial", 10, "bold"))
            lbl_title.pack(pady=(0, 5))

            lbl_img = Label(frame, image=tk_img)
            lbl_img.image = tk_img
            lbl_img.pack()

    # Hitung lebar window setelah semua gambar dimasukkan
    total_width = len(methods) * (img_width + padding)
    window_height = 320
    new_win.geometry(f"{total_width}x{window_height}")

    main_window.hide_progress()
    main_window.status_bar.config(text="All segmentations displayed")
