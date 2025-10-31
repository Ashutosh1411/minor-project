"""
Virtual Memory Simulator
A comprehensive OS project demonstrating multi-level paging, TLB, and page replacement
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow

def main():
    """Entry point"""
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
