from .page_table import PageTable
from .tlb import TLB
from .page_replacement import get_replacer
from .swap_space import SwapSpace

class MemoryManager:
    """Main Virtual Memory Manager"""
    def __init__(self, num_frames=16, page_size=4096, tlb_size=8, algorithm='LRU'):
        self.num_frames = num_frames
        self.page_size = page_size
        self.algorithm = algorithm
        
        # Components
        self.page_table = PageTable()
        self.tlb = TLB(tlb_size)
        self.swap_space = SwapSpace()
        self.physical_memory = [None] * num_frames
        
        # Metrics
        self.page_faults = 0
        self.total_accesses = 0
        
        # Page replacement
        self.replacer = None
    
    def initialize_replacer(self, future_refs=None):
        """Initialize page replacement algorithm"""
        self.replacer = get_replacer(self.algorithm, self.num_frames, future_refs)
    
    def access_page(self, page_num):
        """Access a page - main simulation logic"""
        self.total_accesses += 1
        
        result = {
            'page': page_num,
            'tlb_hit': False,
            'page_fault': False,
            'victim': None,
            'frame': None
        }
        
        # Check TLB
        frame = self.tlb.lookup(page_num)
        if frame is not None:
            result['tlb_hit'] = True
            result['frame'] = frame
            return result
        
        # Check page table
        frame = self.page_table.get_frame(page_num)
        if frame is not None:
            result['frame'] = frame
            self.tlb.insert(page_num, frame)
            return result
        
        # Page fault
        result['page_fault'] = True
        self.page_faults += 1
        
        # Page replacement
        victim, _ = self.replacer.access(page_num)
        
        if victim is not None:
            result['victim'] = victim
            victim_frame = self._find_page_frame(victim)
            if victim_frame is not None:
                self.swap_space.swap_out(victim)
                self.physical_memory[victim_frame] = page_num
                result['frame'] = victim_frame
                self.page_table.remove(victim)
                self.page_table.insert(page_num, victim_frame)
        else:
            # Find empty frame
            frame = self._find_empty_frame()
            self.physical_memory[frame] = page_num
            result['frame'] = frame
            self.page_table.insert(page_num, frame)
        
        self.swap_space.swap_in(page_num)
        self.tlb.insert(page_num, result['frame'])
        
        return result
    
    def _find_empty_frame(self):
        """Find first empty frame"""
        for i in range(self.num_frames):
            if self.physical_memory[i] is None:
                return i
        return 0
    
    def _find_page_frame(self, page_num):
        """Find which frame contains page"""
        for i in range(self.num_frames):
            if self.physical_memory[i] == page_num:
                return i
        return None
    
    def reset(self):
        """Reset all components"""
        self.physical_memory = [None] * self.num_frames
        self.page_table = PageTable()
        self.tlb.clear()
        self.swap_space.clear()
        self.page_faults = 0
        self.total_accesses = 0
        self.replacer = None
    
    def get_metrics(self):
        """Get performance metrics"""
        return {
            'page_faults': self.page_faults,
            'total_accesses': self.total_accesses,
            'fault_rate': (self.page_faults / self.total_accesses * 100) if self.total_accesses > 0 else 0,
            'tlb_hits': self.tlb.hits,
            'tlb_misses': self.tlb.misses,
            'tlb_hit_ratio': (self.tlb.hits / (self.tlb.hits + self.tlb.misses) * 100) if (self.tlb.hits + self.tlb.misses) > 0 else 0,
            'swap_ins': self.swap_space.swap_in_count,
            'swap_outs': self.swap_space.swap_out_count
        }
