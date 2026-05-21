#!/usr/bin/env python3
"""
Launcher script for the CLI interface
Run this to use the command-line interface
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.encryptor import main

if __name__ == "__main__":
    main()
