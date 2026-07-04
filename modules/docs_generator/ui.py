import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

from core.utils.helpers import set_status
from core.ui.modern_theme import create_card_frame, ModernTheme, add_tooltip
from core.utils.logging import get_logger
from modules.docs_generator import logic

logger = get_logger(__name__)


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
        if path:
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
            command=lambda: update_preview()
        )
        btn.pack(side="left", padx=(0, ModernTheme.PADDING_LG))
        add_tooltip(btn, tooltip_text)

    # Generation actions
    actions_card, actions_content = create_card_frame(main_frame, "Actions")
    actions_card.pack(fill="x", pady=(0, ModernTheme.PADDING_LG))
    
    actions_frame = ttk.Frame(actions_content)
    actions_frame.pack(fill="x")
    
    def generate_and_save():
        """Generate documentation and save to file."""
        if not project_var.get():
            messagebox.showerror("Error", "Please select a project folder first.")
            return
        
        try:
            template_type = template_var.get()
            project_path = project_var.get()
            
            # Generate content based on template
            if template_type == "README":
                content = logic.generate_readme_stub(project_path)
                filename = "README.md"
            elif template_type == "CHANGELOG":
                content = logic.generate_changelog_stub(project_path)
                filename = "CHANGELOG.md"
            elif template_type == "PRIVACY":
                content = "# Privacy Policy\n\nThis application respects your privacy..."
                filename = "PRIVACY.md"
            elif template_type == "ARCHITECTURE":
                content = "# Architecture\n\nThis document describes the technical architecture..."
                filename = "ARCHITECTURE.md"
            else:
                raise ValueError(f"Unknown template type: {template_type}")
            
            # Save to file
            output_path = os.path.join(project_path, filename)
            
            # Ask for confirmation if file exists
            if os.path.exists(output_path):
                if not messagebox.askyesno(
                    "File Exists", 
                    f"{filename} already exists. Overwrite?"
                ):
                    return
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            set_status(status_var, f"Generated: {filename}")
            messagebox.showinfo("Success", f"Generated {filename} successfully!")
            update_preview()
            
        except Exception as e:
            messagebox.showerror("Generation Error", f"Failed to generate documentation:\n{str(e)}")
            set_status(status_var, "Generation failed")
    
    def update_preview():
        """Update the preview with current selection."""
        if not project_var.get():
            preview_text.config(state="normal")
            preview_text.delete("1.0", "end")
            preview_text.insert("1.0", "Select a project folder to see preview...")
            preview_text.config(state="disabled")
            return
        
        try:
            template_type = template_var.get()
            project_path = project_var.get()
            
            # Generate preview content
            if template_type == "README":
                content = logic.generate_readme_stub(project_path)
            elif template_type == "CHANGELOG":
                content = logic.generate_changelog_stub(project_path)
            elif template_type == "PRIVACY":
                content = "# Privacy Policy\n\nThis application respects your privacy and does not collect personal information..."
            elif template_type == "ARCHITECTURE":
                content = "# Architecture Documentation\n\nThis document outlines the technical architecture and design decisions..."
            else:
                content = "Unknown template type"
            
            preview_text.config(state="normal")
            preview_text.delete("1.0", "end")
            preview_text.insert("1.0", content)
            preview_text.config(state="disabled")
            
        except Exception as e:
            preview_text.config(state="normal")
            preview_text.delete("1.0", "end")
            preview_text.insert("1.0", f"Error generating preview: {str(e)}")
            preview_text.config(state="disabled")
    
    generate_btn = ttk.Button(
        actions_frame,
        text="Generate & Save",
        command=generate_and_save,
        style="Primary.TButton"
    )
    generate_btn.pack(side="left", padx=(0, ModernTheme.PADDING_MD))
    add_tooltip(generate_btn, "Generate documentation and save to project folder")
    
    preview_btn = ttk.Button(
        actions_frame,
        text="Update Preview",
        command=update_preview
    )
    preview_btn.pack(side="left")
    add_tooltip(preview_btn, "Refresh preview with current settings")
    
    # Live preview
    preview_card, preview_content = create_card_frame(main_frame, "Live Preview")
    preview_card.pack(fill="both", expand=True)
    
    # Preview text with scrollbar
    preview_frame = ttk.Frame(preview_content)
    preview_frame.pack(fill="both", expand=True)
    
    preview_text = tk.Text(
        preview_frame,
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
    
    preview_scrollbar = ttk.Scrollbar(preview_frame, orient="vertical", command=preview_text.yview)
    preview_text.configure(yscrollcommand=preview_scrollbar.set)
    
    preview_text.pack(side="left", fill="both", expand=True)
    preview_scrollbar.pack(side="right", fill="y")
    
    # Initial preview
    preview_text.insert("1.0", "Select a project folder and template to see preview...")
    preview_text.config(state="disabled")
