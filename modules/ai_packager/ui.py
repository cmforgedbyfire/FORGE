import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from core.utils.helpers import set_status
from modules.ai_packager import logic


def build_ui(parent, status_var=None):
    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    project_var = tk.StringVar()
    output_text = tk.StringVar(value="No AI analysis performed yet.")

    # Folder selector
    project_frame = ttk.LabelFrame(frame, text="AI Project")
    project_frame.pack(fill="x", pady=(0, 10))

    entry = ttk.Entry(project_frame, textvariable=project_var)
    entry.pack(side="left", fill="x", expand=True, padx=(8, 4), pady=6)

    def choose_project():
        path = filedialog.askdirectory(title="Select AI project folder")
        if path:
            project_var.set(path)
            set_status(status_var, f"AI project set to: {path}")

    browse_btn = ttk.Button(project_frame, text="Browse", command=choose_project)
    browse_btn.pack(side="right", padx=(4, 8), pady=6)

    # Actions
    btn_frame = ttk.LabelFrame(frame, text="Actions")
    btn_frame.pack(fill="x", pady=(0, 10))

    def summarize():
        project_path = project_var.get() or ""
        if not project_path:
            set_status(status_var, "Set an AI project folder first.")
            return
        msg = logic.summarize_ai_project(project_path)
        output_text.set(msg)
        set_status(status_var, "AI project summary (placeholder).")

    def bundle():
        project_path = project_var.get() or ""
        if not project_path:
            set_status(status_var, "Set an AI project folder first.")
            return
        if not messagebox.askyesno("Confirm Bundle", "Create an AI bundle for this project?"):
            return
        msg = logic.create_ai_bundle(project_path, project_path)
        output_text.set(msg)
        set_status(status_var, "AI bundle creation (placeholder).")

    summary_btn = ttk.Button(btn_frame, text="Summarize AI Project", command=summarize)
    summary_btn.grid(row=0, column=0, padx=6, pady=6, sticky="ew")

    bundle_btn = ttk.Button(btn_frame, text="Create AI Bundle", command=bundle)
    bundle_btn.grid(row=0, column=1, padx=6, pady=6, sticky="ew")

    btn_frame.columnconfigure(0, weight=1)
    btn_frame.columnconfigure(1, weight=1)

    # Output
    output_frame = ttk.LabelFrame(frame, text="Output")
    output_frame.pack(fill="both", expand=True)

    label = ttk.Label(output_frame, textvariable=output_text, justify="left", anchor="nw")
    label.pack(fill="both", expand=True, padx=8, pady=8)
