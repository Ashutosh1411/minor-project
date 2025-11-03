import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from simulator.memory_manager import MemoryManager
from .control_panel import ControlPanel
from .memory_view import MemoryView
from .tlb_view import TLBView
from .page_table_view import PageTableView
from .swap_view import SwapView
from .event_log import BeautifulEventLog  # Changed name
  # ADD THIS


class MainWindow(ttk.Window):
    """Modern main application window with ttkbootstrap"""
    def __init__(self):
        super().__init__(themename="yeti")
        
        self.title("🖥️ Virtual Memory Simulator - Modern OS Project")
        self.geometry("1600x1100")
        
        # Memory manager
        self.memory_manager = MemoryManager(num_frames=16, tlb_size=8, algorithm='LRU')
        
        # Animation state
        self.is_running = False
        self.current_index = 0
        self.reference_pages = []
        self.animation_speed = 800
        
        self.create_layout()
    
    def create_layout(self):
       """Create modern layout"""
    # Top control panel
       self.control_panel = ControlPanel(self, self)
       self.control_panel.pack(side=TOP, fill=X, padx=10, pady=10)
    
    # Main content area with PanedWindow
       main_paned = ttk.PanedWindow(self, orient=VERTICAL)
       main_paned.pack(fill=BOTH, expand=YES, padx=10, pady=5)
    
    # Upper section: Memory views + Metrics
       content_frame = ttk.Frame(main_paned)
       main_paned.add(content_frame, weight=2)
    
    # Left: Metrics panel
       metrics_frame = ttk.Frame(content_frame, bootstyle="dark", width=300)
       metrics_frame.pack(side=LEFT, fill=Y, padx=(0, 5))
       metrics_frame.pack_propagate(False)
       self.create_metrics(metrics_frame)
    
    # Right: Notebook with tabs
       self.notebook = ttk.Notebook(content_frame, bootstyle="info")
       self.notebook.pack(side=RIGHT, fill=BOTH, expand=YES)
    
    # Create tabs
       self.memory_view = MemoryView(self.notebook)
       self.tlb_view = TLBView(self.notebook)
       self.page_table_view = PageTableView(self.notebook)
       self.swap_view = SwapView(self.notebook)
    
       self.notebook.add(self.memory_view, text="🗄️ Physical Memory")
       self.notebook.add(self.tlb_view, text="⚡ TLB Cache")
       self.notebook.add(self.page_table_view, text="📋 Page Table")
       self.notebook.add(self.swap_view, text="💾 Swap Space")
    
    # Set memory manager
       self.memory_view.set_memory_manager(self.memory_manager)
       self.tlb_view.set_memory_manager(self.memory_manager)
       self.page_table_view.set_memory_manager(self.memory_manager)
       self.swap_view.set_memory_manager(self.memory_manager)
    
    # Lower section: Beautiful event log
       self.event_log = BeautifulEventLog(main_paned)
       main_paned.add(self.event_log, weight=1)

    def create_metrics(self, parent):
        """Create modern metrics panel"""
        # Header
        header = ttk.Frame(parent, bootstyle="primary", padding=15)
        header.pack(fill=X, pady=(0, 10))
        
        ttk.Label(header, text="📊 Performance Metrics", 
                 font=("Segoe UI", 14, "bold"),
                 bootstyle="inverse-primary").pack()
        
        # Metrics container
        metrics_container = ttk.Frame(parent, padding=8)
        metrics_container.pack(fill=BOTH, expand=YES)
        
        self.metric_labels = {}
        metrics = [
            ('Page Faults', 'page_faults', 'danger'),
            ('Total Accesses', 'total_accesses', 'info'),
            ('Fault Rate (%)', 'fault_rate', 'warning'),
            ('TLB Hits', 'tlb_hits', 'success'),
            ('TLB Misses', 'tlb_misses', 'danger'),
            ('TLB Hit Ratio (%)', 'tlb_hit_ratio', 'success'),
            ('Swap Ins', 'swap_ins', 'secondary'),
            ('Swap Outs', 'swap_outs', 'secondary')
        ]
        
        for label, key, color in metrics:
            card = ttk.Frame(metrics_container, bootstyle=color, 
                           relief=RAISED, padding=12)
            card.pack(fill=X, pady=8)
            
            ttk.Label(card, text=label, 
                     font=("Segoe UI", 10),
                     bootstyle=f"inverse-{color}").pack(anchor=W)
            
            value_label = ttk.Label(card, text='0', 
                                   font=("Segoe UI", 20, "bold"),
                                   bootstyle=f"inverse-{color}")
            value_label.pack(anchor=E)
            
            self.metric_labels[key] = value_label
    
    def start_simulation(self, pages, algorithm):
        """Start simulation"""
        self.is_running = True
        self.current_index = 0
        self.reference_pages = pages
        
        self.memory_manager.reset()
        self.memory_manager.algorithm = algorithm
        self.memory_manager.initialize_replacer(pages)
        
        self.event_log.clear_log()
        self.event_log.add_event('INFO', 0, 
                                details=f'Algorithm: {algorithm}',
                                result=f'Reference: {pages}')
        
        self.run_step()
    
    def run_step(self):
        """Run one simulation step"""
        if not self.is_running or self.current_index >= len(self.reference_pages):
            self.is_running = False
            self.event_log.add_event('COMPLETE', 0,
                                    details='All pages processed',
                                    result='✓ Done')
            return
        
        page = self.reference_pages[self.current_index]
        result = self.memory_manager.access_page(page)
        
        # Add to event log with proper typing
        if result['tlb_hit']:
            self.event_log.add_event(
                'TLB_HIT',
                page,
                details=f'Page {page} found in TLB',
                result=f'Frame {result["frame"]}'
            )
        
        elif result['page_fault']:
            victim_info = f'Replaced Page {result["victim"]}' if result['victim'] else 'Empty frame'
            self.event_log.add_event(
                'PAGE_FAULT',
                page,
                details=f'Page {page} not in memory - {victim_info}',
                result=f'Loaded in Frame {result["frame"]}'
            )
        
        else:
            self.event_log.add_event(
                'PAGE_HIT',
                page,
                details=f'Page {page} found in physical memory',
                result=f'Frame {result["frame"]}'
            )
        
        # Update displays
        self.memory_view.update_display(result['frame'])
        self.tlb_view.update_display()
        self.page_table_view.update_display()
        self.swap_view.update_display()
        self.update_metrics()
        
        self.current_index += 1
        self.after(self.animation_speed, self.run_step)
    
    def pause_simulation(self):
        """Pause simulation"""
        self.is_running = False
        self.event_log.add_event('PAUSE', 0,
                                details='Simulation paused by user',
                                result='Waiting...')
    
    def reset_simulation(self):
        """Reset simulation"""
        self.is_running = False
        self.current_index = 0
        self.memory_manager.reset()
        
        self.memory_view.update_display()
        self.tlb_view.update_display()
        self.page_table_view.update_display()
        self.swap_view.update_display()
        self.update_metrics()
        
        self.event_log.clear_log()
        self.event_log.add_event('RESET', 0,
                                details='All systems cleared',
                                result='Ready for new simulation')
    
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
