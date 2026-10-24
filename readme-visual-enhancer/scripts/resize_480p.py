#!/data/data/com.termux/files/usr/bin/python3
# ==============================================================================
# Script Name: resize_480p.py (Compatibility Alias for resize_420p.py)
# Description: Compatibility CLI wrapper that delegates to resize_420p.py with configurable
#              maximum dimension (defaults to 420px max while strictly maintaining aspect ratio).
# Version: 1.2.0
# Date Created: 2026-10-21
# Author: Elton Boehnen · boehnenelton2024@gmail.com · boehnenelton2024.pages.dev · github.com/boehnenelton
# RELATIONAL_ID: ff0c7a93-b206-4a67-a7a8-67cd8a5732b7
# ==============================================================================

import sys
from pathlib import Path

# Add current script directory to module search path
current_script_directory = Path(__file__).resolve().parent
sys.path.insert(0, str(current_script_directory))

from resize_420p import main

if __name__ == "__main__":
    main()
