import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from core.utils.helpers import set_status
from core.ui.modern_theme import create_card_frame, ModernTheme, add_tooltip
from core.utils.enhanced_helpers import validate_directory_path, truncate_path
from modules.docs_generator import logic


def build_ui(parent, status_var=None):
    main_frame = ttk.Frame(parent)
    main_frame.pack(fill="both", expand=True, padx=ModernTheme.PADDING_LG, pady=ModernTheme.PADDING_LG)

    # Project configuration
    project_card, project_content = create_card_frame(main_frame, "Project & Templates")
    project_card.pack(fill="x", pady=(0, ModernTheme.PADDING_LG))

    project_var = tk.StringVar()
    template_var = tk.StringVar(value="README")
    
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
        if path and validate_directory_path(path):
            project_var.set(path)
            set_status(status_var, f"Project: {os.path.basename(path)}")
            update_preview()

    browse_btn = ttk.Button(entry_frame, text="Browse", command=choose_project)
    browse_btn.pack(side="right")
    add_tooltip(browse_btn, "Select project folder for documentation generation")
    
    # Template selection
    template_frame = ttk.Frame(project_content)
    template_frame.pack(fill="x")
    
    ttk.Label(template_frame, text="Template Type:").pack(anchor="w")
    
    template_buttons_frame = ttk.Frame(template_frame)
    template_buttons_frame.pack(fill="x", pady=(ModernTheme.PADDING_SM, 0))
    
    templates = [
        ("README", "Project README documentation"),
        ("CHANGELOG", "Version history and changes"),
        ("PRIVACY", "Privacy policy template"),
        ("ARCHITECTURE", "Technical architecture docs")
    ]
    
    for i, (template_name, tooltip_text) in enumerate(templates):
        btn = ttk.Radiobutton(
            template_buttons_frame,
            text=template_name,
            variable=template_var,
            value=template_name,
            command=update_preview
        )
        btn.pack(side="left", padx=(0, ModernTheme.PADDING_LG))
        add_tooltip(btn, tooltip_text)
        output_text.set(text)
        set_status(status_var, "Changelog generated.")

    def gen_architecture():
        project_path = project_var.get() or ""
        if not project_path:
            set_status(status_var, "Set a project folder first.")
            return
        text = logic.generate_architecture_doc(project_path)
        output_text.set(text)
        set_status(status_var, "Architecture summary generated.")

    def gen_features():
        project_path = project_var.get() or ""
        if not project_path:
            set_status(status_var, "Set a project folder first.")
            return
        text = logic.generate_feature_list(project_path)
        output_text.set(text)
        set_status(status_var, "Feature list generated.")

    def gen_privacy():
        project_path = project_var.get() or ""
        if not project_path:
            set_status(status_var, "Set a project folder first.")
            return
        text = logic.generate_privacy_doc(project_path)
        output_text.set(text)
        set_status(status_var, "Privacy statement generated.")

    def gen_website_copy():
        project_path = project_var.get() or ""
        if not project_path:
            set_status(status_var, "Set a project folder first.")
            return
        text = logic.generate_website_copy(project_path)
        output_text.set(text)
        set_status(status_var, "Website copy generated.")

    def gen_printable():
        project_path = project_var.get() or ""
        if not project_path:
            set_status(status_var, "Set a project folder first.")
            return
        text = logic.generate_printable_overview(project_path)
        output_text.set(text)
        set_status(status_var, "Printable overview generated.")

    readme_btn = ttk.Button(btn_frame, text="README", command=gen_readme)
    readme_btn.grid(row=0, column=0, padx=6, pady=6, sticky="ew")

    changelog_btn = ttk.Button(btn_frame, text="Changelog", command=gen_changelog)
    changelog_btn.grid(row=0, column=1, padx=6, pady=6, sticky="ew")

    architecture_btn = ttk.Button(btn_frame, text="Architecture", command=gen_architecture)
    architecture_btn.grid(row=0, column=2, padx=6, pady=6, sticky="ew")

    features_btn = ttk.Button(btn_frame, text="Features", command=gen_features)
    features_btn.grid(row=1, column=0, padx=6, pady=6, sticky="ew")

    privacy_btn = ttk.Button(btn_frame, text="Privacy", command=gen_privacy)
    privacy_btn.grid(row=1, column=1, padx=6, pady=6, sticky="ew")

    website_btn = ttk.Button(btn_frame, text="Website Copy", command=gen_website_copy)
    website_btn.grid(row=1, column=2, padx=6, pady=6, sticky="ew")

    printable_btn = ttk.Button(btn_frame, text="Printable Overview", command=gen_printable)
    printable_btn.grid(row=2, column=0, columnspan=3, padx=6, pady=6, sticky="ew")

    for c in range(3):
        btn_frame.columnconfigure(c, weight=1)

    # Output
    output_frame = ttk.LabelFrame(frame, text="Preview")
    output_frame.pack(fill="both", expand=True)

    text_widget = tk.Text(output_frame, wrap="word")
    text_widget.pack(fill="both", expand=True, padx=8, pady=8)

    def sync_output(*_args):
        text_widget.delete("1.0", "end")
        text_widget.insert("1.0", output_text.get())

    output_text.trace_add("write", sync_output)
    sync_output()

    # Controls
    controls = ttk.Frame(frame)
    controls.pack(fill="x", pady=(8, 0))

    def clear_output():
        output_text.set("")
        set_status(status_var, "Output cleared.")

    def save_output_as():
        content = output_text.get().strip()
        if not content:
            set_status(status_var, "No content to save.")
            return
        filetypes = [
            ("Markdown", "*.md"),
            ("Text", "*.txt"),
            ("HTML", "*.html"),
            ("All files", "*.*"),
        ]
        path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=filetypes,
            title="Save Docs Output As",
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        set_status(status_var, f"Saved output to: {path}")

    ttk.Button(controls, text="Clear", command=clear_output).pack(side="left")
    ttk.Button(controls, text="Save As...", command=save_output_as).pack(side="left", padx=(6, 0))
