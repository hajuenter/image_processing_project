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

        # Center window
        hist_window.transient(self.parent)
        hist_window.grab_set()
        self._center_window(hist_window)

    def _create_single_histogram(self, image):
        """Buat histogram untuk gambar RGB atau Grayscale"""
        if image.mode == "RGB":
            fig, axes = plt.subplots(3, 1, figsize=(5, 7))
            channels = image.split()
            colors = ["red", "green", "blue"]
            titles = ["Red Channel", "Green Channel", "Blue Channel"]

            for ax, channel, color, title in zip(axes, channels, colors, titles):
                data = np.array(channel).flatten()
                ax.hist(data, bins=256, color=color, alpha=0.7, edgecolor=color)
                ax.set_xlim([0, 255])
                ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
                ax.set_facecolor("white")
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_title(title, fontsize=10)

        elif image.mode == "L":  # Grayscale
            fig, ax = plt.subplots(figsize=(5, 3))
            data = np.array(image).flatten()
            ax.hist(data, bins=256, color="black", alpha=0.7, edgecolor="black")
            ax.set_xlim([0, 255])
            ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
            ax.set_facecolor("white")
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title("Grayscale Histogram", fontsize=12)

        else:
            # fallback untuk mode lain (RGBA, CMYK, dsb)
            fig, ax = plt.subplots(figsize=(5, 3))
            data = np.array(image.convert("L")).flatten()
            ax.hist(data, bins=256, color="gray", alpha=0.7, edgecolor="black")
            ax.set_xlim([0, 255])
            ax.set_title(f"Histogram ({image.mode})", fontsize=12)

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
