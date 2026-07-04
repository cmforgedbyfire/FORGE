"""
Configuration persistence for FORGE.
Save and restore user preferences, window state, and recent files.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass, asdict

from core.utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class WindowState:
    """Window geometry and state."""
    width: int = 1033
    height: int = 608
    x: int = 100
    y: int = 100
    maximized: bool = False


@dataclass
class AppPreferences:
    """Application preferences."""
    last_screenshot_dir: str = ""
    last_project_dir: str = ""
    default_project_type: str = "auto"
    recent_projects: List[str] = None
    recent_screenshots: List[str] = None
    window_state: WindowState = None
    
    def __post_init__(self):
        if self.recent_projects is None:
            self.recent_projects = []
        if self.recent_screenshots is None:
            self.recent_screenshots = []
        if self.window_state is None:
            self.window_state = WindowState()


class PreferencesManager:
    """Manage application preferences persistence."""
    
    def __init__(self):
        self.config_dir = Path.home() / ".forge"
        self.config_file = self.config_dir / "preferences.json"
        self.preferences = AppPreferences()
        
        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)
        
        # Load existing preferences
        self.load()
    
    def load(self) -> None:
        """Load preferences from disk."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Handle window state
                if 'window_state' in data:
                    data['window_state'] = WindowState(**data['window_state'])
                
                # Update preferences with loaded data
                for key, value in data.items():
                    if hasattr(self.preferences, key):
                        setattr(self.preferences, key, value)
                        
                logger.info("Loaded preferences from disk")
        except Exception as e:
            logger.error(f"Failed to load preferences: {e}")
    
    def save(self) -> None:
        """Save preferences to disk."""
        try:
            # Convert to dict for JSON serialization
            data = asdict(self.preferences)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            logger.debug("Saved preferences to disk")
        except Exception as e:
            logger.error(f"Failed to save preferences: {e}")
    
    def add_recent_project(self, path: str) -> None:
        """Add a project to recent projects list."""
        path = os.path.abspath(path)
        
        # Remove if already exists
        if path in self.preferences.recent_projects:
            self.preferences.recent_projects.remove(path)
        
        # Add to front of list
        self.preferences.recent_projects.insert(0, path)
        
        # Keep only last 10
        self.preferences.recent_projects = self.preferences.recent_projects[:10]
        
        # Save immediately
        self.save()
    
    def add_recent_screenshot(self, path: str) -> None:
        """Add a screenshot to recent screenshots list."""
        path = os.path.abspath(path)
        
        if path in self.preferences.recent_screenshots:
            self.preferences.recent_screenshots.remove(path)
        
        self.preferences.recent_screenshots.insert(0, path)
        self.preferences.recent_screenshots = self.preferences.recent_screenshots[:20]
        
        self.save()
    
    def get_recent_projects(self) -> List[str]:
        """Get list of recent projects that still exist."""
        valid_projects = []
        for path in self.preferences.recent_projects:
            if os.path.exists(path):
                valid_projects.append(path)
        
        # Update list to remove non-existent paths
        if len(valid_projects) != len(self.preferences.recent_projects):
            self.preferences.recent_projects = valid_projects
            self.save()
        
        return valid_projects
    
    def update_window_state(self, width: int, height: int, x: int, y: int, maximized: bool = False) -> None:
        """Update window state."""
        self.preferences.window_state.width = width
        self.preferences.window_state.height = height
        self.preferences.window_state.x = x
        self.preferences.window_state.y = y
        self.preferences.window_state.maximized = maximized
        self.save()


# Global instance
preferences = PreferencesManager()
