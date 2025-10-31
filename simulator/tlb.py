from collections import OrderedDict

class TLB:
    """Translation Lookaside Buffer"""
    def __init__(self, size=8):
        self.size = size
        self.entries = OrderedDict()
        self.hits = 0
        self.misses = 0
    
    def lookup(self, page_num):
        """Look up page in TLB"""
        if page_num in self.entries:
            self.hits += 1
            self.entries.move_to_end(page_num)  # LRU
            return self.entries[page_num]
        else:
            self.misses += 1
            return None
    
    def insert(self, page_num, frame_num):
        """Insert into TLB"""
        if page_num in self.entries:
            self.entries.move_to_end(page_num)
        else:
            if len(self.entries) >= self.size:
                self.entries.popitem(last=False)
            self.entries[page_num] = frame_num
    
    def clear(self):
        """Clear TLB"""
        self.entries.clear()
        self.hits = 0
        self.misses = 0
    
    def get_entries(self):
        """Get all TLB entries"""
        return list(self.entries.items())
