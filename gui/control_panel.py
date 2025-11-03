import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from tkinter import simpledialog
from simulator.memory_manager import MemoryManager


class ControlPanel(ttk.Frame):
    """Modern control panel with Bootstrap styling"""
    def __init__(self, parent, app):
        super().__init__(parent, bootstyle="dark")
        self.app = app
        self.create_widgets()
    
    def create_widgets(self):
        """Create modern control widgets"""
        # Main container with padding
        container = ttk.Frame(self, bootstyle="dark", padding=15)
        container.pack(fill=BOTH, expand=YES)
        
        # Left section - Configuration
        left_frame = ttk.Frame(container, bootstyle="dark")
        left_frame.pack(side=LEFT, fill=BOTH, expand=YES)
        
        # Algorithm selection with modern label
        ttk.Label(left_frame, text="Algorithm:", 
                 font=("Segoe UI", 11, "bold"),
                 bootstyle="inverse-dark").pack(side=LEFT, padx=(0, 8))
        
        self.algo_var = ttk.StringVar(value='LRU')
        algo_menu = ttk.Combobox(left_frame, textvariable=self.algo_var, 
                                values=['FIFO', 'LRU', 'LFU', 'Optimal'],
                                state='readonly', width=12,
                                bootstyle="info")
        algo_menu.pack(side=LEFT, padx=5)
        
        # Reference string input
        ttk.Label(left_frame, text="Reference String:", 
                 font=("Segoe UI", 11, "bold"),
                 bootstyle="inverse-dark").pack(side=LEFT, padx=(20, 8))
        
        self.ref_entry = ttk.Entry(left_frame, width=28, 
                                   font=("Segoe UI", 10),
                                   bootstyle="info")
        self.ref_entry.insert(0, "1,2,3,4,1,2,5,1,2,3,4,5")
        self.ref_entry.pack(side=LEFT, padx=5)
        
        # Right section - Action buttons
        right_frame = ttk.Frame(container, bootstyle="dark")
        right_frame.pack(side=RIGHT, padx=10)
        
        # Settings button with icon
        self.settings_btn = ttk.Button(right_frame, text="⚙ Settings", 
                                      command=self.open_settings,
                                      bootstyle="secondary-outline",
                                      width=12)
        self.settings_btn.pack(side=LEFT, padx=5)
        
        # Start button
        self.start_btn = ttk.Button(right_frame, text="▶ Start", 
                                    command=self.start_sim,
                                    bootstyle="success",
                                    width=12)
        self.start_btn.pack(side=LEFT, padx=5)
        
        # Pause button
        self.pause_btn = ttk.Button(right_frame, text="⏸ Pause", 
                                    command=self.pause_sim,
                                    bootstyle="warning",
                                    width=12,
                                    state=DISABLED)
        self.pause_btn.pack(side=LEFT, padx=5)
        
        # Reset button
        self.reset_btn = ttk.Button(right_frame, text="↺ Reset", 
                                    command=self.reset_sim,
                                    bootstyle="danger",
                                    width=12)
        self.reset_btn.pack(side=LEFT, padx=5)
        
        # Speed control with modern scale
        speed_frame = ttk.Frame(container, bootstyle="dark")
        speed_frame.pack(side=RIGHT, padx=20)
        
        ttk.Label(speed_frame, text="Speed:", 
                 font=("Segoe UI", 11, "bold"),
                 bootstyle="inverse-dark").pack(side=LEFT, padx=(0, 10))
        
        self.speed_slider = ttk.Scale(speed_frame, from_=100, to=2000, 
                                     orient=HORIZONTAL, length=180,
                                     command=self.update_speed,
                                     bootstyle="info")
        self.speed_slider.set(800)
        self.speed_slider.pack(side=LEFT)
    
    def open_settings(self):
        """Open modern settings dialog"""
        num_frames = simpledialog.askinteger(
            "Memory Settings",
            "Enter number of frames (4-32):",
            initialvalue=self.app.memory_manager.num_frames,
            minvalue=4,
            maxvalue=32
        )
        
        if num_frames:
            tlb_size = simpledialog.askinteger(
                "TLB Settings",
                "Enter TLB size (4-16):",
                initialvalue=8,
                minvalue=4,
                maxvalue=16
            )
            
            if tlb_size:
                self.app.memory_manager = MemoryManager(
                    num_frames=num_frames,
                    tlb_size=tlb_size,
                    algorithm=self.algo_var.get()
                )
                
                self.app.memory_view.set_memory_manager(self.app.memory_manager)
                self.app.tlb_view.set_memory_manager(self.app.memory_manager)
                self.app.page_table_view.set_memory_manager(self.app.memory_manager)
                self.app.swap_view.set_memory_manager(self.app.memory_manager)
                
                self.app.log_event(f"✓ Settings updated: {num_frames} frames, TLB size {tlb_size}")
    
    def start_sim(self):
        """Start simulation"""
        ref_string = self.ref_entry.get()
        try:
            pages = [int(x.strip()) for x in ref_string.split(',')]
            self.app.start_simulation(pages, self.algo_var.get())
            self.start_btn.config(state=DISABLED)
            self.pause_btn.config(state=NORMAL)
        except ValueError:
            Messagebox.show_error("Invalid reference string format!", "Input Error")
    
    def pause_sim(self):
        """Pause simulation"""
        self.app.pause_simulation()
        self.start_btn.config(state=NORMAL)
        self.pause_btn.config(state=DISABLED)
    
    def reset_sim(self):
        """Reset simulation"""
        self.app.reset_simulation()
        self.start_btn.config(state=NORMAL)
        self.pause_btn.config(state=DISABLED)
    
    def update_speed(self, value):
        """Update animation speed"""
        self.app.animation_speed = int(float(value))
