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
        # Validasi berdasarkan mode
        if mode == "input":
            if input_image is None:
                messagebox.showwarning(
                    "Warning", "Tidak ada gambar input untuk ditampilkan histogramnya!"
                )
                return
        elif mode == "output":
            if output_image is None:
                messagebox.showwarning(
                    "Warning", "Tidak ada gambar output untuk ditampilkan histogramnya!"
                )
                return
        elif mode == "both":
            if input_image is None:
                messagebox.showwarning(
                    "Warning", "Tidak ada gambar input untuk ditampilkan histogramnya!"
                )
                return
            if output_image is None:
                messagebox.showwarning(
                    "Warning", "Tidak ada gambar output untuk ditampilkan histogramnya!"
                )
                return

        # Buat window histogram
        self._create_histogram_window(mode, input_image, output_image)

    def _create_histogram_window(self, mode, input_image, output_image):
        """Buat window untuk menampilkan histogram"""
        hist_window = tk.Toplevel(self.parent)
        hist_window.title(f"Histogram - {mode.title()}")
        hist_window.configure(bg="white")
        hist_window.resizable(True, True)

        # Set ukuran window berdasarkan mode (lebih kecil karena tanpa teks)
        if mode == "both":
            hist_window.geometry("700x550")
        else:
            hist_window.geometry("400x450")

        # Buat figure matplotlib berdasarkan mode
        if mode == "input":
            fig = self._create_single_histogram(input_image)
        elif mode == "output":
            fig = self._create_single_histogram(output_image)
        elif mode == "both":
            fig = self._create_comparison_histogram(input_image, output_image)

        # Embed matplotlib dalam tkinter
        canvas = FigureCanvasTkAgg(fig, hist_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame untuk tombol
        button_frame = tk.Frame(hist_window, bg="white")
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        # Tombol Save dan Close
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
        """Buat histogram untuk satu gambar dengan subplot vertikal untuk R, G, B tanpa teks"""
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(5, 7))

        if image.mode == "RGB":
            # Pisahkan channel RGB
            r_channel = np.array(image.split()[0])
            g_channel = np.array(image.split()[1])
            b_channel = np.array(image.split()[2])

            # Plot histogram Red (paling atas)
            ax1.hist(
                r_channel.flatten(),
                bins=256,
                color="red",
                alpha=0.7,
                edgecolor="darkred",
            )
            ax1.set_xlim([0, 255])
            ax1.axis("off")

            # Plot histogram Green (tengah)
            ax2.hist(
                g_channel.flatten(),
                bins=256,
                color="green",
                alpha=0.7,
                edgecolor="darkgreen",
            )
            ax2.set_xlim([0, 255])
            ax2.axis("off")

            # Plot histogram Blue (paling bawah)
            ax3.hist(
                b_channel.flatten(),
                bins=256,
                color="blue",
                alpha=0.7,
                edgecolor="darkblue",
            )
            ax3.set_xlim([0, 255])
            ax3.axis("off")

        else:
            # Untuk grayscale
            gray_channel = np.array(image)

            # Red representation
            ax1.hist(gray_channel.flatten(), bins=256, color="red", alpha=0.7)
            ax1.set_xlim([0, 255])
            ax1.axis("off")

            # Green representation
            ax2.hist(gray_channel.flatten(), bins=256, color="green", alpha=0.7)
            ax2.set_xlim([0, 255])
            ax2.axis("off")

            # Blue representation
            ax3.hist(gray_channel.flatten(), bins=256, color="blue", alpha=0.7)
            ax3.set_xlim([0, 255])
            ax3.axis("off")

        plt.subplots_adjust(hspace=0.1)
        plt.tight_layout()
        return fig

    def _create_comparison_histogram(self, input_image, output_image):
        """Buat histogram perbandingan untuk input dan output tanpa teks"""
        fig, axes = plt.subplots(3, 2, figsize=(8, 9))

        # Column 1: Input histogram (vertikal)
        self._plot_rgb_channels_vertical(input_image, axes[:, 0])

        # Column 2: Output histogram (vertikal)
        self._plot_rgb_channels_vertical(output_image, axes[:, 1])

        plt.subplots_adjust(hspace=0.1, wspace=0.1)
        plt.tight_layout()
        return fig

    def _plot_rgb_channels_vertical(self, image, axes_column):
        """Plot RGB channels untuk satu kolom axes (vertikal) tanpa teks"""
        if image.mode == "RGB":
            # Pisahkan channel RGB
            channels = image.split()
            colors = ["red", "green", "blue"]

            for i, (channel, color) in enumerate(zip(channels, colors)):
                channel_data = np.array(channel)
                axes_column[i].hist(
                    channel_data.flatten(),
                    bins=256,
                    color=color,
                    alpha=0.7,
                    edgecolor=f"dark{color}",
                )
                axes_column[i].set_xlim([0, 255])
                axes_column[i].axis("off")
        else:
            # Untuk grayscale
            gray_channel = np.array(image)
            colors = ["red", "green", "blue"]

            for i, color in enumerate(colors):
                axes_column[i].hist(
                    gray_channel.flatten(), bins=256, color=color, alpha=0.7
                )
                axes_column[i].set_xlim([0, 255])
                axes_column[i].axis("off")

    def _save_histogram(self, fig):
        """Simpan histogram sebagai gambar"""
        from tkinter import filedialog

        file_path = filedialog.asksaveasfilename(
            title="Save Histogram",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("PDF files", "*.pdf"),
                ("SVG files", "*.svg"),
                ("All files", "*.*"),
            ],
        )

        if file_path:
            try:
                fig.savefig(
                    file_path,
                    dpi=300,
                    bbox_inches="tight",
                    facecolor="white",
                    edgecolor="none",
                )
                messagebox.showinfo(
                    "Success", f"Histogram saved successfully to:\n{file_path}"
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save histogram:\n{str(e)}")

    def _center_window(self, window):
        """Center window di layar"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
