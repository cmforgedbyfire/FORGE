import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import pyautogui

from core.utils.helpers import set_status
from core.ui.modern_theme import create_card_frame, ModernTheme, add_tooltip
from modules.screenshots import logic


def build_ui(parent, status_var=None):
    """
    Build the enhanced UI for the Screenshot module.
    """
    main_frame = ttk.Frame(parent)
    main_frame.pack(fill="both", expand=True, padx=ModernTheme.PADDING_LG, pady=ModernTheme.PADDING_LG)

    # Output folder configuration
    folder_card, folder_content = create_card_frame(main_frame, "Output Folder")
    folder_card.pack(fill="x", pady=(0, ModernTheme.PADDING_LG))

    output_var = tk.StringVar(value=logic.get_default_output_dir())

    folder_frame = ttk.Frame(folder_content)
    folder_frame.pack(fill="x")

    entry = ttk.Entry(folder_frame, textvariable=output_var)
    entry.pack(side="left", fill="x", expand=True, padx=(0, ModernTheme.PADDING_MD))

    def choose_folder():
        folder = filedialog.askdirectory(initialdir=output_var.get())
        if folder:
            output_var.set(folder)
            set_status(status_var, f"Output folder: {os.path.basename(folder)}")
            update_thumbnail_view()

    browse_btn = ttk.Button(folder_frame, text="Browse", command=choose_folder)
    browse_btn.pack(side="right")
    add_tooltip(browse_btn, "Choose output folder for screenshots")

    # Capture modes
    capture_card, capture_content = create_card_frame(main_frame, "Capture Options")
    capture_card.pack(fill="x", pady=(0, ModernTheme.PADDING_LG))

    # ---------- Full Screen Capture (fixed for black screen) ----------

    def _capture_full_screen():
        try:
            output_dir = output_var.get()
            filename = logic.capture_full_screen(output_dir)
            set_status(status_var, f"Saved full screen: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture full screen:\n{e}")
            set_status(status_var, "Full screen capture failed.")
        finally:
            parent.winfo_toplevel().deiconify()

    def do_full_screen():
        parent.winfo_toplevel().withdraw()
        parent.after(300, _capture_full_screen)

    full_btn = ttk.Button(btn_frame, text="Full Screen", command=do_full_screen)
    full_btn.grid(row=0, column=0, padx=6, pady=6, sticky="ew")

    # ---------- Region Capture (fixed for black screen) ----------

    def _capture_region():
        try:
            tl_x, tl_y = pyautogui.position()
            messagebox.showinfo(
                "Region Capture",
                "Top-left recorded.\nMove to the BOTTOM-RIGHT corner and press OK."
            )
            br_x, br_y = pyautogui.position()

            left = min(tl_x, br_x)
            top = min(tl_y, br_y)
            width = abs(br_x - tl_x)
            height = abs(br_y - tl_y)

            output_dir = output_var.get()
            filename = logic.capture_region(output_dir, (left, top, width, height))
            set_status(status_var, f"Saved region: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture region:\n{e}")
            set_status(status_var, "Region capture failed.")
        finally:
            parent.winfo_toplevel().deiconify()

    def do_region():
        messagebox.showinfo(
            "Region Capture",
            "Step 1: Move your mouse to the TOP-LEFT corner and press OK.\n"
            "Step 2: Move to the BOTTOM-RIGHT corner and press OK again."
        )
        parent.winfo_toplevel().withdraw()
        parent.after(300, _capture_region)

    region_btn = ttk.Button(btn_frame, text="Select Region", command=do_region)
    region_btn.grid(row=0, column=1, padx=6, pady=6, sticky="ew")

    # ---------- Window-like Capture (fixed for black screen) ----------

    def _capture_window_click():
        try:
            x, y = pyautogui.position()
            output_dir = output_var.get()
            filename = logic.capture_centered_window_like(output_dir, x, y)
            set_status(status_var, f"Saved window area: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture window area:\n{e}")
            set_status(status_var, "Window capture failed.")
        finally:
            parent.winfo_toplevel().deiconify()

    def do_window_click():
        messagebox.showinfo(
            "Window Capture",
            "Move your mouse over the window you want to capture.\n"
            "Position the cursor, then press OK.\n\n"
            "A 1280x720 screenshot centered on the cursor will be saved."
        )
        parent.winfo_toplevel().withdraw()
        parent.after(300, _capture_window_click)

    window_btn = ttk.Button(
        btn_frame,
        text="Click Window (1280x720)",
        command=do_window_click
    )
    window_btn.grid(row=1, column=0, columnspan=2, padx=6, pady=6, sticky="ew")

    # Make buttons expand evenly
    btn_frame.columnconfigure(0, weight=1)
    btn_frame.columnconfigure(1, weight=1)

    # Info area (for future logs)
    info_frame = ttk.LabelFrame(frame, text="Info")
    info_frame.pack(fill="both", expand=True)

    info_label = ttk.Label(
        info_frame,
        text=(
            "This module helps you capture clean screenshots for marketing,\n"
            "documentation, and portfolio use.\n\n"
            "Future ideas:\n"
            "- Preset aspect ratios\n"
            "- Watermarks and branding frames\n"
            "- Automatic export to project asset folders"
        ),
        justify="left",
        anchor="nw"
    )
    info_label.pack(fill="both", expand=True, padx=8, pady=8)
