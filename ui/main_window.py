import tkinter as tk
from tkinter import ttk, Menu, messagebox
from PIL import Image, ImageTk, ImageOps
import numpy as np

# Import the HistogramGenerator class
from features.histogram import HistogramGenerator
from features.open_image import open_image
from features.save_image import save_image


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

        # Menu Bar
        self._create_menu()

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

        # Status Bar dengan style yang lebih baik
        status_frame = tk.Frame(self.root, relief="sunken", bd=1)
        status_frame.grid(row=1, column=0, columnspan=2, sticky="we")

        self.status_bar = tk.Label(
            status_frame,
            text="Ready | No image loaded",
            anchor="w",
            padx=5,
            pady=2,
            bg="#e0e0e0",
        )
        self.status_bar.pack(fill="x")

        # Simpan referensi gambar
        self.tk_img_left = None
        self.tk_img_right = None
        self.current_image = None
        self.original_image = None
        self.output_image = None

        # Bind event untuk resize window
        self.root.bind("<Configure>", self._on_window_resize)

    def _create_menu(self):
        menubar = Menu(self.root, relief="flat", borderwidth=0)

        # Konfigurasi untuk mengurangi bayangan dan blur
        menubar.config(
            bg="#f8f8f8",
            fg="black",
            activebackground="#e0e0e0",
            activeforeground="black",
            relief="flat",
            bd=0,
        )

        def load_icon(path, size=(16, 16)):
            try:
                img = Image.open(path).convert("RGBA")
                img = img.resize(size, Image.LANCZOS)

                # Background putih solid
                bg_img = Image.new("RGBA", size, (255, 255, 255, 255))
                bg_img.paste(img, (0, 0), img)
                bg_img = bg_img.convert("RGB")

                return ImageTk.PhotoImage(bg_img)
            except Exception as e:
                print(f"Icon loading error: {e}")
                return None

        # Load icons
        self.icon_open = (
            load_icon("icons/open.png") if self._file_exists("icons/open.png") else None
        )
        self.icon_save = (
            load_icon("icons/save.png") if self._file_exists("icons/save.png") else None
        )
        self.icon_exit = (
            load_icon("icons/exit.png") if self._file_exists("icons/exit.png") else None
        )
        self.icon_histogram = (
            load_icon("icons/histogram.png")
            if self._file_exists("icons/histogram.png")
            else None
        )

        # File Menu
        file_menu = Menu(menubar, tearoff=0, relief="flat", bd=0)
        file_menu.config(
            bg="white",
            fg="black",
            activebackground="#0078d4",
            activeforeground="white",
            selectcolor="#0078d4",
        )

        file_menu.add_command(
            label="Open",
            command=self.open_image_wrapper,
            image=self.icon_open if self.icon_open else None,
            compound="left",
            accelerator="Ctrl+O",
        )
        file_menu.add_command(
            label="Save",
            command=self.save_image_wrapper,
            image=self.icon_save if self.icon_save else None,
            compound="left",
            accelerator="Ctrl+S",
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Exit",
            command=self.root.quit,
            image=self.icon_exit if self.icon_exit else None,
            compound="left",
            accelerator="Alt+F4",
        )
        menubar.add_cascade(label="File", menu=file_menu)

        # View Menu dengan submenu Histogram
        view_menu = Menu(menubar, tearoff=0, relief="flat", bd=0)
        view_menu.config(
            bg="white", fg="black", activebackground="#0078d4", activeforeground="white"
        )

        # Submenu Histogram - Now using HistogramGenerator
        histogram_menu = Menu(view_menu, tearoff=0, relief="flat", bd=0)
        histogram_menu.config(
            bg="white", fg="black", activebackground="#0078d4", activeforeground="white"
        )

        histogram_menu.add_command(
            label="Input", command=lambda: self.show_histogram("input")
        )
        histogram_menu.add_command(
            label="Output", command=lambda: self.show_histogram("output")
        )
        histogram_menu.add_command(
            label="Input dan Output", command=lambda: self.show_histogram("both")
        )

        view_menu.add_cascade(
            label="Histogram",
            menu=histogram_menu,
            image=self.icon_histogram if self.icon_histogram else None,
            compound="left",
        )
        menubar.add_cascade(label="View", menu=view_menu)

        # Menu lainnya dengan style konsisten
        def create_menu(label, commands=None):
            menu = Menu(menubar, tearoff=0, relief="flat", bd=0)
            menu.config(
                bg="white",
                fg="black",
                activebackground="#0078d4",
                activeforeground="white",
            )
            if commands:
                for cmd_label, cmd_func in commands:
                    menu.add_command(label=cmd_label, command=cmd_func)
            return menu

        # Colors Menu
        colors_menu = Menu(menubar, tearoff=0, relief="flat", bd=0)
        colors_menu.config(
            bg="white",
            fg="black",
            activebackground="#0078d4",
            activeforeground="white",
        )

        # Submenu RGB
        rgb_menu = Menu(colors_menu, tearoff=0, relief="flat", bd=0)
        rgb_menu.config(
            bg="white", fg="black", activebackground="#0078d4", activeforeground="white"
        )
        for color in ["Yellow", "Orange", "Cyan", "Purple", "Grey", "Brown", "Red"]:
            rgb_menu.add_command(
                label=color, command=lambda c=color: print(f"RGB -> {c}")
            )
        colors_menu.add_cascade(label="RGB", menu=rgb_menu)

        # Submenu RGB to Grayscale
        grayscale_menu = Menu(colors_menu, tearoff=0, relief="flat", bd=0)
        grayscale_menu.config(
            bg="white", fg="black", activebackground="#0078d4", activeforeground="white"
        )
        for method in ["Average", "Lightness", "Luminance"]:
            grayscale_menu.add_command(
                label=method, command=lambda m=method: print(f"Grayscale -> {m}")
            )
        colors_menu.add_cascade(label="RGB to Grayscale", menu=grayscale_menu)

        # Submenu Brightness
        brightness_menu = Menu(colors_menu, tearoff=0, relief="flat", bd=0)
        brightness_menu.config(
            bg="white", fg="black", activebackground="#0078d4", activeforeground="white"
        )
        brightness_menu.add_command(
            label="Contrast", command=lambda: print("Brightness -> Contrast")
        )
        colors_menu.add_cascade(label="Brightness", menu=brightness_menu)

        # Brightness - Contrast (langsung item biasa)
        colors_menu.add_command(
            label="Brightness - Contrast",
            command=lambda: print("Brightness - Contrast"),
        )

        # Invert
        colors_menu.add_command(label="Invert", command=lambda: print("Invert"))

        # Log Brightness
        colors_menu.add_command(
            label="Log Brightness", command=lambda: print("Log Brightness")
        )

        # Submenu Bit Depth
        bitdepth_menu = Menu(colors_menu, tearoff=0, relief="flat", bd=0)
        bitdepth_menu.config(
            bg="white", fg="black", activebackground="#0078d4", activeforeground="white"
        )
        for i in range(1, 8):
            bitdepth_menu.add_command(
                label=f"{i} bit", command=lambda b=i: print(f"Bit Depth -> {b} bit")
            )
        colors_menu.add_cascade(label="Bit Depth", menu=bitdepth_menu)

        # Gamma Correction
        colors_menu.add_command(
            label="Gamma Correction", command=lambda: print("Gamma Correction")
        )

        # Tambahkan ke menubar
        menubar.add_cascade(label="Colors", menu=colors_menu)

        # Menu Tentang sebagai command, bukan cascade
        menubar.add_command(
            label="Tentang",
            command=lambda: messagebox.showinfo(
                "Tentang", "Aplikasi GUI Python\nVersion 1.0"
            ),
        )

        processing_menu = create_menu("Image Processing")
        menubar.add_cascade(label="Image Processing", menu=processing_menu)

        arithmetic_menu = create_menu("Arithmetical Operation")
        menubar.add_cascade(label="Arithmetical Operation", menu=arithmetic_menu)

        filter_menu = create_menu("Filter")
        menubar.add_cascade(label="Filter", menu=filter_menu)

        edge_menu = create_menu("Edge Detection")
        menubar.add_cascade(label="Edge Detection", menu=edge_menu)

        morfologi_menu = create_menu("Morfologi")
        menubar.add_cascade(label="Morfologi", menu=morfologi_menu)

        self.root.config(menu=menubar)

        # Bind keyboard shortcuts
        self.root.bind("<Control-o>", lambda e: self.open_image_wrapper())
        self.root.bind("<Control-s>", lambda e: self.save_image_wrapper())

    def _file_exists(self, path):
        import os

        return os.path.exists(path)

    def show_histogram(self, mode):
        """
        Tampilkan histogram menggunakan HistogramGenerator
        Ini menggantikan implementasi histogram yang lama
        """
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

        # Update status
        self.status_bar.config(text="Image processed successfully")

    def get_input_image(self):
        """Method untuk mendapatkan gambar input untuk processing"""
        return self.original_image

    def get_output_image(self):
        """Method untuk mendapatkan gambar output"""
        return self.output_image

    def run(self):
        self.root.mainloop()
