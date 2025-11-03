import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview


class TLBView(ttk.Frame):
    """Modern TLB display with styled table"""
    def __init__(self, parent):
        super().__init__(parent)
        self.memory_manager = None
        self.create_table()
    
    def create_table(self):
        """Create modern styled table"""
        # Header
        header_frame = ttk.Frame(self, bootstyle="dark", padding=15)
        header_frame.pack(fill=X, padx=20, pady=(20, 10))
        
        ttk.Label(header_frame, text="Translation Lookaside Buffer (TLB)", 
                 font=("Segoe UI", 14, "bold"),
                 bootstyle="inverse-dark").pack(side=LEFT)
        
        # Table frame
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)
        
        # Treeview with modern styling
        columns = ('Entry', 'Page Number', 'Frame Number')
        self.tree = ttk.Treeview(table_frame, columns=columns, 
                                show='headings', height=10,
                                bootstyle="info")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, 
                                 command=self.tree.yview,
                                 bootstyle="info-round")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)
    
    def set_memory_manager(self, mm):
        """Set memory manager reference"""
        self.memory_manager = mm
        self.update_display()
    
    def update_display(self):
        """Update TLB display"""
        if not self.memory_manager:
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        entries = self.memory_manager.tlb.get_entries()
        for idx, (page, frame) in enumerate(entries):
            self.tree.insert('', END, values=(idx, page, frame),
                           tags=('odd' if idx % 2 else 'even',))
