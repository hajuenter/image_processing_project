import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class HistogramGenerator:
    def __init__(self, parent):
        self.parent = parent

    def show_histogram(self, mode, input_image=None, output_image=None):
        """
        Tampilkan histogram berdasarkan mode yang dipilih

        Args:
            mode (str): 'input', 'output', atau 'both'
            input_image (PIL.Image): Gambar input
            output_image (PIL.Image): Gambar output
        """
        if mode == "input":
            if input_image is None:
                messagebox.showwarning("Warning", "Tidak ada gambar input!")
                return
            self._create_histogram_window("Input", input_image)

        elif mode == "output":
            if output_image is None:
                messagebox.showwarning("Warning", "Tidak ada gambar output!")
                return
            self._create_histogram_window("Output", output_image)

        elif mode == "both":
            if input_image is None or output_image is None:
                messagebox.showwarning("Warning", "Input/Output tidak tersedia!")
                return
            # Buka 2 window terpisah
            self._create_histogram_window("Input", input_image)
            self._create_histogram_window("Output", output_image)

    def _create_histogram_window(self, label, image):
        """Buat window untuk menampilkan histogram"""
        hist_window = tk.Toplevel(self.parent)
        hist_window.title(f"Histogram - {label}")
        hist_window.configure(bg="white")
        hist_window.geometry("400x450")
        hist_window.resizable(True, True)

        # Buat figure matplotlib
        fig = self._create_single_histogram(image)

        # Embed matplotlib dalam tkinter
        canvas = FigureCanvasTkAgg(fig, hist_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame tombol
        button_frame = tk.Frame(hist_window, bg="white")
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        save_btn = ttk.Button(
            button_frame,
            text="Save Histogram",
            command=lambda: self._save_histogram(fig),
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 10))

        close_btn = ttk.Button(button_frame, text="Close", command=hist_window.destroy)
        close_btn.pack(side=tk.RIGHT)

        # Center window
        hist_window.transient(self.parent)
        hist_window.grab_set()
        self._center_window(hist_window)

    def _create_single_histogram(self, image):
        """Buat histogram untuk satu gambar dengan subplot vertikal untuk R, G, B"""
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(5, 7))

        if image.mode == "RGB":
            channels = image.split()
            colors = ["red", "green", "blue"]
        else:
            # grayscale → gunakan 3 channel dengan warna berbeda
            channels = [image, image, image]
            colors = ["red", "green", "blue"]

        for ax, channel, color in zip((ax1, ax2, ax3), channels, colors):
            data = np.array(channel).flatten()
            ax.hist(data, bins=256, color=color, alpha=0.7, edgecolor=color)
            ax.set_xlim([0, 255])

            # Tambahkan grid kotak-kotak
            ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
            ax.set_facecolor("white")

            # Hilangkan angka sumbu
            ax.set_xticks([])
            ax.set_yticks([])

        plt.subplots_adjust(hspace=0.1)
        plt.tight_layout()
        return fig

    def _center_window(self, window):
        """Center window di layar"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
