import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os

from core.utils.helpers import set_status
from core.ui.modern_theme import create_card_frame, ModernTheme, add_tooltip
from core.utils.error_handling import safe_execute
from modules.build_packager import logic


def build_ui(parent, status_var=None):
    main_frame = ttk.Frame(parent)
    main_frame.pack(fill="both", expand=True, padx=ModernTheme.PADDING_LG, pady=ModernTheme.PADDING_LG)

    # Project configuration
    project_card, project_content = create_card_frame(main_frame, "Project Configuration")
    project_card.pack(fill="x", pady=(0, ModernTheme.PADDING_LG))

    project_var = tk.StringVar()
    project_type_var = tk.StringVar(value="auto")
    
    # Project path
    path_frame = ttk.Frame(project_content)
    path_frame.pack(fill="x", pady=(0, ModernTheme.PADDING_MD))
    
    ttk.Label(path_frame, text="Project Path:").pack(anchor="w")
    
    entry_frame = ttk.Frame(path_frame)
    entry_frame.pack(fill="x", pady=(ModernTheme.PADDING_SM, 0))
    
    entry = ttk.Entry(entry_frame, textvariable=project_var)
    entry.pack(side="left", fill="x", expand=True, padx=(0, ModernTheme.PADDING_MD))

    def choose_project():
        path = filedialog.askdirectory(title="Select project folder")
        if path:
            project_var.set(path)
            # Auto-detect project type
            detected_type = safe_execute(
                lambda: logic.detect_project_type(path),
                "project type detection",
                "unknown"
            )
            project_type_var.set(detected_type)
            set_status(status_var, f"Project: {os.path.basename(path)} ({detected_type})")

    browse_btn = ttk.Button(entry_frame, text="Browse", command=choose_project)
    browse_btn.pack(side="right")
    add_tooltip(browse_btn, "Select project folder to build")
    
    # Project type selection
    type_frame = ttk.Frame(project_content)
    type_frame.pack(fill="x")
    
    ttk.Label(type_frame, text="Project Type:").pack(anchor="w")
    type_combo = ttk.Combobox(
        type_frame,
        textvariable=project_type_var,
        values=["auto", "python", "node", "python+node", "dotnet", "go", "rust", "other"],
        state="readonly",
        width=15
    )
    type_combo.pack(anchor="w", pady=(ModernTheme.PADDING_SM, 0))
    add_tooltip(type_combo, "Select project type for build optimization")
            "rust",
            "java",
            "ruby",
            "php",
            "cpp",
        ],
        width=18,
        state="readonly",
    )
    type_combo.pack(side="left", padx=(6, 0))

    def detect():
        project_path = project_var.get() or ""
        if not project_path:
            set_status(status_var, "Set a project folder first.")
            return
        p_type = logic.detect_project_type(project_path)
        output_text.set(f"Detected project type: {p_type}")
        set_status(status_var, "Project detection complete.")

    def build():
        project_path = project_var.get() or ""
        if not project_path:
            set_status(status_var, "Set a project folder first.")
            return
        if not messagebox.askyesno("Confirm Build", "Run build for this project?"):
            return
        selected = project_type_var.get()
        ptype = None if selected == "auto" else selected
        msg = logic.run_build(project_path, project_type=ptype)
        output_text.set(msg)
        set_status(status_var, "Build command invoked (placeholder).")

    def package():
        project_path = project_var.get() or ""
        if not project_path:
            set_status(status_var, "Set a project folder first.")
            return
        if not messagebox.askyesno("Confirm Package", "Create a package zip for this project?"):
            return
        # Later: ask for explicit output path
        selected = project_type_var.get()
        ptype = None if selected == "auto" else selected
        msg = logic.create_package(project_path, project_path, project_type=ptype)
        output_text.set(msg)
        set_status(status_var, "Package command invoked (placeholder).")

    detect_btn = ttk.Button(btn_frame, text="Detect Project Type", command=detect)
    detect_btn.grid(row=1, column=0, padx=6, pady=6, sticky="ew")

    build_btn = ttk.Button(btn_frame, text="Run Build", command=build)
    build_btn.grid(row=1, column=1, padx=6, pady=6, sticky="ew")

    package_btn = ttk.Button(btn_frame, text="Create Package", command=package)
    package_btn.grid(row=1, column=2, padx=6, pady=6, sticky="ew")

    btn_frame.columnconfigure(0, weight=1)
    btn_frame.columnconfigure(1, weight=1)
    btn_frame.columnconfigure(2, weight=1)

    # Output / info
    output_frame = ttk.LabelFrame(frame, text="Output")
    output_frame.pack(fill="both", expand=True)

    label = ttk.Label(output_frame, textvariable=output_text, justify="left", anchor="nw")
    label.pack(fill="both", expand=True, padx=8, pady=8)
