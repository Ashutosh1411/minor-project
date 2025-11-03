import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox


class BeautifulEventLog(ttk.Frame):
    """Compact event log with smaller boxes"""
    def __init__(self, parent):
        super().__init__(parent, bootstyle="dark")
        self.event_stats = {
            'tlb_hits': 0,
            'page_faults': 0,
            'page_hits': 0,
            'swaps': 0,
            'total': 0
        }
        self.step_count = 0
        self.text_widget = None
        self.stats_labels = {}
        self.create_widgets()
    
    def create_widgets(self):
        """Create compact event log UI"""
        # ===== TOP COMPACT HEADER =====
        header_frame = ttk.Frame(self, bootstyle="primary", padding=10)
        header_frame.pack(fill=X)
        
        # Title + Stats in one line
        title_stats_frame = ttk.Frame(header_frame, bootstyle="primary")
        title_stats_frame.pack(fill=X)
        
        ttk.Label(title_stats_frame, text="📝 Event Log", 
                 font=("Segoe UI", 11, "bold"),
                 bootstyle="inverse-primary").pack(side=LEFT, padx=(0, 20))
        
        # Compact stats - Horizontal layout
        self.stats_labels = {}
        stats_config = [
            {'title': '⚡', 'key': 'tlb_hits', 'color': 'success'},
            {'title': '❌', 'key': 'page_faults', 'color': 'danger'},
            {'title': '✓', 'key': 'page_hits', 'color': 'info'},
            {'title': '💾', 'key': 'swaps', 'color': 'warning'},
            {'title': '📊', 'key': 'total', 'color': 'secondary'}
        ]
        
        for stat in stats_config:
            stat_frame = ttk.Frame(title_stats_frame, bootstyle=stat['color'], relief=FLAT, padding=6)
            stat_frame.pack(side=LEFT, padx=5)
            
            ttk.Label(stat_frame, text=stat['title'],
                     font=("Segoe UI", 9),
                     bootstyle=f"inverse-{stat['color']}").pack(side=LEFT, padx=(0, 5))
            
            value_label = ttk.Label(stat_frame, text='0',
                                   font=("Segoe UI", 10, "bold"),
                                   bootstyle=f"inverse-{stat['color']}")
            value_label.pack(side=LEFT)
            
            self.stats_labels[stat['key']] = value_label
        
        # ===== COMPACT EVENT LOG DISPLAY =====
        log_frame = ttk.Frame(self, bootstyle="dark")
        log_frame.pack(fill=BOTH, expand=YES, padx=10, pady=(5, 10))
        
        # Create text widget - COMPACT
        self.text_widget = tk.Text(
            log_frame,
            font=("Consolas", 9),
            bg="#0d1117",
            fg="#c9d1d9",
            insertbackground="#58a6ff",
            wrap=WORD,
            relief=FLAT,
            borderwidth=0,
            padx=12,
            pady=8,
            height=6,  # COMPACT HEIGHT
            spacing1=2,
            spacing2=1,
            spacing3=4
        )
        
        self._configure_text_tags()
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(log_frame, orient=VERTICAL, 
                                 command=self.text_widget.yview,
                                 bootstyle="info-round")
        self.text_widget.configure(yscrollcommand=scrollbar.set)
        
        self.text_widget.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y, padx=(5, 0))
        
        # ===== COMPACT CONTROL BUTTONS =====
        button_frame = ttk.Frame(self, bootstyle="dark", padding=8)
        button_frame.pack(fill=X)
        
        self.clear_btn = ttk.Button(button_frame, text="🗑️ Clear",
                                    command=self.clear_log,
                                    bootstyle="danger-outline", width=12)
        self.clear_btn.pack(side=LEFT, padx=4)
        
        self.export_btn = ttk.Button(button_frame, text="💾 Export",
                                     command=self.export_log,
                                     bootstyle="info-outline", width=12)
        self.export_btn.pack(side=LEFT, padx=4)
        
        self.copy_btn = ttk.Button(button_frame, text="📋 Copy",
                                   command=self.copy_all,
                                   bootstyle="success-outline", width=12)
        self.copy_btn.pack(side=LEFT, padx=4)
    
    def _configure_text_tags(self):
        """Configure compact text formatting tags"""
        
        # TLB Hit - Green
        self.text_widget.tag_configure('tlb_hit',
                                       font=("Consolas", 9),
                                       foreground="#3fb950",
                                       background="#0d2818",
                                       spacing3=3)
        
        # Page Fault - Red
        self.text_widget.tag_configure('page_fault',
                                       font=("Consolas", 9),
                                       foreground="#f85149",
                                       background="#3d1f1a",
                                       spacing3=3)
        
        # Page Hit - Blue
        self.text_widget.tag_configure('page_hit',
                                       font=("Consolas", 9),
                                       foreground="#58a6ff",
                                       background="#0d1b3d",
                                       spacing3=3)
        
        # Swap - Yellow
        self.text_widget.tag_configure('swap',
                                       font=("Consolas", 9),
                                       foreground="#d29922",
                                       background="#3d2d1a",
                                       spacing3=3)
        
        # Info - Cyan
        self.text_widget.tag_configure('info',
                                       font=("Consolas", 9),
                                       foreground="#79c0ff",
                                       background="#0d2a3d",
                                       spacing3=3)
    
    def add_event(self, event_type, page_num, details='', result=''):
        """Add compact formatted event"""
        self.step_count += 1
        self.event_stats['total'] += 1
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Event configuration
        event_config = {
            'TLB_HIT': {
                'tag': 'tlb_hit',
                'icon': '⚡',
                'name': 'TLB',
                'stat_key': 'tlb_hits'
            },
            'PAGE_FAULT': {
                'tag': 'page_fault',
                'icon': '❌',
                'name': 'FAULT',
                'stat_key': 'page_faults'
            },
            'PAGE_HIT': {
                'tag': 'page_hit',
                'icon': '✓',
                'name': 'HIT',
                'stat_key': 'page_hits'
            },
            'SWAP': {
                'tag': 'swap',
                'icon': '💾',
                'name': 'SWAP',
                'stat_key': 'swaps'
            },
            'INFO': {
                'tag': 'info',
                'icon': 'ℹ️',
                'name': 'INFO',
                'stat_key': None
            }
        }
        
        config = event_config.get(event_type, event_config['INFO'])
        
        # Update stats
        if config['stat_key']:
            self.event_stats[config['stat_key']] += 1
        self.update_stats()
        
        # COMPACT single-line format
        entry = f"{config['icon']} [{self.step_count:02d}] {config['name']} | "
        entry += f"Page:{page_num:2d} | {current_time}"
        
        if details:
            entry += f" | {details[:40]}"
        if result:
            entry += f" | {result[:30]}"
        
        entry += "\n"
        
        # Insert with tag
        self.text_widget.insert(tk.END, entry, config['tag'])
        
        # Auto scroll
        self.text_widget.see(tk.END)
        self.text_widget.update_idletasks()
    
    def update_stats(self):
        """Update statistics display"""
        self.stats_labels['tlb_hits'].config(text=str(self.event_stats['tlb_hits']))
        self.stats_labels['page_faults'].config(text=str(self.event_stats['page_faults']))
        self.stats_labels['page_hits'].config(text=str(self.event_stats['page_hits']))
        self.stats_labels['swaps'].config(text=str(self.event_stats['swaps']))
        self.stats_labels['total'].config(text=str(self.event_stats['total']))
    
    def clear_log(self):
        """Clear all events"""
        self.text_widget.delete('1.0', tk.END)
        self.event_stats = {
            'tlb_hits': 0,
            'page_faults': 0,
            'page_hits': 0,
            'swaps': 0,
            'total': 0
        }
        self.update_stats()
        self.step_count = 0
    
    def copy_all(self):
        """Copy log to clipboard"""
        try:
            log_content = self.text_widget.get('1.0', tk.END)
            self.text_widget.clipboard_clear()
            self.text_widget.clipboard_append(log_content)
            self.text_widget.update()
            messagebox.showinfo("Success", "✓ Copied!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def export_log(self):
        """Export log to file"""
        log_content = self.text_widget.get('1.0', tk.END)
        
        if not log_content.strip():
            messagebox.showwarning("Empty", "Nothing to export!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text", "*.txt")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(log_content)
                    f.write(f"\n\nSTATISTICS:\n")
                    f.write(f"Total: {self.event_stats['total']}\n")
                    f.write(f"TLB Hits: {self.event_stats['tlb_hits']}\n")
                    f.write(f"Faults: {self.event_stats['page_faults']}\n")
                    f.write(f"Page Hits: {self.event_stats['page_hits']}\n")
                    f.write(f"Swaps: {self.event_stats['swaps']}\n")
                
                messagebox.showinfo("Success", "✓ Exported!")
            except Exception as e:
                messagebox.showerror("Error", str(e))
