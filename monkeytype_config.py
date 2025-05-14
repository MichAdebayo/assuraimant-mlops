# monkeytype_config.py
from monkeytype_config import DefaultConfig


class Config(DefaultConfig):
    # Ignore files you don’t care about
    exclude = (
        ".venv/",
        "__pycache__/",
        "migrations/",
        ".vscode/",
        ".pytest_cache/",
        ".coverage",
        "tests/",
        "admin.py",
    )

    # Optional: control output formatting
    formatter = "black"
