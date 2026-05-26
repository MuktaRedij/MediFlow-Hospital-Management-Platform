"""
MediFlow Tests Package Initialization
Configures test environment and imports
"""

import os
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
