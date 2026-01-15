# FORGE Developer Quick Reference

## 🔥 Essential Imports

```python
# Logging
from core.utils.logging import get_logger, LoggedOperation
logger = get_logger(__name__)

# Error Handling
from core.utils.errors import (
    handle_errors, show_error, show_exception,
    ValidationError, BuildError, LLMError
)

# Validation
from core.utils.validation import (
    validate_directory, validate_file, validate_url,
    validate_not_empty, validate_number
)

# Progress
from core.utils.progress import run_with_progress, ProgressDialog

# Recent Projects
from core.utils.recent_projects import add_recent_project, get_recent_projects
```

---

## 📝 Common Patterns

### Pattern 1: Simple Function with Error Handling

```python
from core.utils.logging import get_logger
from core.utils.errors import handle_errors

logger = get_logger(__name__)

@handle_errors("Failed to load settings", show_dialog=True)
def load_settings(path):
    logger.info(f"Loading settings from {path}")
    # ... load logic
    return settings
```

### Pattern 2: Operation with Logging

```python
from core.utils.logging import get_logger, LoggedOperation

logger = get_logger(__name__)

def process_project(project_path):
    with LoggedOperation(logger, "process_project", path=project_path):
        # Automatically logs start, duration, success/failure
        result = do_processing(project_path)
        return result
```

### Pattern 3: Input Validation

```python
from core.utils.validation import validate_directory, validate_url
from core.utils.errors import ValidationError

def configure_llm(endpoint_url, model_name):
    # Validate inputs with helpful errors
    endpoint = validate_url(endpoint_url, require_scheme=True)
    model = validate_not_empty(model_name, "Model name")
    
    # ... configuration logic
```

### Pattern 4: Long Operation with Progress

```python
from core.utils.progress import run_with_progress

def my_long_task(progress_callback):
    """Worker function - receives progress callback."""
    total_steps = 100
    
    for i in range(total_steps):
        # Update progress
        progress_callback(i, total_steps, f"Step {i}/{total_steps}")
        
        # Do work
        process_step(i)
        
        # Check cancellation
        if hasattr(progress_callback, 'is_cancelled'):
            if progress_callback.is_cancelled():
                return "Cancelled"
    
    return "Complete"

def start_operation():
    """Start operation with progress dialog."""
    def on_complete(result):
        print(f"Done: {result}")
    
    def on_error(exc):
        show_error("Operation failed", str(exc))
    
    run_with_progress(
        root_window,
        "Processing...",
        my_long_task,
        on_complete,
        on_error,
        can_cancel=True
    )
```

### Pattern 5: User-Friendly Errors

```python
from core.utils.errors import show_error_with_suggestion

try:
    result = risky_operation()
except FileNotFoundError as exc:
    # Shows error with helpful suggestion
    show_error_with_suggestion(
        exc,
        "Failed to load file",
        parent=window
    )
    # Displays: "Make sure the file or folder exists and the path is correct."
```

---

## 🎯 Best Practices

### Logging

**DO:**
```python
# Use module-specific logger
logger = get_logger(__name__)

# Log important operations
logger.info(f"Starting build for {project_name}")

# Log errors with exception info
logger.error("Build failed", exc_info=True)

# Use appropriate levels
logger.debug("Detailed debug info")
logger.info("Normal operation")
logger.warning("Something unusual")
logger.error("Operation failed")
logger.critical("System-level failure")
```

**DON'T:**
```python
# Don't use print()
print("Starting build")  # ❌

# Don't log sensitive data
logger.info(f"API key: {api_key}")  # ❌

# Don't log in tight loops
for i in range(10000):
    logger.debug(f"Processing {i}")  # ❌ Too verbose
```

### Error Handling

**DO:**
```python
# Use specific exceptions
raise ValidationError("Invalid path", details=path)

# Show helpful dialogs
show_error("Build Failed", error_msg, details=log_path)

# Use decorators for common patterns
@handle_errors("Operation failed")
def my_function():
    ...
```

**DON'T:**
```python
# Don't swallow exceptions silently
try:
    operation()
except:
    pass  # ❌

# Don't show technical errors to users
messagebox.showerror("Error", str(traceback.format_exc()))  # ❌

# Don't use generic Exception
raise Exception("Something failed")  # ❌ Use specific exceptions
```

### Validation

**DO:**
```python
# Validate at entry points
def process_project(path, output_dir):
    path = validate_directory(path, must_exist=True)
    output_dir = validate_directory(output_dir, create_if_missing=True)
    # Now safe to use

# Provide context
validate_not_empty(name, "Project name")  # Good error message

# Chain validators
url = validate_not_empty(raw_url, "API endpoint")
url = validate_url(url, require_scheme=True)
```

**DON'T:**
```python
# Don't validate in loops
for item in items:
    validate_directory(item)  # ❌ Validate collection first

# Don't catch and ignore validation errors
try:
    validate_url(url)
except ValidationError:
    pass  # ❌ Handle properly

# Don't validate after use
result = use_path(path)
validate_directory(path)  # ❌ Too late!
```

---

## 🔧 Module Integration Checklist

When adding a new module:

- [ ] Import logger: `logger = get_logger(__name__)`
- [ ] Add error handling with `@handle_errors()` or try/except
- [ ] Validate all user inputs with validation framework
- [ ] Use `LoggedOperation` for main operations
- [ ] Add progress indicators for long operations (>2 seconds)
- [ ] Track recent projects if applicable
- [ ] Log start/end of operations
- [ ] Show user-friendly error messages
- [ ] Test cancellation if supporting it
- [ ] Add keyboard shortcuts if UI-heavy

---

## 🎨 UI Integration Examples

### Add Recent Projects Dropdown

```python
from core.utils.recent_projects import get_recent_projects

def build_project_selector(parent):
    frame = ttk.LabelFrame(parent, text="Project")
    
    # Path entry
    path_var = tk.StringVar()
    entry = ttk.Entry(frame, textvariable=path_var)
    entry.pack(side="left", fill="x", expand=True)
    
    # Recent projects dropdown
    recent = get_recent_projects(limit=10)
    if recent:
        recent_menu = ttk.Menubutton(frame, text="Recent ▼")
        menu = tk.Menu(recent_menu, tearoff=0)
        
        for proj in recent:
            menu.add_command(
                label=f"{proj.name} ({proj.use_count} uses)",
                command=lambda p=proj: path_var.set(p.path)
            )
        
        recent_menu.config(menu=menu)
        recent_menu.pack(side="right")
    
    return frame
```

### Add Progress to Existing Operation

```python
# Before
def create_release(project_path, output_path):
    copy_files(project_path, output_path)
    generate_docs(output_path)
    create_manifest(output_path)

# After
def create_release_with_progress(root, project_path, output_path):
    def worker(progress):
        progress(0, 3, "Copying files...")
        copy_files(project_path, output_path)
        
        progress(1, 3, "Generating documentation...")
        generate_docs(output_path)
        
        progress(2, 3, "Creating manifest...")
        create_manifest(output_path)
        
        progress(3, 3, "Complete!")
        return output_path
    
    def on_complete(result):
        show_info("Success", f"Release created at {result}")
    
    run_with_progress(root, "Creating Release", worker, on_complete)
```

---

## 📚 Framework Reference

### Logging Levels

| Level | When to Use | Example |
|-------|------------|---------|
| DEBUG | Development details | `logger.debug(f"Cache hit: {key}")` |
| INFO | Normal operations | `logger.info("Build started")` |
| WARNING | Recoverable issues | `logger.warning("Config missing, using default")` |
| ERROR | Operation failures | `logger.error("Build failed", exc_info=True)` |
| CRITICAL | System failures | `logger.critical("Cannot access disk")` |

### Exception Classes

| Exception | Use Case |
|-----------|----------|
| `ValidationError` | Invalid user input |
| `ProjectError` | Project loading/processing failures |
| `BuildError` | Build operation failures |
| `LLMError` | AI/LLM operation failures |
| `FileOperationError` | File system errors |

### Validation Functions

| Function | Purpose |
|----------|---------|
| `validate_directory()` | Check/create directories |
| `validate_file()` | Validate file paths with extensions |
| `validate_url()` | Validate URLs with schemes |
| `validate_api_endpoint()` | Normalize API endpoints |
| `validate_not_empty()` | Non-empty strings |
| `validate_number()` | Numeric ranges |
| `validate_temperature()` | LLM temperature (0.0-1.0) |

---

## 🚀 Performance Tips

1. **Log at appropriate levels** - Use DEBUG for verbose, INFO for normal
2. **Validate once** - Don't re-validate in loops
3. **Progress updates** - Update every 1-5% for smooth UI
4. **Thread long operations** - Anything >1 second
5. **Cache validations** - Store validated paths/URLs

---

## 🐛 Debugging

### View Logs

```bash
# Main log
cat ~/.forge/logs/forge.log

# Errors only
cat ~/.forge/logs/errors.log

# Everything (debug)
cat ~/.forge/logs/debug.log

# Follow in real-time
tail -f ~/.forge/logs/forge.log
```

### Test Frameworks

```python
# Test logging
from core.utils.logging import get_logger
logger = get_logger("test")
logger.info("Test message")

# Test error handling
from core.utils.errors import show_error
show_error("Test", "This is a test error")

# Test validation
from core.utils.validation import validate_directory
try:
    validate_directory("/invalid/path")
except ValidationError as e:
    print(f"Caught: {e.get_user_message()}")

# Test progress
from core.utils.progress import ProgressDialog
dialog = ProgressDialog(root, "Test")
dialog.update(50, 100, "Halfway done")
```

---

**Keep this reference handy while developing FORGE modules!** 🔥
