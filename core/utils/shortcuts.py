"""
Ship Studio Keyboard Shortcuts System

Global keyboard shortcuts for common operations.
"""

import tkinter as tk
from typing import Dict, Callable, Optional, List
from dataclasses import dataclass

from core.utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class Shortcut:
    """Keyboard shortcut definition."""
    key: str  # e.g., "<Control-s>", "<Control-o>"
    description: str
    callback: Callable
    enabled: bool = True


class ShortcutManager:
    """Manage keyboard shortcuts for the application."""
    
    def __init__(self, root: tk.Tk):
        """
        Initialize shortcut manager.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.shortcuts: Dict[str, Shortcut] = {}
        logger.info("Shortcut manager initialized")
    
    def register(self, key: str, description: str, callback: Callable) -> None:
        """
        Register a keyboard shortcut.
        
        Args:
            key: Key combination (e.g., "<Control-s>", "<Alt-f>")
            description: Human-readable description
            callback: Function to call when shortcut is pressed
        """
        # Normalize key
        key = key.lower()
        
        # Create shortcut
        shortcut = Shortcut(key, description, callback)
        self.shortcuts[key] = shortcut
        
        # Bind to root window
        self.root.bind(key, self._make_handler(callback))
        
        logger.debug(f"Registered shortcut: {key} - {description}")
    
    def _make_handler(self, callback: Callable) -> Callable:
        """Create event handler wrapper."""
        def handler(event):
            try:
                callback()
                return "break"  # Prevent default handling
            except Exception as e:
                logger.error(f"Shortcut callback error: {e}", exc_info=True)
        return handler
    
    def unregister(self, key: str) -> bool:
        """
        Unregister a keyboard shortcut.
        
        Args:
            key: Key combination to unregister
        
        Returns:
            True if unregistered, False if not found
        """
        key = key.lower()
        
        if key in self.shortcuts:
            # Unbind
            self.root.unbind(key)
            del self.shortcuts[key]
            logger.debug(f"Unregistered shortcut: {key}")
            return True
        
        return False
    
    def enable(self, key: str) -> bool:
        """Enable a shortcut."""
        key = key.lower()
        if key in self.shortcuts:
            self.shortcuts[key].enabled = True
            return True
        return False
    
    def disable(self, key: str) -> bool:
        """Disable a shortcut."""
        key = key.lower()
        if key in self.shortcuts:
            self.shortcuts[key].enabled = False
            return True
        return False
    
    def get_all(self) -> List[Shortcut]:
        """Get all registered shortcuts."""
        return list(self.shortcuts.values())
    
    def get_help_text(self) -> str:
        """
        Get formatted help text for all shortcuts.
        
        Returns:
            Multi-line string with all shortcuts
        """
        lines = ["Keyboard Shortcuts:", ""]
        
        for shortcut in sorted(self.shortcuts.values(), key=lambda s: s.key):
            status = "" if shortcut.enabled else " (disabled)"
            key_display = shortcut.key.replace("<Control-", "Ctrl+").replace(">", "")
            key_display = key_display.replace("<Alt-", "Alt+").replace("<Shift-", "Shift+")
            lines.append(f"  {key_display:20} - {shortcut.description}{status}")
        
        return "\n".join(lines)


def setup_default_shortcuts(root: tk.Tk, app) -> ShortcutManager:
    """
    Setup default Ship Studio keyboard shortcuts.
    
    Args:
        root: Tkinter root window
        app: ForgeApp instance
    
    Returns:
        ShortcutManager instance
    """
    manager = ShortcutManager(root)
    
    # File operations
    # manager.register("<Control-n>", "New project", lambda: print("New project"))
    # manager.register("<Control-o>", "Open project", lambda: print("Open project"))
    # manager.register("<Control-s>", "Save output", lambda: print("Save"))
    
    # Tab navigation
    def next_tab():
        """Switch to next tab."""
        if hasattr(app, 'tab_manager') and hasattr(app.tab_manager, 'notebook'):
            nb = app.tab_manager.notebook
            current = nb.index(nb.select())
            nb.select((current + 1) % nb.index("end"))
    
    def prev_tab():
        """Switch to previous tab."""
        if hasattr(app, 'tab_manager') and hasattr(app.tab_manager, 'notebook'):
            nb = app.tab_manager.notebook
            current = nb.index(nb.select())
            nb.select((current - 1) % nb.index("end"))
    
    manager.register("<Control-Tab>", "Next tab", next_tab)
    manager.register("<Control-Shift-Tab>", "Previous tab", prev_tab)
    
    # Help
    def show_help():
        """Show keyboard shortcuts help."""
        from tkinter import messagebox
        messagebox.showinfo("Keyboard Shortcuts", manager.get_help_text())
    
    manager.register("<F1>", "Show help", show_help)
    
    # Refresh (for AI status, etc.)
    def refresh():
        """Refresh UI state."""
        if hasattr(app, '_update_ai_mode_indicator'):
            app._update_ai_mode_indicator()
        logger.info("UI refreshed via shortcut")
    
    manager.register("<F5>", "Refresh UI", refresh)
    
    logger.info("Default shortcuts registered")
    return manager


# Platform-specific key mappings
def get_platform_key(key: str) -> str:
    """
    Get platform-specific key name.
    
    Args:
        key: Generic key name (e.g., "Control", "Command")
    
    Returns:
        Platform-specific key name
    """
    import sys
    
    if sys.platform == "darwin":  # macOS
        return key.replace("Control", "Command")
    
    return key


# Common shortcut patterns
COMMON_SHORTCUTS = {
    "new": "<Control-n>",
    "open": "<Control-o>",
    "save": "<Control-s>",
    "save_as": "<Control-Shift-s>",
    "quit": "<Control-q>",
    "copy": "<Control-c>",
    "paste": "<Control-v>",
    "cut": "<Control-x>",
    "undo": "<Control-z>",
    "redo": "<Control-y>",
    "find": "<Control-f>",
    "replace": "<Control-h>",
    "select_all": "<Control-a>",
    "close_tab": "<Control-w>",
    "next_tab": "<Control-Tab>",
    "prev_tab": "<Control-Shift-Tab>",
    "help": "<F1>",
    "refresh": "<F5>",
}


def get_shortcut_key(action: str) -> str:
    """
    Get shortcut key for common action.
    
    Args:
        action: Action name (e.g., "save", "open")
    
    Returns:
        Shortcut key combination
    """
    return COMMON_SHORTCUTS.get(action, "")
