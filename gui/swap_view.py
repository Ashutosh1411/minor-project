import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class SwapView(ttk.Frame):
    """Modern swap space display"""
    def __init__(self, parent):
        super().__init__(parent)
        self.memory_manager = None
        self.create_widgets()
    
    def create_widgets(self):
        """Create modern swap space widgets"""
        # Header
        header_frame = ttk.Frame(self, bootstyle="dark", padding=15)
        header_frame.pack(fill=X, padx=20, pady=(20, 10))
        
        ttk.Label(header_frame, text="Swap Space (Disk Storage)", 
                 font=("Segoe UI", 14, "bold"),
                 bootstyle="inverse-dark").pack(side=LEFT)
        
        # Listbox frame
        list_frame = ttk.Frame(self)
        list_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)
        
        # Treeview as listbox replacement
        self.tree = ttk.Treeview(list_frame, columns=('page',), 
                                show='tree headings', height=20,
                                bootstyle="warning")
        
        self.tree.heading('#0', text='Index')
        self.tree.heading('page', text='Page Number')
        self.tree.column('#0', width=100, anchor=CENTER)
        self.tree.column('page', width=200, anchor=CENTER)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=VERTICAL, 
                                 command=self.tree.yview,
                                 bootstyle="warning-round")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)
    
    def set_memory_manager(self, mm):
        """Set memory manager reference"""
        self.memory_manager = mm
        self.update_display()
    
    def update_display(self):
        """Update swap display"""
        if not self.memory_manager:
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        pages = self.memory_manager.swap_space.get_pages_on_disk()
        for idx, page in enumerate(pages):
            self.tree.insert('', END, text=f'{idx + 1}', 
                           values=(f'Page {page}',))
