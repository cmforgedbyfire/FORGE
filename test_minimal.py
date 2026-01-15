import tkinter as tk
from core.config.settings import APP_DISPLAY_NAME, VERSION
from core.utils.logging import setup_logging

# Setup logging
setup_logging(console=True)

# Create minimal window
root = tk.Tk()
root.title(f"{APP_DISPLAY_NAME} v{VERSION}")
root.geometry("800x600")

# Add simple label
label = tk.Label(root, text="Ship Studio Test", font=("Arial", 16))
label.pack(pady=50)

print("Ship Studio starting...")
root.mainloop()