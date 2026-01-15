"""
Enhanced helpers with input validation and user experience improvements.
"""

import os
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from typing import Optional


def ensure_dir(path: str) -> None:
    """Create directory if it doesn't exist."""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise OSError(f"Failed to create directory {path}: {e}")


def set_status(status_var: Optional[tk.StringVar], message: str) -> None:
    """Set status message with validation."""
    if status_var and isinstance(status_var, tk.StringVar):
        try:
            # Limit status message length
            if len(message) > 80:
                message = message[:77] + "..."
            status_var.set(message)
        except Exception:
            pass  # Silently fail if status update fails


def validate_file_path(path: str, must_exist: bool = True) -> bool:
    """Validate file path with user feedback."""
    if not path or not path.strip():
        messagebox.showerror("Validation Error", "Please provide a file path.")
        return False
    
    path = path.strip()
    
    if must_exist and not os.path.exists(path):
        messagebox.showerror("File Not Found", f"The specified path does not exist:\n{path}")
        return False
    
    if must_exist and not os.path.isfile(path):
        messagebox.showerror("Invalid File", f"The specified path is not a file:\n{path}")
        return False
    
    return True


def validate_directory_path(path: str, must_exist: bool = True, create_if_missing: bool = False) -> bool:
    """Validate directory path with optional creation."""
    if not path or not path.strip():
        messagebox.showerror("Validation Error", "Please provide a directory path.")
        return False
    
    path = path.strip()
    
    if not os.path.exists(path):
        if create_if_missing:
            try:
                ensure_dir(path)
                return True
            except Exception as e:
                messagebox.showerror("Directory Creation Failed", str(e))
                return False
        elif must_exist:
            messagebox.showerror("Directory Not Found", f"The specified directory does not exist:\n{path}")
            return False
    
    if os.path.exists(path) and not os.path.isdir(path):
        messagebox.showerror("Invalid Directory", f"The specified path is not a directory:\n{path}")
        return False
    
    return True


def show_operation_complete(operation: str, details: str = None) -> None:
    """Show operation completion message."""
    if details:
        messagebox.showinfo(f"{operation} Complete", f"{operation} completed successfully.\n\n{details}")
    else:
        messagebox.showinfo(f"{operation} Complete", f"{operation} completed successfully.")


def confirm_operation(operation: str, details: str = None) -> bool:
    """Ask user confirmation for operation."""
    message = f"Are you sure you want to {operation}?"
    if details:
        message += f"\n\n{details}"
    
    return messagebox.askyesno("Confirm Operation", message)


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes/1024:.1f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes/(1024**2):.1f} MB"
    else:
        return f"{size_bytes/(1024**3):.1f} GB"


def get_file_info(path: str) -> dict:
    """Get detailed file information."""
    try:
        stat = os.stat(path)
        return {
            "size": stat.st_size,
            "size_formatted": format_file_size(stat.st_size),
            "modified": stat.st_mtime,
            "name": os.path.basename(path),
            "directory": os.path.dirname(path),
            "extension": os.path.splitext(path)[1].lower()
        }
    except Exception as e:
        return {"error": str(e)}


def truncate_path(path: str, max_length: int = 50) -> str:
    """Truncate long paths for display."""
    if len(path) <= max_length:
        return path
    
    # Show beginning and end of path
    if max_length > 10:
        start_len = (max_length - 3) // 2
        end_len = max_length - 3 - start_len
        return f"{path[:start_len]}...{path[-end_len:]}"
    else:
        return path[:max_length-3] + "..."