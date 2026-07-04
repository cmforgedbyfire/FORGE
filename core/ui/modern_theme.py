"""
Modern UI styling for FORGE with professional theming.
"""

import tkinter as tk
from tkinter import ttk


class ModernTheme:
    """Modern color scheme and styling constants."""
    
    # Brand colors
    PRIMARY = "#0066CC"
    PRIMARY_HOVER = "#0052A3"
    ACCENT = "#FF6B35"
    
    # Grays
    BG_PRIMARY = "#FFFFFF"
    BG_SECONDARY = "#F8F9FA"
    BG_PANEL = "#FFFFFF"
    
    BORDER_COLOR = "#DEE2E6"
    BORDER_FOCUS = "#0066CC"
    
    TEXT_PRIMARY = "#212529"
    TEXT_SECONDARY = "#6C757D"
    TEXT_MUTED = "#ADB5BD"
    
    # Status colors
    SUCCESS = "#28A745"
    WARNING = "#FFC107"
    ERROR = "#DC3545"
    INFO = "#17A2B8"
    
    # Spacing
    PADDING_SM = 4
    PADDING_MD = 8
    PADDING_LG = 12
    PADDING_XL = 16
    
    RADIUS = 6
    BORDER_WIDTH = 1


def configure_modern_style():
    """Configure modern ttk styling."""
    style = ttk.Style()
    
    # Use 'clam' theme as base for better customization
    try:
        style.theme_use('clam')
    except tk.TclError:
        style.theme_use('default')
    
    # Configure notebook (tabs)
    style.configure(
        "TNotebook",
        background=ModernTheme.BG_SECONDARY,
        borderwidth=0,
        tabposition="n"
    )
    
    style.configure(
        "TNotebook.Tab",
        background=ModernTheme.BG_SECONDARY,
        foreground=ModernTheme.TEXT_SECONDARY,
        padding=(ModernTheme.PADDING_LG, ModernTheme.PADDING_MD),
        borderwidth=1,
        focuscolor="none"
    )
    
    style.map(
        "TNotebook.Tab",
        background=[
            ("selected", ModernTheme.BG_PRIMARY),
            ("active", ModernTheme.BG_PANEL)
        ],
        foreground=[
            ("selected", ModernTheme.PRIMARY),
            ("active", ModernTheme.TEXT_PRIMARY)
        ],
        bordercolor=[
            ("selected", ModernTheme.BORDER_FOCUS),
            ("", ModernTheme.BORDER_COLOR)
        ]
    )
    
    # Configure frames
    style.configure(
        "TFrame",
        background=ModernTheme.BG_PRIMARY,
        relief="flat",
        borderwidth=0
    )
    
    style.configure(
        "Card.TFrame",
        background=ModernTheme.BG_PANEL,
        relief="solid",
        borderwidth=1
    )
    
    # Configure labels
    style.configure(
        "TLabel",
        background=ModernTheme.BG_PRIMARY,
        foreground=ModernTheme.TEXT_PRIMARY,
        font=('Segoe UI', 9)
    )
    
    style.configure(
        "Heading.TLabel",
        font=('Segoe UI', 11, 'bold'),
        foreground=ModernTheme.TEXT_PRIMARY
    )
    
    style.configure(
        "Muted.TLabel",
        foreground=ModernTheme.TEXT_MUTED,
        font=('Segoe UI', 8)
    )
    
    # Configure buttons
    style.configure(
        "TButton",
        background=ModernTheme.BG_PANEL,
        foreground=ModernTheme.TEXT_PRIMARY,
        borderwidth=1,
        relief="solid",
        padding=(ModernTheme.PADDING_LG, ModernTheme.PADDING_MD),
        font=('Segoe UI', 9)
    )
    
    style.map(
        "TButton",
        background=[
            ("active", ModernTheme.BG_SECONDARY),
            ("pressed", ModernTheme.BORDER_COLOR)
        ],
        bordercolor=[
            ("focus", ModernTheme.BORDER_FOCUS),
            ("", ModernTheme.BORDER_COLOR)
        ]
    )
    
    style.configure(
        "Primary.TButton",
        background=ModernTheme.PRIMARY,
        foreground="white",
        borderwidth=0,
        font=('Segoe UI', 9, 'bold')
    )
    
    style.map(
        "Primary.TButton",
        background=[
            ("active", ModernTheme.PRIMARY_HOVER),
            ("pressed", ModernTheme.PRIMARY_HOVER)
        ]
    )
    
    # Configure entries
    style.configure(
        "TEntry",
        borderwidth=1,
        relief="solid",
        padding=ModernTheme.PADDING_MD,
        font=('Segoe UI', 9)
    )
    
    style.map(
        "TEntry",
        bordercolor=[
            ("focus", ModernTheme.BORDER_FOCUS),
            ("", ModernTheme.BORDER_COLOR)
        ]
    )
    
    # Configure progressbar
    style.configure(
        "TProgressbar",
        background=ModernTheme.PRIMARY,
        troughcolor=ModernTheme.BG_SECONDARY,
        borderwidth=0,
        lightcolor=ModernTheme.PRIMARY,
        darkcolor=ModernTheme.PRIMARY
    )


def _bind_size_label(widget, label, prefix=""):
    """Keep a small live width x height label synced with a widget."""
    def update_size(event=None):
        width = widget.winfo_width()
        height = widget.winfo_height()
        if width > 1 and height > 1:
            label.configure(text=f"{prefix}{width} x {height}")

    widget.bind("<Configure>", update_size, add="+")
    widget.after_idle(update_size)


def create_card_frame(parent, title=None, show_size=True, **kwargs):
    """Create a modern card-style frame with optional title."""
    # Main card container
    card = ttk.Frame(parent, style="Card.TFrame", **kwargs)
    
    if title:
        # Header row
        header = ttk.Frame(card)
        header.pack(
            fill="x",
            padx=ModernTheme.PADDING_LG,
            pady=(ModernTheme.PADDING_LG, ModernTheme.PADDING_MD)
        )

        title_label = ttk.Label(
            header,
            text=title, 
            style="Heading.TLabel"
        )
        title_label.pack(side="left", anchor="w")

        if show_size:
            size_label = ttk.Label(header, text="", style="Muted.TLabel", anchor="e")
            size_label.pack(side="right", anchor="e")
            _bind_size_label(card, size_label)
        
        # Content frame
        content = ttk.Frame(card)
        content.pack(
            fill="both", 
            expand=True,
            padx=ModernTheme.PADDING_LG,
            pady=(0, ModernTheme.PADDING_LG)
        )
        return card, content
    else:
        return card


def add_tooltip(widget, text):
    """Add a simple tooltip to a widget."""
    def on_enter(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        
        label = tk.Label(
            tooltip,
            text=text,
            background="#FFFBF0",
            foreground=ModernTheme.TEXT_PRIMARY,
            relief="solid",
            borderwidth=1,
            font=('Segoe UI', 8),
            padx=ModernTheme.PADDING_MD,
            pady=ModernTheme.PADDING_SM
        )
        label.pack()
        
        widget.tooltip = tooltip
    
    def on_leave(event):
        if hasattr(widget, 'tooltip'):
            widget.tooltip.destroy()
            delattr(widget, 'tooltip')
    
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)
