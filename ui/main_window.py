import tkinter as tk
from tkinter import ttk, Menu, filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import numpy as np

# Import the HistogramGenerator class
from features.histogram import HistogramGenerator


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
        self.output_image = None  # Add this for consistency

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
            command=self.open_image,
            image=self.icon_open if self.icon_open else None,
            compound="left",
            accelerator="Ctrl+O",
        )
        file_menu.add_command(
            label="Save",
            command=self.save_image,
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

        colors_menu = create_menu("Colors")
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
        self.root.bind("<Control-o>", lambda e: self.open_image())
        self.root.bind("<Control-s>", lambda e: self.save_image())

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

    def save_image(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "Tidak ada gambar untuk disimpan!")
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
        if file_path:
            try:
                self.current_image.save(file_path)
                messagebox.showinfo(
                    "Info", f"Gambar berhasil disimpan ke:\n{file_path}"
                )
                self.status_bar.config(text=f"Saved: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan gambar:\n{str(e)}")

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
                    lambda: self._resize_and_display_image(self.current_image, "right"),
                )

    def open_image(self):
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
        if file_path:
            try:
                img = Image.open(file_path)

                # Simpan gambar asli
                self.original_image = img.copy()
                self.current_image = img.copy()

                # Tampilkan gambar di input frame
                self._resize_and_display_image(self.current_image, "left")

                # Clear output frame (reset ke placeholder)
                self.output_image = None
                self.right_label.config(image="", text="Output Image")
                self.tk_img_right = None

                # Update status
                img_info = f"{img.size[0]}x{img.size[1]} - {img.mode}"
                self.status_bar.config(text=f"Opened: {file_path} | Size: {img_info}")

            except Exception as e:
                messagebox.showerror("Error", f"Gagal membuka gambar:\n{str(e)}")

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
