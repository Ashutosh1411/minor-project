import tkinter as tk

class MemoryView(tk.Frame):
    """Physical memory visualization"""
    def __init__(self, parent):
        super().__init__(parent, bg='white')
        self.canvas = tk.Canvas(self, bg='white', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.memory_manager = None
    
    def set_memory_manager(self, mm):
        """Set memory manager reference"""
        self.memory_manager = mm
        self.draw_memory()
    
    def draw_memory(self, highlight_frame=None):
        """Draw memory frames"""
        if not self.memory_manager:
            return
        
        self.canvas.delete("all")
        
        num_frames = self.memory_manager.num_frames
        cols = 4
        rows = (num_frames + cols - 1) // cols
        
        block_width = 150
        block_height = 70
        padding = 15
        
        for i in range(num_frames):
            row = i // cols
            col = i % cols
            
            x1 = col * (block_width + padding) + padding
            y1 = row * (block_height + padding) + padding
            x2 = x1 + block_width
            y2 = y1 + block_height
            
            page = self.memory_manager.physical_memory[i]
            
            if page is None:
                color = '#ecf0f1'
                text = 'Empty'
                text_color = '#95a5a6'
            else:
                color = '#3498db' if i != highlight_frame else '#27ae60'
                text = f'Page {page}'
                text_color = 'white'
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, 
                                        outline='#7f8c8d', width=2)
            
            self.canvas.create_text(x1 + 10, y1 + 10, text=f'Frame {i}',
                                   anchor='nw', font=('Arial', 9, 'bold'),
                                   fill=text_color)
            
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=text,
                                   font=('Arial', 12, 'bold'), fill=text_color)
