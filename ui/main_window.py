import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
import numpy as np

from features.histogram import HistogramGenerator
from features.open_image import open_image
from features.save_image import save_image
from ui.menu.menu_bar import MenuBar


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Form1")
        self.root.geometry("900x500")

        # Set style untuk tampilan yang lebih modern
        style = ttk.Style()
        style.theme_use("clam")

        # Atur grid root supaya responsif
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        # Initialize HistogramGenerator
        self.histogram_generator = HistogramGenerator(self.root)

        # Initialize MenuBar
        self.menu_bar = MenuBar(self)

        # Frame kiri (gambar 1)
        self.left_frame = tk.Frame(self.root, bd=2, relief="groove", bg="#f0f0f0")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.left_frame.rowconfigure(0, weight=1)
        self.left_frame.columnconfigure(0, weight=1)
        self.left_frame.grid_propagate(False)

        self.left_label = tk.Label(
            self.left_frame,
            bg="white",
            text="Input Image",
            font=("Arial", 10),
            fg="gray",
        )
        self.left_label.grid(row=0, column=0, sticky="nsew")

        # Frame kanan (gambar 2)
        self.right_frame = tk.Frame(self.root, bd=2, relief="groove", bg="#f0f0f0")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.right_frame.rowconfigure(0, weight=1)
        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.grid_propagate(False)

        self.right_label = tk.Label(
            self.right_frame,
            bg="white",
            text="Output Image",
            font=("Arial", 10),
            fg="gray",
        )
        self.right_label.grid(row=0, column=0, sticky="nsew")

        # Status Bar dengan style yang lebih baik dan layout horizontal
        status_frame = tk.Frame(self.root, relief="sunken", bd=1, bg="#e0e0e0")
        status_frame.grid(row=1, column=0, columnspan=2, sticky="we")

        # Frame untuk status text dan progress bar dalam satu baris
        content_frame = tk.Frame(status_frame, bg="#e0e0e0")
        content_frame.pack(fill="x", padx=5, pady=2)

        self.status_bar = tk.Label(
            content_frame,
            text="Ready | No image loaded",
            anchor="w",
            bg="#e0e0e0",
            fg="black",
        )
        self.status_bar.pack(side="left", fill="x", expand=True)

        # Progress bar dengan style hijau dan ukuran yang lebih kecil
        style.configure(
            "Green.Horizontal.TProgressbar",
            foreground="green",
            background="green",
            lightcolor="lightgreen",
            darkcolor="darkgreen",
            bordercolor="gray",
            focuscolor="green",
        )

        self.progress = ttk.Progressbar(
            content_frame,
            mode="indeterminate",
            length=200,
            style="Green.Horizontal.TProgressbar",
        )
        # Progress bar tidak ditampilkan secara default

        # Simpan referensi gambar
        self.tk_img_left = None
        self.tk_img_right = None
        self.current_image = None
        self.original_image = None
        self.output_image = None

        # Bind event untuk resize window
        self.root.bind("<Configure>", self._on_window_resize)

    def show_progress(self, message="Processing..."):
        """Tampilkan loading bar dengan pesan"""
        self.status_bar.config(text=message)
        self.progress.pack(side="right", padx=(10, 0))
        self.progress.start(10)  # Animasi indeterminate
        self.root.update_idletasks()

    def hide_progress(self):
        """Sembunyikan loading bar dan reset status"""
        self.progress.stop()
        self.progress.pack_forget()

    def show_histogram(self, mode):
        # Delegate ke HistogramGenerator dengan parameter yang sesuai
        self.histogram_generator.show_histogram(
            mode=mode, input_image=self.original_image, output_image=self.output_image
        )

    def open_image_wrapper(self):
        """
        Wrapper untuk fungsi open_image dari features.open_image
        """
        # Panggil fungsi open_image dari features dengan passing self sebagai main_window
        open_image(self)

    def save_image_wrapper(self):
        """
        Wrapper untuk fungsi save_image dari features.save_image
        """
        # Panggil fungsi save_image dari features dengan passing self sebagai main_window
        save_image(self)

    def _get_frame_size(self):
        """Mendapatkan ukuran frame yang sebenarnya"""
        self.root.update_idletasks()

        frame_w = self.left_frame.winfo_width()
        frame_h = self.left_frame.winfo_height()

        if frame_w <= 1 or frame_h <= 1:
            window_w = self.root.winfo_width()
            window_h = self.root.winfo_height()
            frame_w = (window_w - 20) // 2
            frame_h = window_h - 80  # Lebih banyak ruang untuk status bar

        return max(frame_w, 100), max(frame_h, 100)

    def _resize_and_display_image(self, img, side="left"):
        """Resize dan tampilkan gambar dengan mempertahankan aspect ratio"""
        frame_w, frame_h = self._get_frame_size()

        # Resize dengan aspect ratio
        img_resized = ImageOps.contain(img, (frame_w - 10, frame_h - 10))
        final_img = Image.new("RGB", (frame_w - 10, frame_h - 10), "white")
        final_img.paste(
            img_resized,
            (
                (frame_w - 10 - img_resized.width) // 2,
                (frame_h - 10 - img_resized.height) // 2,
            ),
        )

        if side == "left":
            self.tk_img_left = ImageTk.PhotoImage(final_img)
            self.left_label.config(image=self.tk_img_left, text="")
            self.left_label.image = self.tk_img_left
        else:
            self.tk_img_right = ImageTk.PhotoImage(final_img)
            self.right_label.config(image=self.tk_img_right, text="")
            self.right_label.image = self.tk_img_right

    def _on_window_resize(self, event):
        """Event handler ketika window diresize"""
        if event.widget == self.root:
            if self.current_image:
                self.root.after(
                    100,
                    lambda: self._resize_and_display_image(self.current_image, "left"),
                )
            if self.tk_img_right:
                self.root.after(
                    100,
                    lambda: self._resize_and_display_image(
                        self.output_image if self.output_image else self.current_image,
                        "right",
                    ),
                )

    def set_output_image(self, processed_image):
        """
        Method untuk set gambar output dari operasi image processing
        Ini akan dipanggil oleh feature lain yang memproses gambar
        """
        self.output_image = processed_image.copy()
        self._resize_and_display_image(self.output_image, "right")

        # Update status tanpa menampilkan pesan sukses yang berlebihan
        img_info = f"{processed_image.size[0]}x{processed_image.size[1]} - {processed_image.mode}"
        self.status_bar.config(text=f"Image processed | Size: {img_info}")

    def get_input_image(self):
        """Method untuk mendapatkan gambar input untuk processing"""
        return self.original_image

    def get_output_image(self):
        """Method untuk mendapatkan gambar output"""
        return self.output_image

    def run(self):
        self.root.mainloop()
