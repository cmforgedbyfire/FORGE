"""
Ship Studio Recent Projects System

Track and provide quick access to recently used project paths.
"""

import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

from core.utils.logging import get_logger

logger = get_logger(__name__)

# Recent projects file
RECENT_PROJECTS_FILE = Path.home() / ".ship_studio" / "recent_projects.json"
MAX_RECENT_PROJECTS = 20


@dataclass
class RecentProject:
    """Information about a recently used project."""
    path: str
    name: str
    last_used: str  # ISO format datetime
    use_count: int = 1
    project_type: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'RecentProject':
        """Create from dictionary."""
        return cls(**data)


class RecentProjectsManager:
    """Manage recent projects list."""
    
    def __init__(self):
        """Initialize manager."""
        self.projects: List[RecentProject] = []
        self._load()
    
    def _load(self) -> None:
        """Load recent projects from file."""
        if not RECENT_PROJECTS_FILE.exists():
            logger.debug("No recent projects file found")
            return
        
        try:
            data = json.loads(RECENT_PROJECTS_FILE.read_text(encoding="utf-8"))
            self.projects = [RecentProject.from_dict(p) for p in data.get("projects", [])]
            logger.info(f"Loaded {len(self.projects)} recent projects")
        except Exception as e:
            logger.error(f"Failed to load recent projects: {e}")
            self.projects = []
    
    def _save(self) -> None:
        """Save recent projects to file."""
        try:
            RECENT_PROJECTS_FILE.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "version": "1.0",
                "projects": [p.to_dict() for p in self.projects]
            }
            RECENT_PROJECTS_FILE.write_text(
                json.dumps(data, indent=2),
                encoding="utf-8"
            )
            logger.debug(f"Saved {len(self.projects)} recent projects")
        except Exception as e:
            logger.error(f"Failed to save recent projects: {e}")
    
    def add(self, path: str, project_type: Optional[str] = None) -> None:
        """
        Add or update a project in recent list.
        
        Args:
            path: Project path
            project_type: Type of project (optional)
        """
        path_obj = Path(path).resolve()
        path_str = str(path_obj)
        
        # Check if project already exists
        existing = None
        for p in self.projects:
            if Path(p.path).resolve() == path_obj:
                existing = p
                break
        
        if existing:
            # Update existing
            existing.last_used = datetime.now().isoformat()
            existing.use_count += 1
            if project_type:
                existing.project_type = project_type
            logger.debug(f"Updated recent project: {path_str} (uses: {existing.use_count})")
        else:
            # Add new
            project = RecentProject(
                path=path_str,
                name=path_obj.name,
                last_used=datetime.now().isoformat(),
                use_count=1,
                project_type=project_type
            )
            self.projects.insert(0, project)
            logger.info(f"Added recent project: {path_str}")
        
        # Re-sort by last used
        self.projects.sort(key=lambda p: p.last_used, reverse=True)
        
        # Limit to max
        if len(self.projects) > MAX_RECENT_PROJECTS:
            removed = self.projects[MAX_RECENT_PROJECTS:]
            self.projects = self.projects[:MAX_RECENT_PROJECTS]
            logger.debug(f"Trimmed {len(removed)} old projects from recent list")
        
        self._save()
    
    def remove(self, path: str) -> bool:
        """
        Remove a project from recent list.
        
        Args:
            path: Project path to remove
        
        Returns:
            True if removed, False if not found
        """
        path_obj = Path(path).resolve()
        
        for i, p in enumerate(self.projects):
            if Path(p.path).resolve() == path_obj:
                removed = self.projects.pop(i)
                logger.info(f"Removed recent project: {removed.path}")
                self._save()
                return True
        
        return False
    
    def clear(self) -> None:
        """Clear all recent projects."""
        count = len(self.projects)
        self.projects = []
        self._save()
        logger.info(f"Cleared {count} recent projects")
    
    def get_all(self, limit: Optional[int] = None) -> List[RecentProject]:
        """
        Get all recent projects.
        
        Args:
            limit: Maximum number to return (optional)
        
        Returns:
            List of recent projects, sorted by last used
        """
        if limit:
            return self.projects[:limit]
        return self.projects.copy()
    
    def get_valid_projects(self, limit: Optional[int] = None) -> List[RecentProject]:
        """
        Get recent projects that still exist on disk.
        
        Args:
            limit: Maximum number to return (optional)
        
        Returns:
            List of valid recent projects
        """
        valid = [p for p in self.projects if Path(p.path).exists()]
        
        # Remove invalid projects
        if len(valid) < len(self.projects):
            invalid_count = len(self.projects) - len(valid)
            self.projects = valid
            self._save()
            logger.info(f"Removed {invalid_count} invalid recent projects")
        
        if limit:
            return valid[:limit]
        return valid
    
    def search(self, query: str) -> List[RecentProject]:
        """
        Search recent projects by name or path.
        
        Args:
            query: Search query
        
        Returns:
            List of matching projects
        """
        query_lower = query.lower()
        matches = [
            p for p in self.projects
            if query_lower in p.name.lower() or query_lower in p.path.lower()
        ]
        logger.debug(f"Search '{query}' found {len(matches)} projects")
        return matches
    
    def get_by_type(self, project_type: str) -> List[RecentProject]:
        """
        Get recent projects of a specific type.
        
        Args:
            project_type: Project type to filter by
        
        Returns:
            List of matching projects
        """
        return [p for p in self.projects if p.project_type == project_type]
    
    def get_stats(self) -> dict:
        """
        Get statistics about recent projects.
        
        Returns:
            Dictionary with stats
        """
        total = len(self.projects)
        valid = len([p for p in self.projects if Path(p.path).exists()])
        
        types = {}
        for p in self.projects:
            if p.project_type:
                types[p.project_type] = types.get(p.project_type, 0) + 1
        
        most_used = max(self.projects, key=lambda p: p.use_count) if self.projects else None
        
        return {
            "total": total,
            "valid": valid,
            "invalid": total - valid,
            "types": types,
            "most_used": {
                "name": most_used.name,
                "path": most_used.path,
                "count": most_used.use_count
            } if most_used else None
        }


# Global instance
_manager: Optional[RecentProjectsManager] = None


def get_manager() -> RecentProjectsManager:
    """Get global recent projects manager instance."""
    global _manager
    if _manager is None:
        _manager = RecentProjectsManager()
    return _manager


# Convenience functions
def add_recent_project(path: str, project_type: Optional[str] = None) -> None:
    """Add project to recent list."""
    get_manager().add(path, project_type)


def get_recent_projects(limit: int = 10, valid_only: bool = True) -> List[RecentProject]:
    """
    Get recent projects.
    
    Args:
        limit: Maximum number to return
        valid_only: Only return projects that exist
    
    Returns:
        List of recent projects
    """
    manager = get_manager()
    if valid_only:
        return manager.get_valid_projects(limit)
    return manager.get_all(limit)


def remove_recent_project(path: str) -> bool:
    """Remove project from recent list."""
    return get_manager().remove(path)


def clear_recent_projects() -> None:
    """Clear all recent projects."""
    get_manager().clear()


def search_recent_projects(query: str) -> List[RecentProject]:
    """Search recent projects."""
    return get_manager().search(query)
