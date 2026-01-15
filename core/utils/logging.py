"""
Ship Studio Logging Framework

Centralized logging system with rotation, levels, and module-specific loggers.
Logs stored in ~/.ship_studio/logs/ with automatic rotation and cleanup.
"""

import logging
try:
    import logging.handlers
    RotatingFileHandler = logging.handlers.RotatingFileHandler
    TimedRotatingFileHandler = logging.handlers.TimedRotatingFileHandler
except ImportError:
    logging.handlers = None
    RotatingFileHandler = None
    TimedRotatingFileHandler = None
from pathlib import Path
from datetime import datetime
from typing import Optional
import sys

# Log directory setup
LOG_DIR = Path.home() / ".ship_studio" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Log file paths
MAIN_LOG = LOG_DIR / "ship_studio.log"
ERROR_LOG = LOG_DIR / "errors.log"
DEBUG_LOG = LOG_DIR / "debug.log"

# Log format
LOG_FORMAT = "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Root logger configured flag
_root_configured = False


def setup_logging(level: int = logging.INFO, console: bool = True) -> None:
    """
    Setup the root logger with file and console handlers.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console: Whether to also log to console
    """
    global _root_configured
    
    if _root_configured:
        return
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Capture everything, handlers filter
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    
    # Main log file (INFO and above) - rotates at 5MB, keeps 10 backups
    if RotatingFileHandler is not None:
        main_handler = RotatingFileHandler(
            MAIN_LOG,
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=10,
            encoding="utf-8"
        )
    else:
        main_handler = logging.FileHandler(MAIN_LOG, encoding="utf-8")
    main_handler.setLevel(logging.INFO)
    main_handler.setFormatter(formatter)
    root_logger.addHandler(main_handler)
    
    # Error log file (ERROR and above)
    if RotatingFileHandler is not None:
        error_handler = RotatingFileHandler(
            ERROR_LOG,
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )
    else:
        error_handler = logging.FileHandler(ERROR_LOG, encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)
    
    # Debug log file (everything) - rotates daily, keeps 7 days
    if TimedRotatingFileHandler is not None:
        debug_handler = TimedRotatingFileHandler(
            DEBUG_LOG,
            when="midnight",
            interval=1,
            backupCount=7,
            encoding="utf-8"
        )
    else:
        debug_handler = logging.FileHandler(DEBUG_LOG, encoding="utf-8")
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)
    root_logger.addHandler(debug_handler)
    
    # Console handler (optional)
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    _root_configured = True
    
    # Log startup
    root_logger.info("=" * 60)
    root_logger.info("Ship Studio Logging System Initialized")
    root_logger.info(f"Log directory: {LOG_DIR}")
    root_logger.info("=" * 60)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module.
    
    Args:
        name: Logger name (typically __name__ of the module)
    
    Returns:
        Configured logger instance
    """
    # Ensure logging is setup
    if not _root_configured:
        setup_logging()
    
    return logging.getLogger(name)


def log_exception(logger: logging.Logger, message: str, exc: Exception) -> None:
    """
    Log an exception with full traceback.
    
    Args:
        logger: Logger instance
        message: Context message
        exc: Exception to log
    """
    logger.error(f"{message}: {exc}", exc_info=True)


def log_operation_start(logger: logging.Logger, operation: str, **kwargs) -> None:
    """
    Log the start of an operation with parameters.
    
    Args:
        logger: Logger instance
        operation: Name of the operation
        **kwargs: Operation parameters to log
    """
    params = ", ".join(f"{k}={v}" for k, v in kwargs.items())
    logger.info(f"Starting operation: {operation} ({params})")


def log_operation_end(logger: logging.Logger, operation: str, success: bool, 
                      duration: Optional[float] = None, **kwargs) -> None:
    """
    Log the end of an operation with result.
    
    Args:
        logger: Logger instance
        operation: Name of the operation
        success: Whether operation succeeded
        duration: Operation duration in seconds (optional)
        **kwargs: Additional result data
    """
    status = "SUCCESS" if success else "FAILED"
    extras = ", ".join(f"{k}={v}" for k, v in kwargs.items())
    
    if duration:
        logger.info(f"Operation {status}: {operation} (duration={duration:.2f}s, {extras})")
    else:
        logger.info(f"Operation {status}: {operation} ({extras})")


def cleanup_old_logs(days: int = 30) -> int:
    """
    Remove log files older than specified days.
    
    Args:
        days: Age threshold in days
    
    Returns:
        Number of files removed
    """
    logger = get_logger(__name__)
    count = 0
    cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
    
    for log_file in LOG_DIR.glob("*.log*"):
        if log_file.stat().st_mtime < cutoff:
            try:
                log_file.unlink()
                count += 1
                logger.debug(f"Removed old log file: {log_file.name}")
            except Exception as e:
                logger.warning(f"Failed to remove old log: {log_file.name}: {e}")
    
    if count > 0:
        logger.info(f"Cleaned up {count} old log files")
    
    return count


def get_log_stats() -> dict:
    """
    Get statistics about log files.
    
    Returns:
        Dictionary with log file stats
    """
    stats = {
        "log_dir": str(LOG_DIR),
        "total_size_mb": 0,
        "file_count": 0,
        "files": []
    }
    
    total_size = 0
    for log_file in LOG_DIR.glob("*.log*"):
        size = log_file.stat().st_size
        total_size += size
        stats["files"].append({
            "name": log_file.name,
            "size_kb": size / 1024,
            "modified": datetime.fromtimestamp(log_file.stat().st_mtime).isoformat()
        })
        stats["file_count"] += 1
    
    stats["total_size_mb"] = total_size / (1024 * 1024)
    stats["files"].sort(key=lambda x: x["modified"], reverse=True)
    
    return stats


# Context manager for operation logging
class LoggedOperation:
    """Context manager for automatic operation logging."""
    
    def __init__(self, logger: logging.Logger, operation: str, **kwargs):
        self.logger = logger
        self.operation = operation
        self.kwargs = kwargs
        self.start_time = None
        self.success = False
    
    def __enter__(self):
        self.start_time = datetime.now()
        log_operation_start(self.logger, self.operation, **self.kwargs)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = (datetime.now() - self.start_time).total_seconds()
        else:
            duration = 0
        
        if exc_type is None:
            self.success = True
            log_operation_end(self.logger, self.operation, True, duration)
        else:
            log_operation_end(self.logger, self.operation, False, duration, 
                            error=str(exc_val))
            log_exception(self.logger, f"Operation failed: {self.operation}", exc_val)
        
        return False  # Don't suppress exceptions


# Initialize logging on module import
setup_logging()
