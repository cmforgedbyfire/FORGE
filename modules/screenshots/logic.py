import os
import datetime
from pathlib import Path

import pyautogui

from core.utils.helpers import ensure_dir


def get_timestamp() -> str:
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def get_default_output_dir(base_dir: str | None = None) -> str:
    """
    Returns a default screenshot directory with date organization.
    """
    if base_dir is None:
        base_dir = os.getcwd()
    
    # Organize by date
    today = datetime.date.today().strftime("%Y-%m-%d")
    output_dir = os.path.join(base_dir, "screenshots", today)
    ensure_dir(output_dir)
    return output_dir


def capture_full_screen(output_dir: str) -> str:
    """
    Capture the full screen and save to output_dir.
    Returns the filename.
    """
    ensure_dir(output_dir)
    ts = get_timestamp()
    filename = f"full_{ts}.png"
    path = os.path.join(output_dir, filename)
    screenshot = pyautogui.screenshot()
    screenshot.save(path)
    return filename


def capture_region(output_dir: str, region: tuple[int, int, int, int]) -> str:
    """
    Capture a specific region (left, top, width, height).
    Returns the filename.
    """
    ensure_dir(output_dir)
    ts = get_timestamp()
    filename = f"region_{ts}.png"
    path = os.path.join(output_dir, filename)
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(path)
    return filename


def capture_centered_window_like(output_dir: str, center_x: int, center_y: int,
                                 width: int = 1280, height: int = 720) -> str:
    """
    Capture a region centered around (center_x, center_y) with given width/height.
    Returns the filename.
    """
    ensure_dir(output_dir)
    left = int(center_x - width / 2)
    top = int(center_y - height / 2)

    ts = get_timestamp()
    filename = f"window_{ts}.png"
    path = os.path.join(output_dir, filename)
    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    screenshot.save(path)
    return filename
