import os
import tkinter as tk
from tkinter import ttk, filedialog

from core.ui.modern_theme import ModernTheme, create_card_frame
from core.utils.helpers import set_status
from modules.release_workspace import logic


ACTION_TO_TAB = {
    "screenshots": 1,
    "build": 2,
    "docs": 4,
    "release": 5,
}


def build_ui(parent, status_var=None, select_tab=None):
    main_frame = ttk.Frame(parent)
    main_frame.pack(fill="both", expand=True, padx=ModernTheme.PADDING_LG, pady=ModernTheme.PADDING_LG)

    project_var = tk.StringVar()
    score_var = tk.StringVar(value="Readiness: not audited")
    summary_var = tk.StringVar(value="Choose a project folder to run a release-readiness audit.")

    project_card, project_content = create_card_frame(main_frame, "Release Workspace")
    project_card.pack(fill="x", pady=(0, ModernTheme.PADDING_LG))

    selector = ttk.Frame(project_content)
    selector.pack(fill="x")
    ttk.Label(selector, text="Project Folder:").pack(side="left", padx=(0, ModernTheme.PADDING_MD))
    entry = ttk.Entry(selector, textvariable=project_var)
    entry.pack(side="left", fill="x", expand=True, padx=(0, ModernTheme.PADDING_MD))

    def run_audit():
        project_path = project_var.get().strip()
        result = logic.audit_project(project_path)
        tree.delete(*tree.get_children())
        if not result.get("ok"):
            score_var.set("Readiness: 0%")
            summary_var.set(result.get("error", "Audit failed."))
            set_status(status_var, "Audit failed.")
            return

        score_var.set(f"Readiness: {result['score']}%")
        counts = result.get("counts", {})
        summary_var.set(
            "Type: {ptype} | Source sampled: {src} | Visuals: {visuals} | Outputs: {outputs}".format(
                ptype=result.get("project_type", "unknown"),
                src=counts.get("source_files_sampled", 0),
                visuals=counts.get("screenshots_dirs", 0) + counts.get("image_or_icon_files_sampled", 0),
                outputs=counts.get("release_outputs", 0),
            )
        )
        for item in result.get("items", []):
            tree.insert(
                "",
                "end",
                values=(
                    item["status"].upper(),
                    item["title"],
                    item["detail"],
                    item["action"],
                ),
            )
        set_status(status_var, f"Audit complete: {result['score']}% ready.")

    def browse_project():
        path = filedialog.askdirectory(title="Select project folder")
        if path:
            project_var.set(path)
            set_status(status_var, f"Project selected: {os.path.basename(path)}")
            run_audit()

    ttk.Button(selector, text="Browse", command=browse_project).pack(side="right", padx=(0, ModernTheme.PADDING_MD))
    ttk.Button(selector, text="Audit", command=run_audit, style="Primary.TButton").pack(side="right")

    result_card, result_content = create_card_frame(main_frame, "Readiness")
    result_card.pack(fill="both", expand=True, pady=(0, ModernTheme.PADDING_LG))

    ttk.Label(result_content, textvariable=score_var, style="Heading.TLabel").pack(anchor="w")
    ttk.Label(result_content, textvariable=summary_var).pack(anchor="w", pady=(ModernTheme.PADDING_SM, ModernTheme.PADDING_MD))

    columns = ("status", "item", "detail", "action")
    tree = ttk.Treeview(result_content, columns=columns, show="headings", height=10)
    tree.heading("status", text="Status")
    tree.heading("item", text="Check")
    tree.heading("detail", text="Detail")
    tree.heading("action", text="Action")
    tree.column("status", width=80, anchor="center", stretch=False)
    tree.column("item", width=190, stretch=False)
    tree.column("detail", width=520)
    tree.column("action", width=90, stretch=False)
    tree.pack(fill="both", expand=True)

    action_bar = ttk.Frame(main_frame)
    action_bar.pack(fill="x")

    def go_to(action):
        if select_tab is None:
            return
        index = ACTION_TO_TAB.get(action)
        if index is not None:
            select_tab(index)

    ttk.Button(action_bar, text="Screenshots", command=lambda: go_to("screenshots")).pack(side="left", padx=(0, ModernTheme.PADDING_MD))
    ttk.Button(action_bar, text="Build", command=lambda: go_to("build")).pack(side="left", padx=(0, ModernTheme.PADDING_MD))
    ttk.Button(action_bar, text="Docs", command=lambda: go_to("docs")).pack(side="left", padx=(0, ModernTheme.PADDING_MD))
    ttk.Button(action_bar, text="Release", command=lambda: go_to("release")).pack(side="left")

    def use_selected_action(_event=None):
        selected = tree.selection()
        if not selected:
            return
        action = tree.item(selected[0], "values")[3]
        go_to(action)

    tree.bind("<Double-1>", use_selected_action)
