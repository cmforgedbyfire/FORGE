import tkinter as tk
from tkinter import ttk

# Import module UIs
from modules.screenshots import ui as screenshots_ui
from modules.build_packager import ui as build_packager_ui
from modules.ai_packager import ui as ai_packager_ui
from modules.docs_generator import ui as docs_generator_ui
from modules.release_creator import ui as release_creator_ui
from modules.llm_assistant import ui as llm_assistant_ui


class TabManager:
    def __init__(self, parent, status_var=None):
        self.parent = parent
        self.status_var = status_var

        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill="both", expand=True)

        self._build_tabs()

    def _build_tabs(self):
        # Screenshots
        screenshots_frame = ttk.Frame(self.notebook)
        self.notebook.add(screenshots_frame, text="Screenshots")
        screenshots_ui.build_ui(screenshots_frame, status_var=self.status_var)

        # Build Packager
        build_frame = ttk.Frame(self.notebook)
        self.notebook.add(build_frame, text="Build & Package")
        build_packager_ui.build_ui(build_frame, status_var=self.status_var)

        # AI Packager
        ai_frame = ttk.Frame(self.notebook)
        self.notebook.add(ai_frame, text="AI Packager")
        ai_packager_ui.build_ui(ai_frame, status_var=self.status_var)

        # Docs Generator
        docs_frame = ttk.Frame(self.notebook)
        self.notebook.add(docs_frame, text="Docs & Changelog")
        docs_generator_ui.build_ui(docs_frame, status_var=self.status_var)

        # Release Creator
        release_frame = ttk.Frame(self.notebook)
        self.notebook.add(release_frame, text="Release Creator")
        release_creator_ui.build_ui(release_frame, status_var=self.status_var)

        # LLM Assistant
        llm_frame = ttk.Frame(self.notebook)
        self.notebook.add(llm_frame, text="LLM Assistant")
        llm_assistant_ui.build_ui(llm_frame, status_var=self.status_var)
