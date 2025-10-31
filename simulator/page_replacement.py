from collections import OrderedDict, defaultdict

class FIFOReplacer:
    """FIFO Page Replacement"""
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.frames = []
    
    def access(self, page_num):
        """Access page, returns (victim, is_fault)"""
        if page_num in self.frames:
            return None, False
        
        victim = None
        if len(self.frames) >= self.num_frames:
            victim = self.frames.pop(0)
        
        self.frames.append(page_num)
        return victim, True

class LRUReplacer:
    """LRU Page Replacement"""
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.frames = OrderedDict()
    
    def access(self, page_num):
        """Access page, returns (victim, is_fault)"""
        if page_num in self.frames:
            self.frames.move_to_end(page_num)
            return None, False
        
        victim = None
        if len(self.frames) >= self.num_frames:
            victim, _ = self.frames.popitem(last=False)
        
        self.frames[page_num] = True
        return victim, True

class LFUReplacer:
    """LFU Page Replacement"""
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.frames = set()
        self.frequency = defaultdict(int)
    
    def access(self, page_num):
        """Access page, returns (victim, is_fault)"""
        if page_num in self.frames:
            self.frequency[page_num] += 1
            return None, False
        
        victim = None
        if len(self.frames) >= self.num_frames:
            victim = min(self.frames, key=lambda x: self.frequency[x])
            self.frames.remove(victim)
            del self.frequency[victim]
        
        self.frames.add(page_num)
        self.frequency[page_num] = 1
        return victim, True

class OptimalReplacer:
    """Optimal Page Replacement"""
    def __init__(self, num_frames, future_refs=None):
        self.num_frames = num_frames
        self.frames = set()
        self.future_refs = future_refs or []
        self.current_index = 0
    
    def access(self, page_num):
        """Access page, returns (victim, is_fault)"""
        if page_num in self.frames:
            self.current_index += 1
            return None, False
        
        victim = None
        if len(self.frames) >= self.num_frames:
            victim = self._find_optimal_victim()
            self.frames.remove(victim)
        
        self.frames.add(page_num)
        self.current_index += 1
        return victim, True
    
    def _find_optimal_victim(self):
        """Find page that won't be used for longest time"""
        future = self.future_refs[self.current_index + 1:]
        farthest = -1
        victim = None
        
        for page in self.frames:
            try:
                next_use = future.index(page)
            except ValueError:
                return page
            
            if next_use > farthest:
                farthest = next_use
                victim = page
        
        return victim if victim else list(self.frames)[0]

def get_replacer(algorithm, num_frames, future_refs=None):
    """Factory function to get replacer"""
    if algorithm == 'FIFO':
        return FIFOReplacer(num_frames)
    elif algorithm == 'LRU':
        return LRUReplacer(num_frames)
    elif algorithm == 'LFU':
        return LFUReplacer(num_frames)
    elif algorithm == 'Optimal':
        return OptimalReplacer(num_frames, future_refs)
    else:
        return LRUReplacer(num_frames)
