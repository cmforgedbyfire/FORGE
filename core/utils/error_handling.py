"""
Error handling utilities for FORGE.
"""

import tkinter as tk
from tkinter import messagebox
import traceback
import logging

logger = logging.getLogger(__name__)


def show_error_dialog(title: str, message: str, detail: str = None):
    """Show a user-friendly error dialog."""
    if detail:
        messagebox.showerror(title, f"{message}\n\nDetails: {detail}")
    else:
        messagebox.showerror(title, message)


def handle_operation_error(operation_name: str, error: Exception, show_dialog: bool = True):
    """Handle errors from operations with consistent logging and user feedback."""
    error_msg = f"Error in {operation_name}: {str(error)}"
    logger.error(error_msg, exc_info=True)
    
    if show_dialog:
        show_error_dialog(
            f"FORGE - {operation_name} Error",
            f"An error occurred during {operation_name}.",
            str(error)
        )


def safe_execute(func, operation_name: str, default_return=None, show_errors: bool = True):
    """Execute a function safely with error handling."""
    try:
        return func()
    except Exception as e:
        handle_operation_error(operation_name, e, show_errors)
        return default_return


def setup_global_exception_handler(root: tk.Tk):
    """Setup global exception handler for uncaught exceptions."""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            return
        
        error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logger.error(f"Uncaught exception: {error_msg}")
        
        messagebox.showerror(
            "FORGE - Unexpected Error",
            "An unexpected error occurred. Please check the logs for details.\n\n"
            f"Error: {exc_value}"
        )
    
    import sys
    sys.excepthook = handle_exception
