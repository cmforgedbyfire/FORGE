import os


def ensure_dir(path: str) -> None:
    """
    Ensure that a directory exists. If not, create it.
    """
    if path and not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def set_status(status_var, text: str) -> None:
    """
    Safely set the status bar text if status_var is provided.
    """
    if status_var is not None:
        status_var.set(text)
