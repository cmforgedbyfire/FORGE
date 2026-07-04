import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import pyautogui

from core.utils.helpers import set_status
from core.ui.modern_theme import create_card_frame, ModernTheme, add_tooltip
from core.utils.logging import get_logger
from modules.screenshots import logic

logger = get_logger(__name__)


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

    browse_btn = ttk.Button(folder_frame, text="Browse", command=choose_folder)
    browse_btn.pack(side="right")
    add_tooltip(browse_btn, "Choose output folder for screenshots")

    # Capture modes
    capture_card, capture_content = create_card_frame(main_frame, "Capture Options")
    capture_card.pack(fill="x", pady=(0, ModernTheme.PADDING_LG))

    buttons_frame = ttk.Frame(capture_content)
    buttons_frame.pack(fill="x")

    def capture_full():
        try:
            filename = logic.capture_full_screen(output_var.get())
            set_status(status_var, f"Captured: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Screenshot failed: {e}")

    def capture_region():
        messagebox.showinfo("Region Capture", "Click and drag to select region (ESC to cancel)")
        try:
            # Simple region capture - could be enhanced with overlay UI
            filename = logic.capture_full_screen(output_var.get())  # Fallback for now
            set_status(status_var, f"Captured: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Screenshot failed: {e}")

    def capture_window_area():
        messagebox.showinfo(
            "Window Capture",
            "Move your mouse over the window you want to capture, then press OK.\n\n"
            "FORGE will save a 1280x720 screenshot centered on the cursor."
        )
        try:
            x, y = pyautogui.position()
            filename = logic.capture_centered_window_like(output_var.get(), x, y)
            set_status(status_var, f"Captured: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Screenshot failed: {e}")

    full_btn = ttk.Button(buttons_frame, text="Full Screen (F11)", command=capture_full, style="Primary.TButton")
    full_btn.pack(side="left", padx=(0, ModernTheme.PADDING_MD))
    add_tooltip(full_btn, "Capture entire screen")

    region_btn = ttk.Button(buttons_frame, text="Region (F12)", command=capture_region)
    region_btn.pack(side="left")
    add_tooltip(region_btn, "Select region to capture")

    window_btn = ttk.Button(buttons_frame, text="Window Area", command=capture_window_area)
    window_btn.pack(side="left", padx=(ModernTheme.PADDING_MD, 0))
    add_tooltip(window_btn, "Capture a 1280x720 area centered on the mouse cursor")

    # Status and tips
    tips_card, tips_content = create_card_frame(main_frame, "Tips")
    tips_card.pack(fill="both", expand=True)

    tips_text = tk.Text(
        tips_content,
        height=6,
        wrap="word",
        font=ModernTheme.FONT_BODY,
        bg=ModernTheme.BG_SECONDARY,
        fg=ModernTheme.TEXT_PRIMARY,
        insertbackground=ModernTheme.TEXT_PRIMARY,
        selectbackground=ModernTheme.BG_PANEL_RAISED,
        selectforeground=ModernTheme.TEXT_PRIMARY,
        relief="solid",
        borderwidth=1,
        highlightthickness=1,
        highlightbackground=ModernTheme.BORDER_COLOR,
        highlightcolor=ModernTheme.BORDER_FOCUS,
        padx=ModernTheme.PADDING_MD,
        pady=ModernTheme.PADDING_MD
    )
    tips_text.pack(fill="both", expand=True)

    tips_content_text = """📸 Screenshot Tips:

• Use F11 for quick full-screen captures
• Move FORGE to another monitor before capturing for clean marketing shots
• Use Window Area for a quick 1280x720 app screenshot
• Screenshots are automatically organized by date
• Use region capture for specific UI elements

Recent captures will be saved to:
""" + output_var.get()

    tips_text.insert("1.0", tips_content_text)
    tips_text.config(state="disabled")

    # Hotkey bindings
    try:
        parent.winfo_toplevel().bind("<F11>", lambda e: capture_full())
        parent.winfo_toplevel().bind("<F12>", lambda e: capture_region())
    except Exception as e:
        logger.warning(f"Could not bind hotkeys: {e}")
