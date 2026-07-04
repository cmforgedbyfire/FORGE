"""
FORGE Progress Indicator System

Thread-safe progress bars and indicators for long-running operations.
"""

import tkinter as tk
from tkinter import ttk
import threading
from typing import Optional, Callable, Any
from dataclasses import dataclass
from datetime import datetime

from core.utils.logging import get_logger
from core.ui.modern_theme import ModernTheme

logger = get_logger(__name__)


@dataclass
class ProgressState:
    """State of a progress operation."""
    total: int = 100
    current: int = 0
    message: str = ""
    is_indeterminate: bool = False
    is_cancelled: bool = False
    start_time: Optional[datetime] = None


class ProgressDialog:
    """
    Modal progress dialog with cancellation support.
    """
    
    def __init__(self, parent: Optional[tk.Tk], title: str = "Working...",
                 message: str = "Please wait...", can_cancel: bool = True):
        """
        Create progress dialog.
        
        Args:
            parent: Parent window
            title: Dialog title
            message: Initial message
            can_cancel: Whether user can cancel
        """
        self.parent = parent
        self.can_cancel = can_cancel
        self.state = ProgressState(start_time=datetime.now())
        
        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.transient(parent)
        self.dialog.resizable(False, False)
        self.dialog.configure(bg=ModernTheme.BG_PRIMARY)
        
        # Center on parent
        if parent:
            self.dialog.geometry(f"+{parent.winfo_x() + 50}+{parent.winfo_y() + 50}")
        
        # Message label
        self.message_var = tk.StringVar(value=message)
        message_label = ttk.Label(self.dialog, textvariable=self.message_var,
                                 padding=10, wraplength=400)
        message_label.pack(fill="x")
        
        # Progress bar
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            self.dialog,
            mode="indeterminate",
            variable=self.progress_var,
            length=400
        )
        self.progress_bar.pack(fill="x", padx=10, pady=(0, 10))
        
        # Details label (for percentage/time)
        self.details_var = tk.StringVar(value="")
        details_label = ttk.Label(self.dialog, textvariable=self.details_var, style="Muted.TLabel")
        details_label.pack(fill="x", padx=10)
        
        # Cancel button
        if can_cancel:
            btn_frame = ttk.Frame(self.dialog)
            btn_frame.pack(fill="x", padx=10, pady=(0, 10))
            
            self.cancel_btn = ttk.Button(
                btn_frame,
                text="Cancel",
                command=self._on_cancel
            )
            self.cancel_btn.pack(side="right")
        
        # Prevent closing via X button unless can_cancel
        if can_cancel:
            self.dialog.protocol("WM_DELETE_WINDOW", self._on_cancel)
        else:
            self.dialog.protocol("WM_DELETE_WINDOW", lambda: None)
        
        # Start indeterminate animation
        self.progress_bar.start(10)
        
        logger.debug(f"Progress dialog created: {title}")
    
    def update(self, current: Optional[int] = None, total: Optional[int] = None,
              message: Optional[str] = None):
        """
        Update progress.
        
        Args:
            current: Current progress value
            total: Total progress value
            message: Progress message
        """
        if total is not None:
            self.state.total = total
            self.state.is_indeterminate = False
            self.progress_bar.config(mode="determinate", maximum=total)
            self.progress_bar.stop()
        
        if current is not None:
            self.state.current = current
            self.progress_var.set(current)
        
        if message is not None:
            self.state.message = message
            self.message_var.set(message)
        
        # Update details (percentage and time)
        if not self.state.is_indeterminate and self.state.start_time:
            percentage = (self.state.current / self.state.total * 100) if self.state.total > 0 else 0
            elapsed = (datetime.now() - self.state.start_time).total_seconds()
            
            details = f"{percentage:.1f}% complete"
            if elapsed > 2 and self.state.current > 0:
                # Estimate remaining time
                rate = self.state.current / elapsed
                remaining = (self.state.total - self.state.current) / rate if rate > 0 else 0
                if remaining > 1:
                    details += f" • ~{remaining:.0f}s remaining"
            
            self.details_var.set(details)
        
        self.dialog.update_idletasks()
    
    def set_indeterminate(self, message: Optional[str] = None):
        """
        Set progress to indeterminate mode.
        
        Args:
            message: Optional message to display
        """
        self.state.is_indeterminate = True
        self.progress_bar.config(mode="indeterminate")
        self.progress_bar.start(10)
        
        if message:
            self.message_var.set(message)
        
        self.details_var.set("")
        self.dialog.update_idletasks()
    
    def is_cancelled(self) -> bool:
        """Check if operation was cancelled."""
        return self.state.is_cancelled
    
    def _on_cancel(self):
        """Handle cancel button click."""
        if self.can_cancel:
            self.state.is_cancelled = True
            self.message_var.set("Cancelling...")
            if hasattr(self, 'cancel_btn'):
                self.cancel_btn.config(state="disabled")
            logger.info("Progress operation cancelled by user")
    
    def close(self):
        """Close the progress dialog."""
        try:
            self.dialog.destroy()
        except:
            pass
        logger.debug("Progress dialog closed")


class ProgressBar:
    """
    Inline progress bar widget for embedding in existing UIs.
    """
    
    def __init__(self, parent: tk.Widget, width: int = 400):
        """
        Create progress bar.
        
        Args:
            parent: Parent widget
            width: Width in pixels
        """
        self.parent = parent
        self.state = ProgressState()
        
        # Container frame
        self.frame = ttk.Frame(parent)
        
        # Message label
        self.message_var = tk.StringVar(value="")
        self.message_label = ttk.Label(self.frame, textvariable=self.message_var)
        self.message_label.pack(fill="x", pady=(0, 5))
        
        # Progress bar
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            self.frame,
            mode="indeterminate",
            variable=self.progress_var,
            length=width
        )
        self.progress_bar.pack(fill="x")
        
        # Initially hidden
        self.frame.pack_forget()
        self.is_visible = False
    
    def show(self, message: str = "Working..."):
        """Show progress bar with message."""
        if not self.is_visible:
            self.frame.pack(fill="x", pady=5)
            self.is_visible = True
        
        self.message_var.set(message)
        self.progress_bar.start(10)
        self.state = ProgressState(start_time=datetime.now(), is_indeterminate=True)
    
    def update(self, current: int, total: int, message: Optional[str] = None):
        """Update progress."""
        if not self.is_visible:
            self.show(message or "Working...")
        
        self.state.total = total
        self.state.current = current
        self.state.is_indeterminate = False
        
        self.progress_bar.stop()
        self.progress_bar.config(mode="determinate", maximum=total)
        self.progress_var.set(current)
        
        if message:
            self.message_var.set(message)
    
    def hide(self):
        """Hide progress bar."""
        if self.is_visible:
            self.progress_bar.stop()
            self.frame.pack_forget()
            self.is_visible = False


class ThreadedOperation:
    """
    Execute long-running operation in thread with progress dialog.
    """
    
    def __init__(self, parent: Any, title: str = "Working...",
                 can_cancel: bool = True):
        """
        Create threaded operation.
        
        Args:
            parent: Parent window
            title: Progress dialog title
            can_cancel: Whether operation can be cancelled
        """
        self.parent = parent
        self.title = title
        self.can_cancel = can_cancel
        self.progress_dialog: Optional[ProgressDialog] = None
        self.worker_thread: Optional[threading.Thread] = None
        self.result = None
        self.exception = None
    
    def run(self, worker_func: Callable, on_complete: Optional[Callable] = None,
           on_error: Optional[Callable[[Exception], None]] = None) -> None:
        """
        Run operation in background thread with progress dialog.
        
        Args:
            worker_func: Function to run (receives progress_callback)
            on_complete: Callback when complete (receives result)
            on_error: Callback on error (receives exception)
        """
        # Create progress dialog
        self.progress_dialog = ProgressDialog(
            self.parent,
            title=self.title,
            can_cancel=self.can_cancel
        )
        
        def worker():
            """Worker thread function."""
            try:
                # Create progress callback
                def progress_callback(current: Optional[int] = None,
                                    total: Optional[int] = None,
                                    message: Optional[str] = None):
                    """Callback for worker to report progress."""
                    if self.progress_dialog is not None and self.parent is not None:
                        dialog = self.progress_dialog
                        self.parent.after(0, lambda: dialog.update(
                            current, total, message
                        ))
                    
                    # Check for cancellation
                    if self.progress_dialog and self.progress_dialog.is_cancelled():
                        raise InterruptedError("Operation cancelled by user")
                
                # Execute worker function
                self.result = worker_func(progress_callback)
                
                # Call completion callback
                if on_complete is not None and self.parent is not None:
                    callback = on_complete
                    result = self.result
                    self.parent.after(0, lambda: callback(result))
                
            except Exception as exc:
                self.exception = exc
                logger.error(f"Threaded operation failed: {exc}", exc_info=True)
                
                if on_error is not None and self.parent is not None:
                    error_callback = on_error
                    error = exc
                    self.parent.after(0, lambda: error_callback(error))
            
            finally:
                # Close progress dialog
                if self.progress_dialog and self.parent:
                    self.parent.after(0, self.progress_dialog.close)
        
        # Start worker thread
        self.worker_thread = threading.Thread(target=worker, daemon=True)
        self.worker_thread.start()
        
        logger.info(f"Started threaded operation: {self.title}")


# Convenience function
def run_with_progress(parent: tk.Tk, title: str, worker_func: Callable,
                     on_complete: Optional[Callable] = None,
                     on_error: Optional[Callable[[Exception], None]] = None,
                     can_cancel: bool = True) -> ThreadedOperation:
    """
    Convenience function to run operation with progress dialog.
    
    Args:
        parent: Parent window
        title: Progress dialog title
        worker_func: Worker function (receives progress_callback)
        on_complete: Completion callback
        on_error: Error callback
        can_cancel: Whether operation can be cancelled
    
    Returns:
        ThreadedOperation instance
    
    Example:
        def my_task(progress):
            for i in range(100):
                progress(i, 100, f"Processing {i}/100")
                time.sleep(0.1)
            return "Done!"
        
        def on_done(result):
            print(f"Result: {result}")
        
        run_with_progress(root, "Processing", my_task, on_done)
    """
    operation = ThreadedOperation(parent, title, can_cancel)
    operation.run(worker_func, on_complete, on_error)
    return operation
