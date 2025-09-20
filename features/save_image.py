from tkinter import filedialog, messagebox


def save_image(main_window):
    """
    Function to save the output image from MainWindow
    main_window: instance of MainWindow
    """
    if main_window.output_image is None:
        messagebox.showwarning("Warning", "No output image to save!")
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
    if not file_path:
        return

    try:
        main_window.output_image.save(file_path)
        messagebox.showinfo("Info", f"Image successfully saved to:\n{file_path}")
        main_window.status_bar.config(text=f"Saved: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image:\n{str(e)}")
