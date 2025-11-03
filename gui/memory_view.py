import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class MemoryView(ttk.Frame):
    """Modern physical memory visualization with cards"""
    def __init__(self, parent):
        super().__init__(parent)
        
        # Scrollable frame
        self.scrolled_frame = ttk.Frame(self)
        self.scrolled_frame.pack(fill=BOTH, expand=YES, padx=20, pady=20)
        
        self.memory_manager = None
        self.frame_cards = []
    
    def set_memory_manager(self, mm):
        """Set memory manager and create cards"""
        self.memory_manager = mm
        self.create_memory_cards()
    
    def create_memory_cards(self):
        """Create modern memory frame cards"""
        # Clear existing
        for widget in self.scrolled_frame.winfo_children():
            widget.destroy()
        self.frame_cards = []
        
        if not self.memory_manager:
            return
        
        num_frames = self.memory_manager.num_frames
        cols = 4
        
        for i in range(num_frames):
            row = i // cols
            col = i % cols
            
            # Card frame
            card = ttk.Frame(self.scrolled_frame, bootstyle="secondary", 
                           relief=RAISED, padding=15)
            card.grid(row=row, column=col, padx=12, pady=12, sticky=NSEW)
            
            # Frame number badge
            badge = ttk.Label(card, text=f"Frame {i}", 
                            font=("Segoe UI", 10, "bold"),
                            bootstyle="inverse-secondary")
            badge.pack(pady=(0, 10))
            
            # Content label
            content_label = ttk.Label(card, text="Empty", 
                                     font=("Segoe UI", 16, "bold"),
                                     bootstyle="secondary")
            content_label.pack(pady=15)
            
            self.frame_cards.append({
                'card': card,
                'badge': badge,
                'label': content_label
            })
        
        # Configure grid weights
        for i in range(cols):
            self.scrolled_frame.columnconfigure(i, weight=1)
    
    def update_display(self, highlight_frame=None):
        """Update memory display with modern styling"""
        if not self.memory_manager:
            return
        
        for i, page in enumerate(self.memory_manager.physical_memory):
            widgets = self.frame_cards[i]
            
            if page is None:
                # Empty frame - light style
                widgets['card'].configure(bootstyle="light")
                widgets['badge'].configure(bootstyle="inverse-light")
                widgets['label'].configure(text="Empty", bootstyle="secondary")
            else:
                # Occupied frame - color based on state
                if i == highlight_frame:
                    # Recently accessed - success color
                    widgets['card'].configure(bootstyle="success")
                    widgets['badge'].configure(bootstyle="inverse-success")
                    widgets['label'].configure(text=f"Page {page}", 
                                              bootstyle="inverse-success")
                else:
                    # Normal occupied - info color
                    widgets['card'].configure(bootstyle="info")
                    widgets['badge'].configure(bootstyle="inverse-info")
                    widgets['label'].configure(text=f"Page {page}", 
                                              bootstyle="inverse-info")
