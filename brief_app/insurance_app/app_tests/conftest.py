import sys
import os
from pathlib import Path
import django

# Add the project directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brief_app.settings")
django.setup()
