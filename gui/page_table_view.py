import tkinter as tk
from tkinter import ttk

class PageTableView(tk.Frame):
    """Page table display"""
    def __init__(self, parent):
        super().__init__(parent, bg='white')
        self.create_table()
        self.memory_manager = None
    
    def create_table(self):
        """Create page table"""
        columns = ('Page Number', 'Frame Number', 'Valid')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor='center')
        
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def set_memory_manager(self, mm):
        """Set memory manager reference"""
        self.memory_manager = mm
        self.update_display()
    
    def update_display(self):
        """Update page table display"""
        if not self.memory_manager:
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        mappings = self.memory_manager.page_table.get_all_mappings()
        for page, frame in mappings:
            self.tree.insert('', tk.END, values=(page, frame, '✓'))
