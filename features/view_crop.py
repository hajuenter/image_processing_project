import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

MAX_PREVIEW_WIDTH = 600
MAX_PREVIEW_HEIGHT = 400


def apply_crop(main_window):
    input_img = main_window.get_output_image()
    if input_img is None:
        input_img = main_window.get_input_image()

    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    # --- Baru buat window ---
    class CropWindow(tk.Toplevel):
        def __init__(self, main_window, input_img):
            super().__init__(main_window.root)
            self.title("Crop Image")
            self.main_window = main_window

            self.original_image = input_img.copy()

            # Tentukan ukuran preview tetap
            w, h = self.original_image.size
            scale = min(MAX_PREVIEW_WIDTH / w, MAX_PREVIEW_HEIGHT / h, 1.0)
            self.preview_size = (int(w * scale), int(h * scale))
            self.display_image = self.original_image.resize(
                self.preview_size, Image.Resampling.LANCZOS
            )

            self.tk_img = ImageTk.PhotoImage(self.display_image)
            self.canvas = tk.Canvas(
                self,
                width=self.tk_img.width(),
                height=self.tk_img.height(),
                cursor="cross",
            )
            self.canvas.pack()
            self.canvas_img = self.canvas.create_image(
                0, 0, anchor="nw", image=self.tk_img
            )

            self.crop_box = None  # (x1, y1, x2, y2)
            self.start_x = None
            self.start_y = None
            self.rect_id = None

            self.canvas.bind("<ButtonPress-1>", self.on_button_press)
            self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
            self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

            # Buttons
            btn_frame = tk.Frame(self)
            btn_frame.pack(fill="x", pady=5)
            tk.Button(btn_frame, text="Apply", width=10, command=self.apply_crop).pack(
                side="left", padx=5
            )
            tk.Button(btn_frame, text="Reset", width=10, command=self.reset_crop).pack(
                side="left", padx=5
            )
            tk.Button(btn_frame, text="Cancel", width=10, command=self.destroy).pack(
                side="left", padx=5
            )

        def on_button_press(self, event):
            self.start_x = event.x
            self.start_y = event.y
            if self.rect_id:
                self.canvas.delete(self.rect_id)
            self.rect_id = self.canvas.create_rectangle(
                self.start_x, self.start_y, self.start_x, self.start_y, outline="red"
            )

        def on_mouse_drag(self, event):
            self.canvas.coords(
                self.rect_id, self.start_x, self.start_y, event.x, event.y
            )

        def on_button_release(self, event):
            end_x, end_y = event.x, event.y
            x1 = max(min(self.start_x, end_x), 0)
            y1 = max(min(self.start_y, end_y), 0)
            x2 = min(max(self.start_x, end_x), self.display_image.width)
            y2 = min(max(self.start_y, end_y), self.display_image.height)

            if x2 - x1 > 0 and y2 - y1 > 0:
                self.crop_box = (x1, y1, x2, y2)
            else:
                self.crop_box = None

        def apply_crop(self):
            if self.crop_box:
                scale_x = self.original_image.width / self.display_image.width
                scale_y = self.original_image.height / self.display_image.height
                x1, y1, x2, y2 = self.crop_box
                crop_coords = (
                    int(x1 * scale_x),
                    int(y1 * scale_y),
                    int(x2 * scale_x),
                    int(y2 * scale_y),
                )
                cropped = self.original_image.crop(crop_coords)
                self.main_window.set_output_image(cropped)
                self.destroy()
            else:
                messagebox.showinfo("Crop", "No valid crop area selected")

        def reset_crop(self):
            self.main_window.set_output_image(self.original_image.copy())
            if self.rect_id:
                self.canvas.delete(self.rect_id)
            self.crop_box = None

    # Buat window crop
    CropWindow(main_window, input_img)
