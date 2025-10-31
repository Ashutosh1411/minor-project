import tkinter as tk
from tkinter import ttk

class SwapView(tk.Frame):
    """Swap space display"""
    def __init__(self, parent):
        super().__init__(parent, bg='white')
        self.create_widgets()
        self.memory_manager = None
    
    def create_widgets(self):
        """Create swap space widgets"""
        tk.Label(self, text="Pages in Swap Space", bg='white',
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        self.listbox = tk.Listbox(self, font=('Arial', 11), height=20)
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def set_memory_manager(self, mm):
        """Set memory manager reference"""
        self.memory_manager = mm
        self.update_display()
    
    def update_display(self):
        """Update swap display"""
        if not self.memory_manager:
            return
        
        self.listbox.delete(0, tk.END)
        
        pages = self.memory_manager.swap_space.get_pages_on_disk()
        for page in pages:
            self.listbox.insert(tk.END, f"Page {page}")
