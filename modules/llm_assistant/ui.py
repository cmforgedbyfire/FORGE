import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from core.utils.helpers import set_status
from modules.llm_assistant import logic


class LLMAssistantUI:
    def __init__(self, parent, status_var=None):
        self.parent = parent
        self.status_var = status_var

        saved_settings = logic.load_local_llm_settings()
        self.base_url_var = tk.StringVar(value=saved_settings.base_url)
        self.model_var = tk.StringVar(value=saved_settings.model)
        self.temperature_var = tk.DoubleVar(value=saved_settings.temperature)
        self.ai_enabled_var = tk.BooleanVar(value=saved_settings.enabled)
        self.preset_var = tk.StringVar(value="generic_chat")
        self.project_path_var = tk.StringVar(value="")
        self.ai_status_var = tk.StringVar(value="AI status: unknown")
        self.current_thread = None
        self.streaming = False

        self.root_frame = None
        self.project_frame = None

        self._build_ui()
        self._setup_drag_and_drop()

    # ---------------- UI construction ----------------

    def _build_ui(self):
        root = ttk.Frame(self.parent)
        root.pack(fill="both", expand=True, padx=10, pady=10)
        self.root_frame = root

        # Local LLM settings
        llm_frame = ttk.LabelFrame(root, text="LLM Configuration")
        llm_frame.pack(fill="x", pady=(0, 8))

        ttk.Label(llm_frame, text="API Endpoint:").grid(row=0, column=0, sticky="w", padx=(8, 4), pady=6)
        base_entry = ttk.Entry(llm_frame, textvariable=self.base_url_var)
        base_entry.grid(row=0, column=1, sticky="ew", padx=(0, 8), pady=6)

        ttk.Label(llm_frame, text="Model:").grid(row=1, column=0, sticky="w", padx=(8, 4), pady=6)
        model_combo = ttk.Combobox(
            llm_frame,
            textvariable=self.model_var,
            values=[
                "KATE",
                "gpt-4",
                "claude-3-5-sonnet",
                "custom-model",
            ],
            width=24,
            state="normal",
        )
        model_combo.grid(row=1, column=1, sticky="w", padx=(0, 8), pady=6)

        ttk.Label(llm_frame, text="Temperature:").grid(row=2, column=0, sticky="w", padx=(8, 4), pady=6)
        temp_scale = ttk.Scale(
            llm_frame,
            from_=0.0,
            to=1.0,
            variable=self.temperature_var,
            orient="horizontal",
            length=180,
        )
        temp_scale.grid(row=2, column=1, sticky="w", padx=(0, 8), pady=6)

        enable_check = ttk.Checkbutton(
            llm_frame,
            text="AI Enabled",
            variable=self.ai_enabled_var,
            command=self._toggle_ai_enabled,
        )
        enable_check.grid(row=0, column=2, padx=(0, 8), pady=6, sticky="w")

        save_btn = ttk.Button(
            llm_frame,
            text="Save LLM Settings",
            command=self._save_llm_settings,
        )
        save_btn.grid(row=1, column=2, rowspan=2, padx=(0, 8), pady=6, sticky="ns")

        check_btn = ttk.Button(
            llm_frame,
            text="Check LLM",
            command=self._check_llm,
        )
        check_btn.grid(row=1, column=3, rowspan=2, padx=(0, 8), pady=6, sticky="ns")

        llm_frame.columnconfigure(1, weight=1)

        status_frame = ttk.Frame(root)
        status_frame.pack(fill="x", pady=(0, 8))
        ttk.Label(status_frame, textvariable=self.ai_status_var).pack(side="left")
        ttk.Button(
            status_frame,
            text="Quick Start",
            command=self._show_quick_start,
        ).pack(side="right")

        # Project path + insert button (boxed)
        project_frame = ttk.LabelFrame(root, text="Project Folder")
        project_frame.pack(fill="x", pady=(0, 8), padx=2)
        self.project_frame = project_frame

        ttk.Label(project_frame, text="Path:").pack(side="left", padx=(8, 4), pady=6)
        project_entry = ttk.Entry(project_frame, textvariable=self.project_path_var)
        project_entry.pack(side="left", fill="x", expand=True, padx=(0, 4), pady=6)

        ttk.Button(
            project_frame,
            text="Insert Project…",
            command=self._select_project_folder,
        ).pack(side="left", padx=(4, 8), pady=6)

        # Preset buttons
        preset_frame = ttk.LabelFrame(root, text="Presets")
        preset_frame.pack(fill="x", pady=(0, 8))

        def preset_btn(text, key, column, row=0):
            return ttk.Button(
                preset_frame,
                text=text,
                command=lambda: self._apply_preset(key),
            ).grid(row=row, column=column, padx=3, pady=3, sticky="ew")

        preset_btn("Product Description", "product_description", 0, 0)
        preset_btn("README Overview", "readme_overview", 1, 0)
        preset_btn("Function Outline", "function_outline", 2, 0)
        preset_btn("Privacy Statement", "privacy_statement", 3, 0)

        preset_btn("Changelog Entry", "changelog_entry", 0, 1)
        preset_btn("How-To Guide", "how_to_guide", 1, 1)
        preset_btn("Website Copy", "website_copy", 2, 1)
        preset_btn("Printable / PDF Draft", "printable_pdf", 3, 1)

        for c in range(4):
            preset_frame.columnconfigure(c, weight=1)

        # Input text
        input_frame = ttk.LabelFrame(root, text="Input / Instructions")
        input_frame.pack(fill="both", expand=True, pady=(0, 8))

        self.input_text = tk.Text(input_frame, height=7, wrap="word")
        self.input_text.pack(fill="both", expand=True, padx=4, pady=4)

        # Quick send button
        send_frame = ttk.Frame(root)
        send_frame.pack(fill="x", pady=(0, 8))
        ttk.Button(
            send_frame,
            text="Send to Assistant",
            command=self._on_generate_clicked,
        ).pack(side="left")

        # Output text
        output_frame = ttk.LabelFrame(root, text="Assistant Output")
        output_frame.pack(fill="both", expand=True, pady=(0, 8))

        self.output_text = tk.Text(output_frame, height=14, wrap="word", state="normal")
        self.output_text.pack(fill="both", expand=True, padx=4, pady=4)

        # Control buttons
        control_frame = ttk.Frame(root)
        control_frame.pack(fill="x")

        self.generate_btn = ttk.Button(
            control_frame,
            text="Generate",
            command=self._on_generate_clicked,
        )
        self.generate_btn.pack(side="left", padx=(0, 4))

        self.stop_btn = ttk.Button(
            control_frame,
            text="Stop",
            command=self._on_stop_clicked,
            state="disabled",
        )
        self.stop_btn.pack(side="left", padx=(0, 4))

        ttk.Button(
            control_frame,
            text="Clear",
            command=self._clear_output,
        ).pack(side="left", padx=(0, 4))

        ttk.Button(
            control_frame,
            text="Save As…",
            command=self._save_output_as,
        ).pack(side="left", padx=(0, 4))

        info_label = ttk.Label(
            root,
            text=(
                "Use presets to generate product descriptions, READMEs, privacy notes,\n"
                "function outlines, website copy, and printable/PDF-ready text.\n"
                "Set a project folder (or drag & drop it here) to let the assistant\n"
                "analyze and \"take apart\" your codebase."
            ),
            justify="left",
        )
        info_label.pack(fill="x", pady=(4, 0))

        self._refresh_ai_status()

    # ---------------- Drag & Drop setup ----------------

    def _setup_drag_and_drop(self):
        """
        Try to enable drag-and-drop of folders into the Project Folder box.

        This uses the underlying Tk/tkdnd support if available. If not available,
        nothing breaks — drag & drop is simply ignored.
        """
        if self.project_frame is None:
            return

        widget = self.project_frame

        try:
            # Try to register as a drop target using tkdnd-style API.
            widget.drop_target_register('DND_Files')
            widget.dnd_bind('<<Drop>>', self._on_project_drop)
            set_status(self.status_var, "Drag & drop enabled for Project Folder.")
        except Exception:
            # Drag & drop not available in this environment; fail silently.
            pass

    def _on_project_drop(self, event):
        """
        Handle folder drop into the Project Folder box.
        We take the first path from the drop data and, if it's a directory,
        set it as the project path.
        """
        data = event.data or ""
        # Windows often gives something like: {C:/path/to/folder}
        data = data.strip()
        if data.startswith("{") and data.endswith("}"):
            data = data[1:-1].strip()

        # There may be multiple paths separated by spaces; use the first one.
        if " " in data:
            first = data.split(" ")[0]
        else:
            first = data

        path = first.strip().strip('"')

        if not path:
            return

        import os
        if os.path.isdir(path):
            self.project_path_var.set(path)
            set_status(self.status_var, f"Dropped project folder: {path}")
        else:
            messagebox.showwarning(
                "Invalid drop",
                "Please drag and drop a folder (project root), not a single file.",
            )

    # ---------------- Event handlers ----------------

    def _select_project_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.project_path_var.set(folder)
            set_status(self.status_var, f"Project set: {folder}")

    def _apply_preset(self, key: str):
        self.preset_var.set(key)
        set_status(self.status_var, f"Preset selected: {key}")

        if key == "product_description":
            template = (
                "Describe your product or project in your own words.\n"
                "Example:\n"
                "\"ship_studio is a desktop app that helps developers capture\n"
                "screenshots, package apps, generate docs, and prepare releases.\"\n"
            )
        elif key == "readme_overview":
            template = (
                "Optional: Add any notes you want highlighted in the README.\n"
                "For example: target users, key workflows, or tech stack.\n"
            )
        elif key == "function_outline":
            template = (
                "Optional: Add any notes about the architecture or important modules\n"
                "you want the outline to emphasize.\n"
            )
        elif key == "privacy_statement":
            template = (
                "Describe what kinds of data your app processes, if any.\n"
                "If you're unsure, say what you *want* it to do with data.\n"
            )
        elif key == "changelog_entry":
            template = (
                "Paste bullet points or rough notes about what changed.\n"
                "Example:\n"
                "- Added screenshot region capture\n"
                "- Fixed black-screen bug on Windows\n"
                "- Improved LLM Assistant prompts\n"
            )
        elif key == "how_to_guide":
            template = (
                "Describe which flow you want a HOW-TO for.\n"
                "Example: \"How to capture window screenshots and save them\"\n"
            )
        elif key == "website_copy":
            template = (
                "Describe your ideal user and tone.\n"
                "Example: \"Indie developers shipping desktop tools, calm and trustworthy tone.\"\n"
            )
        elif key == "printable_pdf":
            template = (
                "Add anything you want in a printable overview (for PDFs or handouts).\n"
                "Example: target audience, main pitch, or context.\n"
            )
        else:
            template = ""

        if template:
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert(tk.END, template)

    def _on_generate_clicked(self):
        if self.streaming:
            return

        self._save_llm_settings()

        model = self.model_var.get()
        temperature = float(self.temperature_var.get())
        base_url = self.base_url_var.get().strip()
        raw_input = self.input_text.get("1.0", tk.END).strip()
        preset_key = self.preset_var.get()
        project_path = self.project_path_var.get().strip()

        if not raw_input and not project_path:
            messagebox.showwarning("No input", "Provide some input text or select a project folder.")
            return
        if not self.ai_enabled_var.get():
            messagebox.showwarning("AI Disabled", "AI is currently disabled. Enable it in LLM Configuration settings and configure your endpoint.")
            set_status(self.status_var, "AI disabled.")
            return
        if not logic.check_llm_available(base_url):
            messagebox.showerror(
                "LLM Unavailable",
                "Cannot reach the LLM endpoint. Make sure your LLM server is running\\n"
                "and the API Endpoint is configured correctly.\\n\\n"
                "For local models: Start your LLM server first.\\n"
                "For cloud APIs: Check your API key and endpoint URL.",
            )
            set_status(self.status_var, "LLM unavailable (check endpoint).")
            return

        project_map_json = None
        if project_path:
            try:
                project_map_json = logic.build_project_map_for_path(project_path, max_files=50)
            except Exception as e:
                messagebox.showerror("Project Error", f"Failed to analyze project:\n{e}")
                project_map_json = None

        prompts = logic.build_preset_prompt(preset_key, project_map_json, raw_input)
        system_prompt = prompts["system"]
        user_prompt = prompts["user"]

        # Prepare UI
        self.output_text.delete("1.0", tk.END)
        self._set_streaming(True)
        set_status(self.status_var, f"Generating with {model} ({preset_key})…")

        def on_chunk(text: str):
            self.parent.after(0, lambda: self.output_text.insert(tk.END, text))

        def on_done(final_text: str):
            self.parent.after(0, lambda: self._on_generation_finished(success=True))

        def on_error(message: str):
            def handler():
                self._on_generation_finished(success=False)
                messagebox.showerror("LLM Error", f"An error occurred:\n{message}")
            self.parent.after(0, handler)

        self.current_thread = logic.stream_llm_response(
            model=model,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            base_url=base_url,
            on_chunk=on_chunk,
            on_done=on_done,
            on_error=on_error,
        )

    def _on_generation_finished(self, success: bool):
        self._set_streaming(False)
        if success:
            set_status(self.status_var, "Generation complete.")
        else:
            set_status(self.status_var, "Generation failed.")

    def _on_stop_clicked(self):
        # We can't cleanly cancel HTTP streaming without more complex plumbing,
        # but we can at least mark the UI as idle and ignore further chunks.
        self._set_streaming(False)
        set_status(self.status_var, "Stop requested (stream may finish in background).")

    def _set_streaming(self, is_streaming: bool):
        self.streaming = is_streaming
        state_generate = "disabled" if is_streaming else "normal"
        state_stop = "normal" if is_streaming else "disabled"
        self.generate_btn.config(state=state_generate)
        self.stop_btn.config(state=state_stop)

    def _clear_output(self):
        self.output_text.delete("1.0", tk.END)
        set_status(self.status_var, "Output cleared.")

    def _save_output_as(self):
        content = self.output_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showinfo("No content", "Nothing to save.")
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
            title="Save Assistant Output As",
        )
        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            set_status(self.status_var, f"Saved output to: {path}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save file:\n{e}")

    def _save_llm_settings(self):
        settings = logic.LLMSettings(
            base_url=self.base_url_var.get().strip(),
            model=self.model_var.get().strip(),
            temperature=float(self.temperature_var.get()),
            enabled=bool(self.ai_enabled_var.get()),
        )
        try:
            logic.save_local_llm_settings(settings)
            set_status(self.status_var, "LLM settings saved.")
        except Exception as e:
            messagebox.showerror("Settings Error", f"Failed to save settings:\n{e}")
        self._refresh_ai_status()

    def _toggle_ai_enabled(self):
        if not self.ai_enabled_var.get():
            set_status(self.status_var, "AI disabled.")
        else:
            set_status(self.status_var, "AI enabled.")
        self._refresh_ai_status()

    def _check_llm(self):
        base_url = self.base_url_var.get().strip()
        if not self.ai_enabled_var.get():
            messagebox.showwarning("AI Disabled", "Enable AI to check the LLM connection.")
            set_status(self.status_var, "AI disabled.")
            return
        if logic.check_llm_available(base_url):
            set_status(self.status_var, "LLM reachable.")
            messagebox.showinfo("LLM Check", "LLM endpoint is reachable and responding.")
        else:
            set_status(self.status_var, "LLM unreachable.")
            messagebox.showerror(
                "LLM Check",
                "LLM endpoint is not reachable.\nMake sure your LLM server is running and the API Endpoint is correct.",
            )
        self._refresh_ai_status()

    def _refresh_ai_status(self):
        def worker():
            enabled = self.ai_enabled_var.get()
            if not enabled:
                status_text = "AI status: disabled"
            else:
                reachable = logic.check_llm_available(self.base_url_var.get().strip())
                status_text = "AI status: reachable" if reachable else "AI status: unavailable"

            def finish():
                self.ai_status_var.set(status_text)
            self.parent.after(0, finish)

        threading.Thread(target=worker, daemon=True).start()

    def _show_quick_start(self):
        messagebox.showinfo(
            "Quick Start - LLM Assistant",
            "🚀 Getting Started:\n\n"
            "1) Start your LLM server (local or cloud)\n"
            "2) Configure API Endpoint and Model name\n"
            "3) Enable 'AI Enabled' checkbox\n"
            "4) Click 'Check LLM' to verify connection\n"
            "5) Enter a prompt and click 'Send to Assistant'\n\n"
            "💡 Note: If AI is disabled, Ship Studio will use\n"
            "manual templates for documentation generation.\n\n"
            "Supported: Ollama, OpenAI API, custom endpoints",
        )


def build_ui(parent, status_var=None):
    """
    Entry point for the module system.
    """
    return LLMAssistantUI(parent, status_var=status_var)

