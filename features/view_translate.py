import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import ImageChops


class TranslateDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="tx (geser horizontal):").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        tk.Label(master, text="ty (geser vertical):").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )

        self.tx_var = tk.IntVar(value=50)
        self.ty_var = tk.IntVar(value=50)

        self.tx_entry = tk.Entry(master, textvariable=self.tx_var)
        self.ty_entry = tk.Entry(master, textvariable=self.ty_var)

        self.tx_entry.grid(row=0, column=1, padx=5, pady=5)
        self.ty_entry.grid(row=1, column=1, padx=5, pady=5)

        return self.tx_entry  # fokus awal

    def buttonbox(self):
        box = tk.Frame(self)

        apply_btn = tk.Button(
            box, text="Apply", width=10, command=self.ok, default=tk.ACTIVE
        )
        apply_btn.pack(side="left", padx=5, pady=5)

        reset_btn = tk.Button(box, text="Reset", width=10, command=self.reset_image)
        reset_btn.pack(side="left", padx=5, pady=5)

        cancel_btn = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_btn.pack(side="left", padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def reset_image(self):
        self.result = "reset"
        self.destroy()

    def apply(self):
        # hanya dipanggil saat klik Apply
        self.result = (self.tx_var.get(), self.ty_var.get())


def apply_translate(main_window):
    """Tampilkan dialog translate dan geser gambar"""
    input_img = main_window.get_output_image() or main_window.get_input_image()
    if input_img is None:
        messagebox.showwarning("No Image", "Please open an image first!")
        main_window.status_bar.config(text="No image loaded")
        return

    dialog = TranslateDialog(main_window.root, title="Translate Image")
    if not dialog.result:
        return  # Cancel ditekan

    if dialog.result == "reset":
        # Kembalikan gambar ke original
        main_window.set_output_image(main_window.original_image.copy())
        main_window.status_bar.config(text="Image reset to original")
        return

    tx, ty = dialog.result
    main_window.show_progress(f"Translating (tx={tx}, ty={ty})...")
    main_window.root.update()

    translated = ImageChops.offset(input_img, tx, ty)

    main_window.set_output_image(translated)
    main_window.hide_progress()
