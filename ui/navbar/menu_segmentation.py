from tkinter import Menu
from features.segmentation_global_thresholding import apply_global_thresholding
from features.segmentation_adaptive_thresholding import apply_adaptive_thresholding
from features.segmentation_kmeans import apply_kmeans
from features.segmentation_watershed import apply_watershed
from features.segmentation_region_growing import apply_region_growing
from features.segmentation_all import view_all_segmentations


def create_segmentation_menu(parent, main_window):
    """Membuat menu Segmentation"""
    segmentation_menu = Menu(parent, tearoff=0, relief="flat", bd=0)
    segmentation_menu.config(
        bg="white", fg="black", activebackground="#0078d4", activeforeground="white"
    )

    segmentation_menu.add_command(
        label="Global Thresholding",
        command=lambda: apply_global_thresholding(main_window),
    )

    segmentation_menu.add_command(
        label="Adaptive Thresholding",
        command=lambda: apply_adaptive_thresholding(main_window),
    )
    segmentation_menu.add_command(
        label="K-Means", command=lambda: apply_kmeans(main_window)
    )
    segmentation_menu.add_command(
        label="Watershed", command=lambda: apply_watershed(main_window)
    )
    segmentation_menu.add_command(
        label="Region Growing", command=lambda: apply_region_growing(main_window)
    )
    segmentation_menu.add_separator()
    segmentation_menu.add_command(
        label="View All Segmentations",
        command=lambda: view_all_segmentations(main_window),
    )

    return segmentation_menu
