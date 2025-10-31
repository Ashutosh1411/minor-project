import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from simulator.memory_manager import MemoryManager


class ControlPanel(tk.Frame):
    """Control panel with buttons and settings"""
    def __init__(self, parent, app):
        super().__init__(parent, bg='#2c3e50', height=80)
        self.app = app
        self.pack_propagate(False)
        self.create_widgets()
    
    def create_widgets(self):
        """Create control widgets"""
        # Algorithm selection
        tk.Label(self, text="Algorithm:", bg='#2c3e50', fg='white', 
                font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=10)
        
        self.algo_var = tk.StringVar(value='LRU')
        algo_menu = ttk.Combobox(self, textvariable=self.algo_var, 
                                values=['FIFO', 'LRU', 'LFU', 'Optimal'],
                                state='readonly', width=10)
        algo_menu.pack(side=tk.LEFT, padx=5)
        
        # Reference string
        tk.Label(self, text="Reference String:", bg='#2c3e50', fg='white',
                font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=20)
        
        self.ref_entry = tk.Entry(self, width=30, font=('Arial', 10))
        self.ref_entry.insert(0, "1,2,3,4,1,2,5,1,2,3,4,5")
        self.ref_entry.pack(side=tk.LEFT, padx=5)
        
        # Settings button
        self.settings_btn = tk.Button(self, text="⚙ Settings", command=self.open_settings,
                                     bg='#9b59b6', fg='white', font=('Arial', 11, 'bold'),
                                     width=10, height=1)
        self.settings_btn.pack(side=tk.LEFT, padx=10)
        
        # Start button
        self.start_btn = tk.Button(self, text="▶ Start", command=self.start_sim,
                                   bg='#27ae60', fg='white', font=('Arial', 11, 'bold'),
                                   width=10, height=1)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        # Pause button
        self.pause_btn = tk.Button(self, text="⏸ Pause", command=self.pause_sim,
                                   bg='#f39c12', fg='white', font=('Arial', 11, 'bold'),
                                   width=10, height=1, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        # Reset button
        self.reset_btn = tk.Button(self, text="↺ Reset", command=self.reset_sim,
                                   bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'),
                                   width=10, height=1)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Speed control
        tk.Label(self, text="Speed:", bg='#2c3e50', fg='white',
                font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=20)
        
        self.speed_slider = tk.Scale(self, from_=100, to=2000, orient=tk.HORIZONTAL,
                                     bg='#2c3e50', fg='white', length=150,
                                     command=self.update_speed)
        self.speed_slider.set(800)
        self.speed_slider.pack(side=tk.LEFT)
    
    def open_settings(self):
        """Open settings dialog"""
        num_frames = simpledialog.askinteger(
            "Settings",
            "Enter number of frames (4-32):",
            initialvalue=self.app.memory_manager.num_frames,
            minvalue=4,
            maxvalue=32
        )
        
        if num_frames:
            tlb_size = simpledialog.askinteger(
                "Settings",
                "Enter TLB size (4-16):",
                initialvalue=8,
                minvalue=4,
                maxvalue=16
            )
            
            if tlb_size:
                # Recreate memory manager with new settings
                self.app.memory_manager = MemoryManager(
                    num_frames=num_frames,
                    tlb_size=tlb_size,
                    algorithm=self.algo_var.get()
                )
                
                # Update all views
                self.app.memory_view.set_memory_manager(self.app.memory_manager)
                self.app.tlb_view.set_memory_manager(self.app.memory_manager)
                self.app.page_table_view.set_memory_manager(self.app.memory_manager)
                self.app.swap_view.set_memory_manager(self.app.memory_manager)
                
                self.app.log_event(f"Settings updated: {num_frames} frames, TLB size {tlb_size}")
    
    def start_sim(self):
        """Start simulation"""
        ref_string = self.ref_entry.get()
        try:
            pages = [int(x.strip()) for x in ref_string.split(',')]
            self.app.start_simulation(pages, self.algo_var.get())
            self.start_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
        except ValueError:
            messagebox.showerror("Error", "Invalid reference string!")
    
    def pause_sim(self):
        """Pause simulation"""
        self.app.pause_simulation()
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
    
    def reset_sim(self):
        """Reset simulation"""
        self.app.reset_simulation()
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
    
    def update_speed(self, value):
        """Update animation speed"""
        self.app.animation_speed = int(value)

    
    