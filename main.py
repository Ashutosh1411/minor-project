#!/usr/bin/env python3
"""
Virtual Memory Simulator - Modern Bootstrap Design
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow

def main():
    """Entry point"""
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
