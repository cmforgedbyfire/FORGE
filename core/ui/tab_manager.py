import tkinter as tk
from tkinter import ttk
import traceback

from core.ui.modern_theme import ModernTheme

# Import module UIs
from modules.screenshots import ui as screenshots_ui
from modules.build_packager import ui as build_packager_ui
from modules.ai_packager import ui as ai_packager_ui
from modules.docs_generator import ui as docs_generator_ui
from modules.release_creator import ui as release_creator_ui
from modules.llm_assistant import ui as llm_assistant_ui
from modules.release_workspace import ui as release_workspace_ui


class TabManager:
    def __init__(self, parent, status_var=None):
        self.parent = parent
        self.status_var = status_var

        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill="both", expand=True)

        self._build_tabs()

    def _build_tabs(self):
        self._add_tab(
            "Release Workspace",
            lambda frame: release_workspace_ui.build_ui(
                frame,
                status_var=self.status_var,
                select_tab=lambda index: self.notebook.select(index),
            ),
        )
        self._add_tab("Screenshots", lambda frame: screenshots_ui.build_ui(frame, status_var=self.status_var))
        self._add_tab("Build & Package", lambda frame: build_packager_ui.build_ui(frame, status_var=self.status_var))
        self._add_tab("AI Packager", lambda frame: ai_packager_ui.build_ui(frame, status_var=self.status_var))
        self._add_tab("Docs & Changelog", lambda frame: docs_generator_ui.build_ui(frame, status_var=self.status_var))
        self._add_tab("Release Creator", lambda frame: release_creator_ui.build_ui(frame, status_var=self.status_var))
        self._add_tab("LLM Assistant", lambda frame: llm_assistant_ui.build_ui(frame, status_var=self.status_var))

    def _add_tab(self, title, build_func):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        try:
            build_func(frame)
        except Exception:
            self._show_tab_error(frame, title, traceback.format_exc())
            if self.status_var is not None:
                self.status_var.set(f"{title} failed to load. Other tools are still available.")

    def _show_tab_error(self, frame, title, details):
        panel = ttk.Frame(frame, style="Card.TFrame")
        panel.pack(fill="both", expand=True, padx=16, pady=16)
        ttk.Label(panel, text=f"{title} could not load", style="CardHeading.TLabel").pack(anchor="w")
        ttk.Label(
            panel,
            text="The rest of FORGE is still available. Restart after fixing the issue or report the details below.",
            wraplength=720,
            style="Card.TLabel",
        ).pack(anchor="w", pady=(6, 10))
        text = tk.Text(
            panel,
            height=14,
            wrap="word",
            bg=ModernTheme.BG_SECONDARY,
            fg=ModernTheme.TEXT_PRIMARY,
            insertbackground=ModernTheme.TEXT_PRIMARY,
            relief="solid",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=ModernTheme.BORDER_COLOR,
            highlightcolor=ModernTheme.BORDER_FOCUS,
            font=("Consolas", 9),
        )
        text.pack(fill="both", expand=True)
        text.insert("1.0", details)
        text.config(state="disabled")
