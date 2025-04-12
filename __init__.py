"""
Scheduling System
"""

__version__ = '0.1.0'

# Add project root to Python path
import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

# Initialize Flask app
from src.app import create_app

app = create_app()
