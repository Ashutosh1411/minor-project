class SwapSpace:
    """Simulates disk swap space"""
    def __init__(self):
        self.disk = {}
        self.swap_in_count = 0
        self.swap_out_count = 0
    
    def swap_out(self, page_num, data=None):
        """Swap page to disk"""
        self.disk[page_num] = data or f"Data_{page_num}"
        self.swap_out_count += 1
    
    def swap_in(self, page_num):
        """Swap page from disk"""
        self.swap_in_count += 1
        return self.disk.get(page_num, None)
    
    def clear(self):
        """Clear swap space"""
        self.disk.clear()
        self.swap_in_count = 0
        self.swap_out_count = 0
    
    def get_pages_on_disk(self):
        """Get list of pages in swap"""
        return list(self.disk.keys())
