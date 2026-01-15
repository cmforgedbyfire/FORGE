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

    # Build actions
    actions_card, actions_content = create_card_frame(main_frame, "Build Actions")
    actions_card.pack(fill="x", pady=(0, ModernTheme.PADDING_LG))

    # Progress bar
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(
        actions_content, 
        variable=progress_var, 
        maximum=100,
        mode='determinate'
    )
    progress_bar.pack(fill="x", pady=(0, ModernTheme.PADDING_MD))

    # Action buttons
    buttons_frame = ttk.Frame(actions_content)
    buttons_frame.pack(fill="x")

    def run_build_threaded(action_func, action_name):
        """Run build action in background thread with progress."""
        def worker():
            try:
                progress_var.set(0)
                set_status(status_var, f"Starting {action_name}...")
                progress_var.set(25)
                
                if not project_var.get():
                    raise ValueError("Please select a project folder first")
                
                progress_var.set(50)
                result = action_func(project_var.get(), project_type_var.get())
                
                progress_var.set(100)
                set_status(status_var, f"{action_name} completed successfully")
                
                # Update output display
                output_text.config(state="normal")
                output_text.delete("1.0", "end")
                output_text.insert("1.0", str(result))
                output_text.config(state="disabled")
                
            except Exception as e:
                progress_var.set(0)
                set_status(status_var, f"{action_name} failed: {str(e)}")
                messagebox.showerror(f"{action_name} Error", str(e))
                
                # Show error in output
                output_text.config(state="normal")
                output_text.delete("1.0", "end")
                output_text.insert("1.0", f"ERROR: {str(e)}")
                output_text.config(state="disabled")
        
        threading.Thread(target=worker, daemon=True).start()

    detect_btn = ttk.Button(
        buttons_frame,
        text="Detect Type",
        command=lambda: safe_execute(
            lambda: [
                project_type_var.set(logic.detect_project_type(project_var.get())),
                set_status(status_var, f"Detected: {project_type_var.get()}")
            ],
            "project detection"
        )
    )
    detect_btn.pack(side="left", padx=(0, ModernTheme.PADDING_MD))
    add_tooltip(detect_btn, "Auto-detect project type from files")

    build_btn = ttk.Button(
        buttons_frame,
        text="Build Project",
        command=lambda: run_build_threaded(
            lambda path, ptype: logic.run_build(path, project_type=None if ptype == "auto" else ptype),
            "Build"
        ),
        style="Primary.TButton"
    )
    build_btn.pack(side="left", padx=(0, ModernTheme.PADDING_MD))
    add_tooltip(build_btn, "Build the project")

    package_btn = ttk.Button(
        buttons_frame,
        text="Create Package",
        command=lambda: run_build_threaded(
            lambda path, ptype: logic.create_package(path, path, project_type=None if ptype == "auto" else ptype),
            "Packaging"
        )
    )
    package_btn.pack(side="left")
    add_tooltip(package_btn, "Create distributable package")

    # Output display
    output_card, output_content = create_card_frame(main_frame, "Build Output")
    output_card.pack(fill="both", expand=True)

    # Text widget with scrollbar
    text_frame = ttk.Frame(output_content)
    text_frame.pack(fill="both", expand=True)

    output_text = tk.Text(
        text_frame,
        height=8,
        wrap="word",
        font=('Consolas', 9),
        bg=ModernTheme.BG_SECONDARY,
        relief="flat",
        padx=ModernTheme.PADDING_MD,
        pady=ModernTheme.PADDING_MD
    )
    
    scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=output_text.yview)
    output_text.configure(yscrollcommand=scrollbar.set)
    
    output_text.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Add initial message
    output_text.insert("1.0", "Select a project and choose build actions.\n\nBuild output will appear here...")
    output_text.config(state="disabled")