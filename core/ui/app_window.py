import tkinter as tk
from tkinter import ttk
from pathlib import Path

from core.config.settings import APP_DISPLAY_NAME, VERSION
from core.config.user_settings import load_llm_settings
from core.config.preferences import preferences
from core.ui.tab_manager import TabManager
from core.ui.modern_theme import configure_modern_style, ModernTheme
from core.utils.logging import get_logger, setup_logging
from core.utils.errors import setup_global_exception_handler
# from core.utils.shortcuts import setup_default_shortcuts

logger = get_logger(__name__)


class ForgeApp:
    def __init__(self):
        # Setup logging first
        setup_logging(console=False)
        logger.info("="*60)
        logger.info(f"FORGE {VERSION} - Application Starting")
        logger.info("="*60)
        
        self.root = tk.Tk()
        self.root.title(f"{APP_DISPLAY_NAME} v{VERSION}")
        self._set_window_icon()
        
        # Restore window state from preferences
        ws = preferences.preferences.window_state
        self.root.geometry(f"{ws.width}x{ws.height}+{ws.x}+{ws.y}")
        self.root.minsize(900, 560)
        
        if ws.maximized:
            self.root.state('zoomed')
        
        # Save window state on close
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Setup global exception handler
        setup_global_exception_handler(self.root)
        
        # Setup keyboard shortcuts (temporarily disabled due to tkinter keysym issues)
        # TODO: Fix keyboard shortcut implementation
        # self.shortcut_manager = setup_default_shortcuts(self.root, self)
        
        self._configure_style()
        self._build_layout()
        
        logger.info("FORGE initialized successfully")

    def _set_window_icon(self):
        """Set the source-run window icon to the FORGE brand icon."""
        icon_path = Path(__file__).resolve().parents[2] / "assets" / "forge.ico"
        if not icon_path.exists():
            logger.warning(f"FORGE icon not found: {icon_path}")
            return

        try:
            self.root.iconbitmap(str(icon_path))
        except Exception as e:
            logger.warning(f"Could not set FORGE window icon: {e}")

    def _on_closing(self):
        """Handle window closing - save state and cleanup."""
        try:
            # Save window geometry
            geometry = self.root.geometry()
            width, height, x, y = self._parse_geometry(geometry)
            maximized = self.root.state() == 'zoomed'
            
            preferences.update_window_state(width, height, x, y, maximized)
            
            logger.info("FORGE closing - state saved")
        except Exception as e:
            logger.error(f"Error saving window state: {e}")
        
        self.root.destroy()
    
    def _parse_geometry(self, geometry: str) -> tuple:
        """Parse tkinter geometry string like '1000x700+100+50'."""
        # Split by 'x' and '+'
        parts = geometry.replace('+', ' +').replace('-', ' -').split()
        width_height = parts[0].split('x')
        width = int(width_height[0])
        height = int(width_height[1])
        x = int(parts[1]) if len(parts) > 1 else 100
        y = int(parts[2]) if len(parts) > 2 else 100
        return width, height, x, y

    def _configure_style(self):
        configure_modern_style()
        
        # Configure window background
        self.root.configure(bg=ModernTheme.BG_PRIMARY)

    def _build_layout(self):
        self.status_var = tk.StringVar(value="Ready")
        self.ai_mode_var = tk.StringVar(value="")
        self.window_size_var = tk.StringVar(value="")

        # Main container
        self.main_frame = ttk.Frame(self.root, style="Surface.TFrame")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))

        # Status bar at bottom
        status_frame = ttk.Frame(self.root, style="Status.TFrame")
        status_frame.pack(fill="x", side="bottom")
        
        status_label = ttk.Label(status_frame, textvariable=self.status_var, anchor="w", style="Status.TLabel")
        status_label.pack(side="left", fill="x", expand=True, padx=10, pady=5)

        # Live window size indicator
        window_size_label = ttk.Label(status_frame, textvariable=self.window_size_var, anchor="e", style="Status.TLabel")
        window_size_label.pack(side="right", padx=10, pady=5)
        
        # AI mode indicator
        ai_mode_label = ttk.Label(status_frame, textvariable=self.ai_mode_var, anchor="e", style="Status.TLabel")
        ai_mode_label.pack(side="right", padx=10, pady=5)
        self.root.bind("<Configure>", self._update_window_size, add="+")
        self.root.after_idle(self._update_window_size)
        
        self._update_ai_mode_indicator()

        # Tab manager
        self.tab_manager = TabManager(self.main_frame, status_var=self.status_var)
        
        # Update AI status periodically
        self._update_ai_mode_indicator()
        self.root.after(5000, self._schedule_ai_update)  # Check every 5 seconds

    def _update_window_size(self, event=None):
        """Update live window dimensions in the status bar."""
        if event is not None and event.widget is not self.root:
            return
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        if width > 1 and height > 1:
            size_text = f"Window: {width} x {height}"
            self.window_size_var.set(size_text)
            self.root.title(f"{APP_DISPLAY_NAME} v{VERSION} - {width} x {height}")
    
    def _schedule_ai_update(self):
        """Schedule periodic AI status updates."""
        self._update_ai_mode_indicator()
        self.root.after(5000, self._schedule_ai_update)
    
    def _update_ai_mode_indicator(self):
        """Update AI mode indicator in status bar"""
        settings = load_llm_settings()
        if settings.enabled:
            self.ai_mode_var.set("AI: Enabled")
        else:
            self.ai_mode_var.set("AI: Disabled (Template Mode)")

    def run(self):
        logger.info("Starting FORGE main loop")
        try:
            self.root.mainloop()
        finally:
            logger.info("FORGE application closed")
            logger.info("="*60)
