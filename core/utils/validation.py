"""
Ship Studio Input Validation Framework

Comprehensive validation for paths, URLs, settings, and user inputs.
Provides helpful error messages and suggestions.
"""

import re
from pathlib import Path
from typing import Optional, List, Union
from urllib.parse import urlparse

from core.utils.errors import ValidationError
from core.utils.logging import get_logger

logger = get_logger(__name__)


# Path validators
def validate_directory(path: str, must_exist: bool = True, 
                      create_if_missing: bool = False) -> Path:
    """
    Validate directory path.
    
    Args:
        path: Path to validate
        must_exist: Whether directory must already exist
        create_if_missing: Create directory if it doesn't exist
    
    Returns:
        Validated Path object
    
    Raises:
        ValidationError: If validation fails
    """
    if not path or not path.strip():
        raise ValidationError(
            "Directory path cannot be empty",
            recoverable=True
        )
    
    path_obj = Path(path).resolve()
    
    if must_exist and not path_obj.exists():
        if create_if_missing:
            try:
                path_obj.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {path_obj}")
            except Exception as e:
                raise ValidationError(
                    f"Cannot create directory: {path}",
                    details=str(e),
                    recoverable=True
                )
        else:
            raise ValidationError(
                f"Directory does not exist: {path}",
                details="Please select an existing directory or check the path.",
                recoverable=True
            )
    
    if path_obj.exists() and not path_obj.is_dir():
        raise ValidationError(
            f"Path exists but is not a directory: {path}",
            details="Please select a directory, not a file.",
            recoverable=True
        )
    
    return path_obj


def validate_file(path: str, must_exist: bool = True, 
                 allowed_extensions: Optional[List[str]] = None) -> Path:
    """
    Validate file path.
    
    Args:
        path: Path to validate
        must_exist: Whether file must already exist
        allowed_extensions: List of allowed extensions (e.g., ['.txt', '.md'])
    
    Returns:
        Validated Path object
    
    Raises:
        ValidationError: If validation fails
    """
    if not path or not path.strip():
        raise ValidationError(
            "File path cannot be empty",
            recoverable=True
        )
    
    path_obj = Path(path).resolve()
    
    if must_exist and not path_obj.exists():
        raise ValidationError(
            f"File does not exist: {path}",
            details="Please select an existing file or check the path.",
            recoverable=True
        )
    
    if path_obj.exists() and not path_obj.is_file():
        raise ValidationError(
            f"Path exists but is not a file: {path}",
            details="Please select a file, not a directory.",
            recoverable=True
        )
    
    if allowed_extensions:
        ext = path_obj.suffix.lower()
        if ext not in [e.lower() for e in allowed_extensions]:
            raise ValidationError(
                f"Invalid file extension: {ext}",
                details=f"Allowed extensions: {', '.join(allowed_extensions)}",
                recoverable=True
            )
    
    return path_obj


def validate_writable_path(path: str) -> Path:
    """
    Validate that a path is writable.
    
    Args:
        path: Path to validate
    
    Returns:
        Validated Path object
    
    Raises:
        ValidationError: If path is not writable
    """
    path_obj = Path(path).resolve()
    
    # Check if parent directory is writable
    parent = path_obj.parent
    if not parent.exists():
        raise ValidationError(
            f"Parent directory does not exist: {parent}",
            details="Create the parent directory first.",
            recoverable=True
        )
    
    # Try to create a test file
    test_file = parent / f".forge_write_test_{id(path_obj)}"
    try:
        test_file.touch()
        test_file.unlink()
    except Exception as e:
        raise ValidationError(
            f"Cannot write to directory: {parent}",
            details=f"Error: {e}\n\nCheck permissions or try a different location.",
            recoverable=True
        )
    
    return path_obj


# URL validators
def validate_url(url: str, require_scheme: bool = True,
                allowed_schemes: Optional[List[str]] = None) -> str:
    """
    Validate URL.
    
    Args:
        url: URL to validate
        require_scheme: Whether scheme (http://, https://) is required
        allowed_schemes: List of allowed schemes (default: ['http', 'https'])
    
    Returns:
        Validated URL string
    
    Raises:
        ValidationError: If validation fails
    """
    if not url or not url.strip():
        raise ValidationError(
            "URL cannot be empty",
            recoverable=True
        )
    
    url = url.strip()
    
    if allowed_schemes is None:
        allowed_schemes = ['http', 'https']
    
    try:
        parsed = urlparse(url)
    except Exception as e:
        raise ValidationError(
            f"Invalid URL format: {url}",
            details=str(e),
            recoverable=True
        )
    
    if require_scheme and not parsed.scheme:
        raise ValidationError(
            f"URL missing scheme: {url}",
            details=f"URL should start with {' or '.join(allowed_schemes)}://",
            recoverable=True
        )
    
    if parsed.scheme and parsed.scheme not in allowed_schemes:
        raise ValidationError(
            f"Invalid URL scheme: {parsed.scheme}",
            details=f"Allowed schemes: {', '.join(allowed_schemes)}",
            recoverable=True
        )
    
    if require_scheme and not parsed.netloc:
        raise ValidationError(
            f"Invalid URL: missing host/domain",
            details=f"Example: http://localhost:11434",
            recoverable=True
        )
    
    return url


def validate_api_endpoint(url: str) -> str:
    """
    Validate API endpoint URL.
    
    Args:
        url: API endpoint URL
    
    Returns:
        Validated and normalized URL
    
    Raises:
        ValidationError: If validation fails
    """
    url = validate_url(url, require_scheme=True, allowed_schemes=['http', 'https'])
    
    # Normalize: remove trailing slash
    url = url.rstrip('/')
    
    return url


# String validators
def validate_not_empty(value: str, field_name: str = "Field") -> str:
    """
    Validate that string is not empty.
    
    Args:
        value: String to validate
        field_name: Name of field for error message
    
    Returns:
        Stripped string
    
    Raises:
        ValidationError: If string is empty
    """
    if not value or not value.strip():
        raise ValidationError(
            f"{field_name} cannot be empty",
            recoverable=True
        )
    
    return value.strip()


def validate_length(value: str, min_length: Optional[int] = None,
                   max_length: Optional[int] = None, field_name: str = "Field") -> str:
    """
    Validate string length.
    
    Args:
        value: String to validate
        min_length: Minimum length (optional)
        max_length: Maximum length (optional)
        field_name: Name of field for error message
    
    Returns:
        Validated string
    
    Raises:
        ValidationError: If length is invalid
    """
    length = len(value)
    
    if min_length is not None and length < min_length:
        raise ValidationError(
            f"{field_name} is too short",
            details=f"Minimum length: {min_length}, got: {length}",
            recoverable=True
        )
    
    if max_length is not None and length > max_length:
        raise ValidationError(
            f"{field_name} is too long",
            details=f"Maximum length: {max_length}, got: {length}",
            recoverable=True
        )
    
    return value


def validate_pattern(value: str, pattern: str, field_name: str = "Field",
                    pattern_description: str = "expected pattern") -> str:
    """
    Validate string against regex pattern.
    
    Args:
        value: String to validate
        pattern: Regex pattern
        field_name: Name of field for error message
        pattern_description: Human-readable pattern description
    
    Returns:
        Validated string
    
    Raises:
        ValidationError: If pattern doesn't match
    """
    if not re.match(pattern, value):
        raise ValidationError(
            f"{field_name} has invalid format",
            details=f"Expected: {pattern_description}\nGot: {value}",
            recoverable=True
        )
    
    return value


def validate_version_string(version: str) -> str:
    """
    Validate semantic version string (e.g., "1.0.0").
    
    Args:
        version: Version string to validate
    
    Returns:
        Validated version string
    
    Raises:
        ValidationError: If version format is invalid
    """
    pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?$'
    return validate_pattern(
        version,
        pattern,
        "Version",
        "semantic version (e.g., 1.0.0 or 1.0.0-beta)"
    )


# Numeric validators
def validate_number(value: Union[int, float, str], min_value: Optional[float] = None,
                   max_value: Optional[float] = None, field_name: str = "Value") -> float:
    """
    Validate numeric value.
    
    Args:
        value: Value to validate (can be string)
        min_value: Minimum allowed value (optional)
        max_value: Maximum allowed value (optional)
        field_name: Name of field for error message
    
    Returns:
        Validated number as float
    
    Raises:
        ValidationError: If validation fails
    """
    try:
        num = float(value)
    except (ValueError, TypeError) as e:
        raise ValidationError(
            f"{field_name} must be a number",
            details=f"Got: {value}",
            recoverable=True
        )
    
    if min_value is not None and num < min_value:
        raise ValidationError(
            f"{field_name} is too small",
            details=f"Minimum: {min_value}, got: {num}",
            recoverable=True
        )
    
    if max_value is not None and num > max_value:
        raise ValidationError(
            f"{field_name} is too large",
            details=f"Maximum: {max_value}, got: {num}",
            recoverable=True
        )
    
    return num


def validate_temperature(temp: Union[float, str]) -> float:
    """
    Validate LLM temperature value (0.0 to 1.0).
    
    Args:
        temp: Temperature value
    
    Returns:
        Validated temperature
    
    Raises:
        ValidationError: If temperature is invalid
    """
    return validate_number(
        temp,
        min_value=0.0,
        max_value=1.0,
        field_name="Temperature"
    )


# Project-specific validators
def validate_project_directory(path: str) -> Path:
    """
    Validate project directory (must exist and be readable).
    
    Args:
        path: Project directory path
    
    Returns:
        Validated Path object
    
    Raises:
        ValidationError: If validation fails
    """
    path_obj = validate_directory(path, must_exist=True)
    
    # Check if directory has any files
    try:
        files = list(path_obj.iterdir())
        if not files:
            logger.warning(f"Project directory is empty: {path}")
    except Exception as e:
        raise ValidationError(
            f"Cannot read project directory: {path}",
            details=str(e),
            recoverable=True
        )
    
    return path_obj


def validate_release_name(name: str) -> str:
    """
    Validate release name (alphanumeric, underscore, hyphen only).
    
    Args:
        name: Release name
    
    Returns:
        Validated release name
    
    Raises:
        ValidationError: If name is invalid
    """
    name = validate_not_empty(name, "Release name")
    name = validate_length(name, min_length=1, max_length=100, field_name="Release name")
    
    # Allow alphanumeric, underscore, hyphen, space
    pattern = r'^[a-zA-Z0-9_\- ]+$'
    return validate_pattern(
        name,
        pattern,
        "Release name",
        "letters, numbers, spaces, underscores, and hyphens only"
    )


def validate_model_name(name: str) -> str:
    """
    Validate LLM model name.
    
    Args:
        name: Model name
    
    Returns:
        Validated model name
    
    Raises:
        ValidationError: If name is invalid
    """
    name = validate_not_empty(name, "Model name")
    name = validate_length(name, min_length=1, max_length=200, field_name="Model name")
    
    # Allow alphanumeric, underscore, hyphen, colon, dot
    pattern = r'^[a-zA-Z0-9_\-:.]+$'
    return validate_pattern(
        name,
        pattern,
        "Model name",
        "letters, numbers, underscores, hyphens, colons, and dots only"
    )


# Batch validation helper
class ValidationResult:
    """Result of validation with detailed errors."""
    
    def __init__(self):
        self.is_valid = True
        self.errors: List[tuple[str, str]] = []  # (field, message)
    
    def add_error(self, field: str, message: str):
        """Add validation error."""
        self.is_valid = False
        self.errors.append((field, message))
        logger.warning(f"Validation error - {field}: {message}")
    
    def get_summary(self) -> str:
        """Get summary of all errors."""
        if self.is_valid:
            return "All fields valid"
        
        lines = ["Validation errors:"]
        for field, message in self.errors:
            lines.append(f"  • {field}: {message}")
        return "\n".join(lines)
    
    def raise_if_invalid(self):
        """Raise ValidationError if validation failed."""
        if not self.is_valid:
            raise ValidationError(
                "Validation failed",
                details=self.get_summary(),
                recoverable=True
            )
