import tkinter as tk
from tkinter import ttk

from core.config.settings import APP_DISPLAY_NAME, VERSION
from core.config.user_settings import load_llm_settings
from core.config.preferences import preferences
from core.ui.tab_manager import TabManager
from core.ui.modern_theme import configure_modern_style, ModernTheme
from core.utils.logging import get_logger, setup_logging
from core.utils.errors import setup_global_exception_handler
# from core.utils.shortcuts import setup_default_shortcuts

logger = get_logger(__name__)


class ShipStudioApp:
    def __init__(self):
        # Setup logging first
        setup_logging(console=False)
        logger.info("="*60)
        logger.info(f"Ship Studio {VERSION} - Application Starting")
        logger.info("="*60)
        
        self.root = tk.Tk()
        self.root.title(f"{APP_DISPLAY_NAME} v{VERSION}")
        
        # Restore window state from preferences
        ws = preferences.preferences.window_state
        self.root.geometry(f"{ws.width}x{ws.height}+{ws.x}+{ws.y}")
        self.root.minsize(900, 600)
        
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
        
        logger.info("Ship Studio initialized successfully")

    def _on_closing(self):
        """Handle window closing - save state and cleanup."""
        try:
            # Save window geometry
            geometry = self.root.geometry()
            width, height, x, y = self._parse_geometry(geometry)
            maximized = self.root.state() == 'zoomed'
            
            preferences.update_window_state(width, height, x, y, maximized)
            
            logger.info("Ship Studio closing - state saved")
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
        self.root.configure(bg=ModernTheme.BG_SECONDARY)

    def _build_layout(self):
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Status bar at bottom
        self.status_var = tk.StringVar(value="Ready")
        self.ai_mode_var = tk.StringVar(value="")
        
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill="x", side="bottom")
        
        status_label = ttk.Label(status_frame, textvariable=self.status_var, anchor="w")
        status_label.pack(side="left", fill="x", expand=True, padx=8, pady=4)
        
        # AI mode indicator
        ai_mode_label = ttk.Label(status_frame, textvariable=self.ai_mode_var, anchor="e")
        ai_mode_label.pack(side="right", padx=8, pady=4)
        
        self._update_ai_mode_indicator()

        # Tab manager
        self.tab_manager = TabManager(self.main_frame, status_var=self.status_var)
        
        # Update AI status periodically
        self._update_ai_mode_indicator()
        self.root.after(5000, self._schedule_ai_update)  # Check every 5 seconds
    
    def _update_ai_mode_indicator(self):
        """Update the AI mode indicator."""
        try:
            ai_settings = load_llm_settings()
            ai_status_text = "AI: Enabled" if ai_settings.enabled else "AI: Disabled"
            self.ai_status_label.config(text=ai_status_text)
        except Exception as e:
            logger.warning(f"Could not update AI status: {e}")
    
    def _schedule_ai_update(self):
        """Schedule periodic AI status updates."""
        self._update_ai_mode_indicator()
        self.root.after(5000, self._schedule_ai_update)
    
    def _update_ai_mode_indicator(self):
        """Update AI mode indicator in status bar"""
        settings = load_llm_settings()
        if settings.enabled:
            self.ai_mode_var.set("🤖 AI: Enabled")
        else:
            self.ai_mode_var.set("📝 AI: Disabled (Template Mode)")
        
        # Refresh every 5 seconds
        self.root.after(5000, self._update_ai_mode_indicator)

    def run(self):
        logger.info("Starting Ship Studio main loop")
        try:
            self.root.mainloop()
        finally:
            logger.info("Ship Studio application closed")
            logger.info("="*60)
