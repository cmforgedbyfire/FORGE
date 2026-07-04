"""
FORGE Error Handling Framework

Centralized exception handling, user-friendly error dialogs, and error reporting.
"""

import tkinter as tk
from tkinter import messagebox
import traceback
from typing import Optional, Callable, Any
from pathlib import Path
import sys

from core.utils.logging import get_logger, log_exception

logger = get_logger(__name__)


# Custom exception classes
class ForgeError(Exception):
    """Base exception for FORGE-specific errors."""
    
    def __init__(self, message: str, details: Optional[str] = None, recoverable: bool = True):
        self.message = message
        self.details = details
        self.recoverable = recoverable
        super().__init__(message)
    
    def get_user_message(self) -> str:
        """Get formatted message for user display."""
        if self.details:
            return f"{self.message}\n\nDetails: {self.details}"
        return self.message


class ProjectError(ForgeError):
    """Errors related to project operations."""
    pass


class BuildError(ForgeError):
    """Errors during build operations."""
    pass


class LLMError(ForgeError):
    """Errors related to LLM operations."""
    pass


class ValidationError(ForgeError):
    """Input validation errors."""
    pass


class FileOperationError(ForgeError):
    """File system operation errors."""
    pass


# Error dialog functions
def show_error(title: str, message: str, details: Optional[str] = None, 
               parent: Any = None) -> None:
    """
    Show error dialog to user.
    
    Args:
        title: Dialog title
        message: Main error message
        details: Additional details (optional)
        parent: Parent window (optional)
    """
    logger.error(f"{title}: {message}")
    if details:
        logger.debug(f"Error details: {details}")
    
    full_message = f"{message}\n\n{details}" if details else message
    messagebox.showerror(title, full_message, parent=parent)


def show_warning(title: str, message: str, parent: Any = None) -> None:
    """Show warning dialog to user."""
    logger.warning(f"{title}: {message}")
    messagebox.showwarning(title, message, parent=parent)


def show_info(title: str, message: str, parent: Any = None) -> None:
    """Show info dialog to user."""
    logger.info(f"{title}: {message}")
    messagebox.showinfo(title, message, parent=parent)


def show_exception(exc: Exception, context: str = "An error occurred", 
                  parent: Any = None) -> None:
    """
    Show exception in user-friendly dialog.
    
    Args:
        exc: Exception to display
        context: Context message
        parent: Parent window (optional)
    """
    if isinstance(exc, ForgeError):
        # Custom FORGE exception with user-friendly message
        show_error(
            context,
            exc.get_user_message(),
            parent=parent
        )
    else:
        # Generic exception
        show_error(
            context,
            str(exc),
            details=f"Type: {type(exc).__name__}",
            parent=parent
        )
    
    log_exception(logger, context, exc)


def ask_yes_no(title: str, message: str, parent: Optional[tk.Tk] = None) -> bool:
    """
    Ask user yes/no question.
    
    Returns:
        True if yes, False if no
    """
    if parent is not None:
        result = messagebox.askyesno(title, message, parent=parent)
    else:
        result = messagebox.askyesno(title, message)
    logger.info(f"User prompt '{title}': {'Yes' if result else 'No'}")
    return result


def ask_ok_cancel(title: str, message: str, parent: Optional[tk.Tk] = None) -> bool:
    """
    Ask user OK/Cancel question.
    
    Returns:
        True if OK, False if Cancel
    """
    if parent is not None:
        result = messagebox.askokcancel(title, message, parent=parent)
    else:
        result = messagebox.askokcancel(title, message)
    logger.info(f"User prompt '{title}': {'OK' if result else 'Cancel'}")
    return result


# Error handling decorators
def handle_errors(context: str, show_dialog: bool = True, 
                 reraise: bool = False, default_return: Any = None):
    """
    Decorator to handle errors in functions.
    
    Args:
        context: Context message for error
        show_dialog: Whether to show error dialog
        reraise: Whether to re-raise exception after handling
        default_return: Value to return on error (if not re-raising)
    
    Example:
        @handle_errors("Failed to load project")
        def load_project(path):
            ...
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                log_exception(logger, f"{context} in {func.__name__}", exc)
                
                if show_dialog:
                    show_exception(exc, context)
                
                if reraise:
                    raise
                
                return default_return
        
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        return wrapper
    
    return decorator


def safe_execute(func: Callable, *args, context: str = "Operation failed",
                show_dialog: bool = True, **kwargs) -> tuple[bool, Any]:
    """
    Safely execute a function with error handling.
    
    Args:
        func: Function to execute
        *args: Function arguments
        context: Context message for errors
        show_dialog: Whether to show error dialog
        **kwargs: Function keyword arguments
    
    Returns:
        Tuple of (success: bool, result: Any)
    """
    try:
        result = func(*args, **kwargs)
        return True, result
    except Exception as exc:
        log_exception(logger, context, exc)
        if show_dialog:
            show_exception(exc, context)
        return False, None


# Global exception handler for uncaught exceptions
def setup_global_exception_handler(root: Optional[tk.Tk] = None) -> None:
    """
    Setup global exception handler for uncaught exceptions.
    
    Args:
        root: Tkinter root window (optional)
    """
    def handle_exception(exc_type, exc_value, exc_traceback):
        """Handle uncaught exceptions."""
        # Ignore KeyboardInterrupt
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        # Log the exception
        logger.critical(
            "Uncaught exception",
            exc_info=(exc_type, exc_value, exc_traceback)
        )
        
        # Show error to user
        error_msg = f"An unexpected error occurred:\n\n{exc_value}"
        tb_summary = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        
        try:
            show_error(
                "Unexpected Error",
                error_msg,
                details=f"Please report this error.\n\nTraceback:\n{tb_summary[:500]}...",
                parent=root
            )
        except:
            # Fallback if dialog fails
            print(f"CRITICAL ERROR: {error_msg}", file=sys.stderr)
            print(tb_summary, file=sys.stderr)
    
    sys.excepthook = handle_exception
    logger.info("Global exception handler installed")


# Error recovery suggestions
ERROR_SUGGESTIONS = {
    FileNotFoundError: "Make sure the file or folder exists and the path is correct.",
    PermissionError: "Check file permissions. Try running FORGE as administrator.",
    ConnectionError: "Check your network connection and firewall settings.",
    TimeoutError: "The operation took too long. Try again or check your connection.",
    ValueError: "Invalid input value. Please check your settings.",
    OSError: "Operating system error. Check disk space and permissions.",
}


def get_error_suggestion(exc: Exception) -> Optional[str]:
    """
    Get helpful suggestion for an error.
    
    Args:
        exc: Exception
    
    Returns:
        Suggestion string or None
    """
    for exc_type, suggestion in ERROR_SUGGESTIONS.items():
        if isinstance(exc, exc_type):
            return suggestion
    return None


def show_error_with_suggestion(exc: Exception, context: str = "An error occurred",
                               parent: Optional[tk.Tk] = None) -> None:
    """
    Show error with helpful suggestion.
    
    Args:
        exc: Exception to display
        context: Context message
        parent: Parent window (optional)
    """
    suggestion = get_error_suggestion(exc)
    details = str(exc)
    
    if suggestion:
        details = f"{details}\n\n💡 Suggestion: {suggestion}"
    
    show_error(context, type(exc).__name__, details=details, parent=parent)
    log_exception(logger, context, exc)


# Validation helpers (basic - more in validation framework)
def validate_path_exists(path: str, path_type: str = "Path") -> None:
    """
    Validate that a path exists.
    
    Args:
        path: Path to validate
        path_type: Description of path type (for error message)
    
    Raises:
        ValidationError: If path doesn't exist
    """
    if not path or not Path(path).exists():
        raise ValidationError(
            f"{path_type} does not exist",
            details=f"Path: {path}",
            recoverable=True
        )


def validate_not_empty(value: str, field_name: str = "Field") -> None:
    """
    Validate that a value is not empty.
    
    Args:
        value: Value to validate
        field_name: Name of field (for error message)
    
    Raises:
        ValidationError: If value is empty
    """
    if not value or not value.strip():
        raise ValidationError(
            f"{field_name} cannot be empty",
            recoverable=True
        )
