import os
from pathlib import Path
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from core.utils.helpers import set_status
from modules.release_creator import logic


def build_ui(parent, status_var=None):
    frame = ttk.Frame(parent)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    project_var = tk.StringVar()
    target_var = tk.StringVar()
    release_name_var = tk.StringVar()
    version_var = tk.StringVar()
    output_text = tk.StringVar(value="No release created yet.")
    include_docs_var = tk.BooleanVar(value=True)
    include_screenshots_var = tk.BooleanVar(value=True)
    include_build_var = tk.BooleanVar(value=True)
    generate_docs_var = tk.BooleanVar(value=True)
    progress_text_var = tk.StringVar(value="Idle")
    last_release_path = {"value": ""}
    preview_text_var = tk.StringVar(value="Preview not run.")
    is_working = False

    # Project and target selectors
    selector_frame = ttk.Frame(frame)
    selector_frame.pack(fill="x", pady=(0, 10))

    project_label = ttk.Label(selector_frame, text="Project:")
    project_label.grid(row=0, column=0, sticky="w", padx=(0, 4))
    project_entry = ttk.Entry(selector_frame, textvariable=project_var)
    project_entry.grid(row=0, column=1, sticky="ew", padx=(0, 4), pady=4)

    target_label = ttk.Label(selector_frame, text="Release Folder:")
    target_label.grid(row=1, column=0, sticky="w", padx=(0, 4))
    target_entry = ttk.Entry(selector_frame, textvariable=target_var)
    target_entry.grid(row=1, column=1, sticky="ew", padx=(0, 4), pady=4)

    def choose_project():
        path = filedialog.askdirectory(title="Select project folder")
        if path:
            project_var.set(path)
            set_status(status_var, f"Release project set to: {path}")

    def choose_target():
        path = filedialog.askdirectory(title="Select release folder")
        if path:
            target_var.set(path)
            set_status(status_var, f"Release target set to: {path}")

    project_browse = ttk.Button(selector_frame, text="Browse", command=choose_project)
    project_browse.grid(row=0, column=2, padx=(4, 0), pady=4)

    target_browse = ttk.Button(selector_frame, text="Browse", command=choose_target)
    target_browse.grid(row=1, column=2, padx=(4, 0), pady=4)

    selector_frame.columnconfigure(1, weight=1)

    # Options
    options_frame = ttk.LabelFrame(frame, text="Options")
    options_frame.pack(fill="x", pady=(0, 10))

    ttk.Label(options_frame, text="Release Name:").grid(row=0, column=0, sticky="w", padx=(8, 4), pady=4)
    release_entry = ttk.Entry(options_frame, textvariable=release_name_var)
    release_entry.grid(row=0, column=1, sticky="ew", padx=(0, 8), pady=4)

    ttk.Label(options_frame, text="Version (optional):").grid(row=1, column=0, sticky="w", padx=(8, 4), pady=4)
    version_entry = ttk.Entry(options_frame, textvariable=version_var)
    version_entry.grid(row=1, column=1, sticky="ew", padx=(0, 8), pady=4)

    options_frame.columnconfigure(1, weight=1)

    checks_frame = ttk.Frame(options_frame)
    checks_frame.grid(row=2, column=0, columnspan=2, sticky="w", padx=(8, 0), pady=(4, 6))

    ttk.Checkbutton(
        checks_frame,
        text="Include docs",
        variable=include_docs_var,
    ).pack(side="left", padx=(0, 10))
    ttk.Checkbutton(
        checks_frame,
        text="Include screenshots",
        variable=include_screenshots_var,
    ).pack(side="left", padx=(0, 10))
    ttk.Checkbutton(
        checks_frame,
        text="Include build outputs",
        variable=include_build_var,
    ).pack(side="left")
    ttk.Checkbutton(
        checks_frame,
        text="Generate docs (LLM)",
        variable=generate_docs_var,
    ).pack(side="left", padx=(10, 0))

    preflight_frame = ttk.LabelFrame(frame, text="Pre-flight Preview")
    preflight_frame.pack(fill="x", pady=(0, 10))

    llm_summary_var = tk.BooleanVar(value=False)

    def run_preview(show_empty_warning: bool = True, run_summary: bool = False):
        project_path = project_var.get() or ""
        if not project_path:
            if show_empty_warning:
                set_status(status_var, "Set a project folder first.")
            return
        summary = logic.preview_release_contents(project_path)
        if "error" in summary:
            preview_text_var.set(summary["error"])
            return

        project_type = summary.get("project_type", "unknown")
        docs_found = summary.get("docs_found", [])
        docs_dir_files = summary.get("docs_dir_files", [])
        screenshots_count = summary.get("screenshots_count", 0)
        screenshot_folders = summary.get("screenshot_folders", {})
        build_counts = summary.get("build_counts", {})
        build_dirs = summary.get("build_dirs", [])
        ext_counts = summary.get("ext_counts", {})

        top_exts = sorted(ext_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        ext_summary = ", ".join(f"{ext}({count})" for ext, count in top_exts) if top_exts else "n/a"

        docs_samples = [Path(p).name for p in docs_found[:5]]
        if not docs_samples and docs_dir_files:
            docs_samples = [Path(p).name for p in docs_dir_files[:5]]

        screenshot_samples = []
        if isinstance(screenshot_folders, dict):
            for folder, count in list(screenshot_folders.items())[:3]:
                screenshot_samples.append(f"{Path(folder).name}({count})")

        build_total = sum(build_counts.values()) if isinstance(build_counts, dict) else 0
        base_text = (
            "Project type: {ptype}\n"
            "Top file types: {exts}\n"
            "Docs: {docs}\n"
            "Screenshots: {shots}\n"
            "Build outputs: {builds}".format(
                ptype=project_type,
                exts=ext_summary,
                docs=", ".join(docs_samples) if docs_samples else "none",
                shots=", ".join(screenshot_samples) if screenshot_samples else str(screenshots_count),
                builds=f"{len(build_dirs)} dirs ({build_total} files)" if build_dirs else "none",
            )
        )
        preview_text_var.set(base_text)
        if run_summary and llm_summary_var.get():
            preview_text_var.set(base_text + "\n\nSummary: generating...")

            def worker():
                summary_text = logic.generate_project_summary(project_path)
                def finish():
                    preview_text_var.set(base_text + "\n\nSummary: " + summary_text)
                frame.after(0, finish)

            threading.Thread(target=worker, daemon=True).start()
        set_status(status_var, "Preview updated.")

    ttk.Button(preflight_frame, text="Preview", command=lambda: run_preview(True, llm_summary_var.get())).pack(
        side="left", padx=(8, 8), pady=6
    )
    summary_check = ttk.Checkbutton(
        preflight_frame,
        text="LLM summary",
        variable=llm_summary_var,
    )
    summary_check.pack(side="left", padx=(0, 8), pady=6)
    preview_label = ttk.Label(preflight_frame, textvariable=preview_text_var, justify="left", wraplength=720)
    preview_label.pack(side="left", padx=(0, 8), pady=6)

    def schedule_preview(*_args):
        frame.after(100, lambda: run_preview(False, llm_summary_var.get()))

    project_var.trace_add("write", schedule_preview)
    llm_summary_var.trace_add("write", schedule_preview)

    def set_working(working: bool, label: str):
        nonlocal is_working
        is_working = working
        state = "disabled" if working else "normal"
        create_btn.config(state=state)
        ship_btn.config(state=state)
        progress_text_var.set(label)
        if working:
            progress.start(10)
        else:
            progress.stop()

    def _capture_release_path(result: str):
        for line in result.splitlines():
            if line.startswith("Release created: "):
                last_release_path["value"] = line.replace("Release created: ", "").strip()
                break

    def _make_status_updater():
        def updater(message: str):
            frame.after(0, lambda: progress_text_var.set(message))
        return updater

    def run_async(action, label: str, done_status: str):
        nonlocal is_working
        if is_working:
            return
        set_working(True, label)

        def worker():
            try:
                result = action()
                ok = True
            except Exception as e:
                result = f"Error: {e}"
                ok = False

            def finish():
                output_text.set(result)
                if ok:
                    _capture_release_path(result)
                set_working(False, "Idle")
                set_status(status_var, done_status if ok else "Action failed.")

            frame.after(0, finish)

        threading.Thread(target=worker, daemon=True).start()

    # Create button
    def create_release():
        project_path = project_var.get() or ""
        target_path = target_var.get() or ""
        if not project_path or not target_path:
            set_status(status_var, "Set both project and release folders.")
            return
        if not messagebox.askyesno("Confirm Release", "Create release structure in the target folder?"):
            return
        run_async(
            lambda: logic.create_release_structure(
                project_path=project_path,
                target_path=target_path,
                release_name=release_name_var.get().strip() or None,
                version=version_var.get().strip() or None,
                include_docs=include_docs_var.get(),
                include_screenshots=include_screenshots_var.get(),
                include_build=include_build_var.get(),
            ),
            "Creating release...",
            "Release created.",
        )

    def one_click_ship():
        project_path = project_var.get() or ""
        target_path = target_var.get() or ""
        if not project_path or not target_path:
            set_status(status_var, "Set both project and release folders.")
            return
        if not messagebox.askyesno("Confirm One-Click Ship", "Run one-click ship for this project?"):
            return
        status_updater = _make_status_updater()
        run_async(
            lambda: logic.create_one_click_ship(
                project_path=project_path,
                target_path=target_path,
                release_name=release_name_var.get().strip() or None,
                version=version_var.get().strip() or None,
                include_docs=include_docs_var.get(),
                include_screenshots=include_screenshots_var.get(),
                include_build=include_build_var.get(),
                generate_docs=generate_docs_var.get(),
                on_status=status_updater,
            ),
            "Shipping...",
            "One-click ship complete.",
        )

    btn_frame = ttk.Frame(frame)
    btn_frame.pack(fill="x", pady=(0, 10))

    create_btn = ttk.Button(btn_frame, text="Create Release Structure", command=create_release)
    create_btn.pack(fill="x", pady=(0, 6))

    ship_btn = ttk.Button(btn_frame, text="One-Click Ship", command=one_click_ship)
    ship_btn.pack(fill="x")

    progress_frame = ttk.Frame(frame)
    progress_frame.pack(fill="x", pady=(0, 10))

    progress = ttk.Progressbar(progress_frame, mode="indeterminate")
    progress.pack(fill="x", side="left", expand=True, padx=(0, 8))
    progress_label = ttk.Label(progress_frame, textvariable=progress_text_var)
    progress_label.pack(side="right")

    actions_frame = ttk.Frame(frame)
    actions_frame.pack(fill="x", pady=(0, 10))

    def open_release_folder():
        path = last_release_path.get("value") or ""
        if not path:
            messagebox.showinfo("No release", "Create a release first.")
            return
        try:
            os.startfile(path)
        except Exception as e:
            messagebox.showerror("Open Error", f"Failed to open folder:\n{e}")

    def open_manifest():
        path = last_release_path.get("value") or ""
        if not path:
            messagebox.showinfo("No release", "Create a release first.")
            return
        manifest_path = os.path.join(path, "manifest.json")
        if not os.path.exists(manifest_path):
            messagebox.showerror("Missing manifest", "manifest.json not found.")
            return
        try:
            os.startfile(manifest_path)
        except Exception as e:
            messagebox.showerror("Open Error", f"Failed to open manifest:\n{e}")

    def copy_summary():
        text = output_text.get().strip()
        if not text:
            messagebox.showinfo("No output", "Nothing to copy.")
            return
        frame.clipboard_clear()
        frame.clipboard_append(text)
        set_status(status_var, "Summary copied to clipboard.")

    ttk.Button(actions_frame, text="Open Release Folder", command=open_release_folder).pack(
        side="left", padx=(0, 8)
    )
    ttk.Button(actions_frame, text="Open Manifest", command=open_manifest).pack(
        side="left", padx=(0, 8)
    )
    ttk.Button(actions_frame, text="Copy Summary", command=copy_summary).pack(side="left")

    # Output
    output_frame = ttk.LabelFrame(frame, text="Output")
    output_frame.pack(fill="both", expand=True)

    label = ttk.Label(output_frame, textvariable=output_text, justify="left", anchor="nw")
    label.pack(fill="both", expand=True, padx=8, pady=8)
