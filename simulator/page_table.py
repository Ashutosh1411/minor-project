class PageTableEntry:
    """Single page table entry"""
    def __init__(self):
        self.valid = False
        self.frame_number = None
        self.dirty = False

class PageTable:
    """Simple page table"""
    def __init__(self):
        self.table = {}
    
    def get_frame(self, page_num):
        """Get frame number for page"""
        if page_num in self.table and self.table[page_num].valid:
            return self.table[page_num].frame_number
        return None
    
    def insert(self, page_num, frame_num):
        """Insert page to frame mapping"""
        if page_num not in self.table:
            self.table[page_num] = PageTableEntry()
        self.table[page_num].valid = True
        self.table[page_num].frame_number = frame_num
    
    def remove(self, page_num):
        """Remove page mapping"""
        if page_num in self.table:
            self.table[page_num].valid = False
    
    def get_all_mappings(self):
        """Get all valid page-to-frame mappings"""
        mappings = []
        for page, entry in self.table.items():
            if entry.valid:
                mappings.append((page, entry.frame_number))
        return mappings
