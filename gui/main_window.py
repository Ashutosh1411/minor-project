from tkinter import simpledialog
import tkinter as tk
from tkinter import ttk, messagebox
from simulator.memory_manager import MemoryManager
from .control_panel import ControlPanel
from .memory_view import MemoryView
from .tlb_view import TLBView
from .page_table_view import PageTableView
from .swap_view import SwapView

class MainWindow(tk.Tk):
    """Main application window"""
    def __init__(self):
        super().__init__()
        
        self.title("Virtual Memory Simulator - OS Project")
        self.geometry("1400x900")
        self.configure(bg='#ecf0f1')
        
        # Memory manager
        self.memory_manager = MemoryManager(num_frames=16, tlb_size=8, algorithm='LRU')
        
        # Animation state
        self.is_running = False
        self.current_index = 0
        self.reference_pages = []
        self.animation_speed = 800
        
        self.create_layout()
    
    def create_layout(self):
        """Create main layout"""
        # Control panel
        self.control_panel = ControlPanel(self, self)
        self.control_panel.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # Main content area
        content_frame = tk.Frame(self, bg='#ecf0f1')
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left: Metrics
        metrics_frame = tk.Frame(content_frame, bg='#34495e', width=280)
        metrics_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        metrics_frame.pack_propagate(False)
        self.create_metrics(metrics_frame)
        
        # Right: Tabs
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.memory_view = MemoryView(self.notebook)
        self.tlb_view = TLBView(self.notebook)
        self.page_table_view = PageTableView(self.notebook)
        self.swap_view = SwapView(self.notebook)
        
        self.notebook.add(self.memory_view, text="Physical Memory")
        self.notebook.add(self.tlb_view, text="TLB")
        self.notebook.add(self.page_table_view, text="Page Table")
        self.notebook.add(self.swap_view, text="Swap Space")
        
        # Set memory manager
        self.memory_view.set_memory_manager(self.memory_manager)
        self.tlb_view.set_memory_manager(self.memory_manager)
        self.page_table_view.set_memory_manager(self.memory_manager)
        self.swap_view.set_memory_manager(self.memory_manager)
        
        # Event log
        log_frame = tk.Frame(self, bg='white')
        log_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        tk.Label(log_frame, text="Event Log", bg='white', 
                font=('Arial', 12, 'bold')).pack(anchor='w', padx=5, pady=5)
        
        self.log_text = tk.Text(log_frame, height=6, font=('Courier', 9))
        log_scroll = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_metrics(self, parent):
        """Create metrics panel"""
        tk.Label(parent, text="Performance Metrics", bg='#34495e', fg='white',
                font=('Arial', 14, 'bold')).pack(pady=15)
        
        self.metric_labels = {}
        metrics = [
            ('Page Faults', 'page_faults'),
            ('Total Accesses', 'total_accesses'),
            ('Fault Rate (%)', 'fault_rate'),
            ('TLB Hits', 'tlb_hits'),
            ('TLB Misses', 'tlb_misses'),
            ('TLB Hit Ratio (%)', 'tlb_hit_ratio'),
            ('Swap Ins', 'swap_ins'),
            ('Swap Outs', 'swap_outs')
        ]
        
        for label, key in metrics:
            frame = tk.Frame(parent, bg='#34495e')
            frame.pack(fill=tk.X, padx=15, pady=8)
            
            tk.Label(frame, text=label, bg='#34495e', fg='#ecf0f1',
                    font=('Arial', 10), anchor='w').pack(side=tk.LEFT)
            
            value_label = tk.Label(frame, text='0', bg='#34495e', fg='#3498db',
                                  font=('Arial', 12, 'bold'), anchor='e')
            value_label.pack(side=tk.RIGHT)
            
            self.metric_labels[key] = value_label
    
    def start_simulation(self, pages, algorithm):
        """Start simulation"""
        self.is_running = True
        self.current_index = 0
        self.reference_pages = pages
        
        # Reset and initialize
        self.memory_manager.reset()
        self.memory_manager.algorithm = algorithm
        self.memory_manager.initialize_replacer(pages)
        
        self.log_event(f"Started {algorithm} simulation")
        self.log_event(f"Reference string: {pages}")
        
        self.run_step()
    
    def run_step(self):
        """Run one simulation step"""
        if not self.is_running or self.current_index >= len(self.reference_pages):
            self.is_running = False
            self.log_event("Simulation completed!")
            return
        
        page = self.reference_pages[self.current_index]
        result = self.memory_manager.access_page(page)
        
        # Log event
        msg = f"Access Page {page}: "
        if result['tlb_hit']:
            msg += "TLB Hit ✓"
        elif result['page_fault']:
            msg += f"Page Fault ✗"
            if result['victim']:
                msg += f" (Replaced {result['victim']})"
        else:
            msg += "Page Hit ✓"
        
        self.log_event(msg)
        
        # Update displays
        self.memory_view.draw_memory(result['frame'])
        self.tlb_view.update_display()
        self.page_table_view.update_display()
        self.swap_view.update_display()
        self.update_metrics()
        
        self.current_index += 1
        self.after(self.animation_speed, self.run_step)
    
    def pause_simulation(self):
        """Pause simulation"""
        self.is_running = False
        self.log_event("Simulation paused")
    
    def reset_simulation(self):
        """Reset simulation"""
        self.is_running = False
        self.current_index = 0
        self.memory_manager.reset()
        
        self.memory_view.draw_memory()
        self.tlb_view.update_display()
        self.page_table_view.update_display()
        self.swap_view.update_display()
        self.update_metrics()
        
        self.log_text.delete(1.0, tk.END)
        self.log_event("Simulation reset")
    
    def update_metrics(self):
        """Update metrics display"""
        metrics = self.memory_manager.get_metrics()
        
        self.metric_labels['page_faults'].config(text=str(metrics['page_faults']))
        self.metric_labels['total_accesses'].config(text=str(metrics['total_accesses']))
        self.metric_labels['fault_rate'].config(text=f"{metrics['fault_rate']:.2f}")
        self.metric_labels['tlb_hits'].config(text=str(metrics['tlb_hits']))
        self.metric_labels['tlb_misses'].config(text=str(metrics['tlb_misses']))
        self.metric_labels['tlb_hit_ratio'].config(text=f"{metrics['tlb_hit_ratio']:.2f}")
        self.metric_labels['swap_ins'].config(text=str(metrics['swap_ins']))
        self.metric_labels['swap_outs'].config(text=str(metrics['swap_outs']))
    
    def log_event(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
