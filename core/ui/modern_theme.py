"""
Brand UI styling for FORGE.
"""

import tkinter as tk
from tkinter import ttk


class ModernTheme:
    """Forged by Fire color, typography, and spacing constants."""

    # Brand colors shared with the website and Master Generator.
    BG_PRIMARY = "#0f0e0c"
    BG_SECONDARY = "#151411"
    BG_PANEL = "#1b1914"
    BG_PANEL_ALT = "#242018"
    BG_PANEL_RAISED = "#2b261d"

    TEXT_PRIMARY = "#f4f1ea"
    TEXT_SECONDARY = "#c1b8ab"
    TEXT_MUTED = "#8f877b"

    BORDER_COLOR = "#2f2a21"
    BORDER_FOCUS = "#ff7a18"

    PRIMARY = "#ff7a18"
    PRIMARY_HOVER = "#d94a1a"
    ACCENT = "#d1a35a"
    TEAL = "#3aa7c5"
    STEEL = "#aeb8bf"

    SUCCESS = "#4faa6b"
    WARNING = "#d1a35a"
    ERROR = "#dc4a34"
    INFO = "#3aa7c5"

    FONT_BODY = ("Trebuchet MS", 9)
    FONT_BODY_BOLD = ("Trebuchet MS", 9, "bold")
    FONT_HEADING = ("Georgia", 12, "bold")
    FONT_SMALL = ("Trebuchet MS", 8)

    PADDING_SM = 4
    PADDING_MD = 8
    PADDING_LG = 12
    PADDING_XL = 16

    RADIUS = 6
    BORDER_WIDTH = 1


def configure_modern_style():
    """Configure ttk styling to match the Forged by Fire brand."""
    style = ttk.Style()

    try:
        style.theme_use("clam")
    except tk.TclError:
        style.theme_use("default")

    style.configure(
        ".",
        background=ModernTheme.BG_PRIMARY,
        foreground=ModernTheme.TEXT_PRIMARY,
        fieldbackground=ModernTheme.BG_PANEL,
        font=ModernTheme.FONT_BODY,
        bordercolor=ModernTheme.BORDER_COLOR,
        lightcolor=ModernTheme.BORDER_COLOR,
        darkcolor=ModernTheme.BORDER_COLOR,
        troughcolor=ModernTheme.BG_SECONDARY,
        focuscolor="none",
    )

    style.configure(
        "TNotebook",
        background=ModernTheme.BG_SECONDARY,
        borderwidth=0,
        tabmargins=(12, 8, 12, 0),
        tabposition="n",
    )
    style.configure(
        "TNotebook.Tab",
        background=ModernTheme.BG_PANEL,
        foreground=ModernTheme.TEXT_SECONDARY,
        padding=(ModernTheme.PADDING_XL, ModernTheme.PADDING_MD),
        borderwidth=1,
        font=ModernTheme.FONT_BODY_BOLD,
    )
    style.map(
        "TNotebook.Tab",
        background=[
            ("selected", ModernTheme.BG_PRIMARY),
            ("active", ModernTheme.BG_PANEL_ALT),
        ],
        foreground=[
            ("selected", ModernTheme.ACCENT),
            ("active", ModernTheme.TEXT_PRIMARY),
        ],
        bordercolor=[
            ("selected", ModernTheme.PRIMARY),
            ("active", ModernTheme.ACCENT),
            ("", ModernTheme.BORDER_COLOR),
        ],
    )

    style.configure("TFrame", background=ModernTheme.BG_PANEL, relief="flat", borderwidth=0)
    style.configure("Surface.TFrame", background=ModernTheme.BG_SECONDARY, relief="flat", borderwidth=0)
    style.configure(
        "Card.TFrame",
        background=ModernTheme.BG_PANEL,
        relief="solid",
        borderwidth=1,
        bordercolor=ModernTheme.BORDER_COLOR,
    )
    style.configure(
        "Status.TFrame",
        background=ModernTheme.BG_SECONDARY,
        relief="solid",
        borderwidth=1,
        bordercolor=ModernTheme.BORDER_COLOR,
    )

    style.configure(
        "TLabel",
        background=ModernTheme.BG_PANEL,
        foreground=ModernTheme.TEXT_PRIMARY,
        font=ModernTheme.FONT_BODY,
    )
    style.configure(
        "Card.TLabel",
        background=ModernTheme.BG_PANEL,
        foreground=ModernTheme.TEXT_PRIMARY,
        font=ModernTheme.FONT_BODY,
    )
    style.configure(
        "Heading.TLabel",
        background=ModernTheme.BG_PANEL,
        foreground=ModernTheme.TEXT_PRIMARY,
        font=ModernTheme.FONT_HEADING,
    )
    style.configure(
        "CardHeading.TLabel",
        background=ModernTheme.BG_PANEL,
        foreground=ModernTheme.TEXT_PRIMARY,
        font=ModernTheme.FONT_HEADING,
    )
    style.configure(
        "Muted.TLabel",
        background=ModernTheme.BG_PANEL,
        foreground=ModernTheme.TEXT_MUTED,
        font=ModernTheme.FONT_SMALL,
    )
    style.configure(
        "CardMuted.TLabel",
        background=ModernTheme.BG_PANEL,
        foreground=ModernTheme.TEXT_MUTED,
        font=ModernTheme.FONT_SMALL,
    )
    style.configure(
        "Status.TLabel",
        background=ModernTheme.BG_SECONDARY,
        foreground=ModernTheme.TEXT_SECONDARY,
        font=ModernTheme.FONT_SMALL,
    )

    style.configure(
        "TLabelframe",
        background=ModernTheme.BG_PANEL,
        foreground=ModernTheme.TEXT_PRIMARY,
        bordercolor=ModernTheme.BORDER_COLOR,
        relief="solid",
        borderwidth=1,
    )
    style.configure(
        "TLabelframe.Label",
        background=ModernTheme.BG_PANEL,
        foreground=ModernTheme.ACCENT,
        font=ModernTheme.FONT_BODY_BOLD,
    )

    style.configure(
        "TButton",
        background=ModernTheme.BG_PANEL_ALT,
        foreground=ModernTheme.TEXT_PRIMARY,
        borderwidth=1,
        relief="solid",
        bordercolor=ModernTheme.BORDER_COLOR,
        padding=(ModernTheme.PADDING_LG, ModernTheme.PADDING_MD),
        font=ModernTheme.FONT_BODY_BOLD,
    )
    style.map(
        "TButton",
        background=[
            ("active", ModernTheme.BG_PANEL_RAISED),
            ("pressed", ModernTheme.BG_SECONDARY),
            ("disabled", ModernTheme.BG_PANEL),
        ],
        foreground=[
            ("disabled", ModernTheme.TEXT_MUTED),
            ("", ModernTheme.TEXT_PRIMARY),
        ],
        bordercolor=[
            ("focus", ModernTheme.BORDER_FOCUS),
            ("active", ModernTheme.ACCENT),
            ("", ModernTheme.BORDER_COLOR),
        ],
    )
    style.configure(
        "Primary.TButton",
        background=ModernTheme.PRIMARY,
        foreground="#1a130c",
        borderwidth=0,
        font=ModernTheme.FONT_BODY_BOLD,
    )
    style.map(
        "Primary.TButton",
        background=[
            ("active", ModernTheme.ACCENT),
            ("pressed", ModernTheme.PRIMARY_HOVER),
            ("disabled", ModernTheme.BG_PANEL_ALT),
        ],
        foreground=[
            ("disabled", ModernTheme.TEXT_MUTED),
            ("", "#1a130c"),
        ],
    )

    style.configure(
        "TEntry",
        fieldbackground=ModernTheme.BG_PANEL,
        background=ModernTheme.BG_PANEL,
        foreground=ModernTheme.TEXT_PRIMARY,
        insertcolor=ModernTheme.TEXT_PRIMARY,
        borderwidth=1,
        relief="solid",
        padding=ModernTheme.PADDING_MD,
        font=ModernTheme.FONT_BODY,
    )
    style.map(
        "TEntry",
        bordercolor=[
            ("focus", ModernTheme.BORDER_FOCUS),
            ("", ModernTheme.BORDER_COLOR),
        ],
    )

    style.configure(
        "TCombobox",
        fieldbackground=ModernTheme.BG_PANEL,
        background=ModernTheme.BG_PANEL_ALT,
        foreground=ModernTheme.TEXT_PRIMARY,
        arrowcolor=ModernTheme.ACCENT,
        bordercolor=ModernTheme.BORDER_COLOR,
        padding=ModernTheme.PADDING_MD,
        font=ModernTheme.FONT_BODY,
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", ModernTheme.BG_PANEL), ("", ModernTheme.BG_PANEL)],
        foreground=[("readonly", ModernTheme.TEXT_PRIMARY), ("", ModernTheme.TEXT_PRIMARY)],
        bordercolor=[("focus", ModernTheme.BORDER_FOCUS), ("", ModernTheme.BORDER_COLOR)],
    )

    style.configure(
        "TRadiobutton",
        background=ModernTheme.BG_PANEL,
        foreground=ModernTheme.TEXT_PRIMARY,
        indicatorcolor=ModernTheme.BG_PANEL,
        font=ModernTheme.FONT_BODY,
    )
    style.configure(
        "TCheckbutton",
        background=ModernTheme.BG_PANEL,
        foreground=ModernTheme.TEXT_PRIMARY,
        indicatorcolor=ModernTheme.BG_PANEL,
        font=ModernTheme.FONT_BODY,
    )
    style.map(
        "TRadiobutton",
        foreground=[("active", ModernTheme.ACCENT), ("", ModernTheme.TEXT_PRIMARY)],
        indicatorcolor=[("selected", ModernTheme.PRIMARY), ("", ModernTheme.BG_PANEL)],
    )
    style.map(
        "TCheckbutton",
        foreground=[("active", ModernTheme.ACCENT), ("", ModernTheme.TEXT_PRIMARY)],
        indicatorcolor=[("selected", ModernTheme.PRIMARY), ("", ModernTheme.BG_PANEL)],
    )

    style.configure(
        "Treeview",
        background=ModernTheme.BG_PANEL,
        fieldbackground=ModernTheme.BG_PANEL,
        foreground=ModernTheme.TEXT_PRIMARY,
        bordercolor=ModernTheme.BORDER_COLOR,
        rowheight=26,
        font=ModernTheme.FONT_BODY,
    )
    style.configure(
        "Treeview.Heading",
        background=ModernTheme.BG_PANEL_ALT,
        foreground=ModernTheme.TEXT_PRIMARY,
        relief="flat",
        bordercolor=ModernTheme.BORDER_COLOR,
        font=ModernTheme.FONT_BODY_BOLD,
    )
    style.map(
        "Treeview",
        background=[("selected", ModernTheme.BG_PANEL_RAISED)],
        foreground=[("selected", ModernTheme.TEXT_PRIMARY)],
    )

    style.configure(
        "Vertical.TScrollbar",
        background=ModernTheme.BG_PANEL_ALT,
        troughcolor=ModernTheme.BG_SECONDARY,
        arrowcolor=ModernTheme.TEXT_MUTED,
        bordercolor=ModernTheme.BORDER_COLOR,
    )
    style.configure(
        "TProgressbar",
        background=ModernTheme.PRIMARY,
        troughcolor=ModernTheme.BG_SECONDARY,
        borderwidth=0,
        lightcolor=ModernTheme.PRIMARY,
        darkcolor=ModernTheme.PRIMARY,
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
    """Create a branded card frame with optional title."""
    card = ttk.Frame(parent, style="Card.TFrame", **kwargs)

    if title:
        header = ttk.Frame(card, style="Card.TFrame")
        header.pack(fill="x", padx=ModernTheme.PADDING_LG, pady=(ModernTheme.PADDING_LG, ModernTheme.PADDING_MD))

        title_label = ttk.Label(header, text=title, style="CardHeading.TLabel")
        title_label.pack(side="left", anchor="w")

        if show_size:
            size_label = ttk.Label(header, text="", style="CardMuted.TLabel", anchor="e")
            size_label.pack(side="right", anchor="e")
            _bind_size_label(card, size_label)

        content = ttk.Frame(card, style="Card.TFrame")
        content.pack(
            fill="both",
            expand=True,
            padx=ModernTheme.PADDING_LG,
            pady=(0, ModernTheme.PADDING_LG),
        )
        return card, content

    return card


def add_tooltip(widget, text):
    """Add a simple branded tooltip to a widget."""

    def on_enter(event):
        tooltip = tk.Toplevel()
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")

        label = tk.Label(
            tooltip,
            text=text,
            background=ModernTheme.BG_PANEL_ALT,
            foreground=ModernTheme.TEXT_PRIMARY,
            relief="solid",
            borderwidth=1,
            padx=ModernTheme.PADDING_MD,
            pady=ModernTheme.PADDING_SM,
            font=ModernTheme.FONT_SMALL,
        )
        label.pack()
        widget.tooltip = tooltip

    def on_leave(event):
        if hasattr(widget, "tooltip"):
            widget.tooltip.destroy()
            delattr(widget, "tooltip")

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)
