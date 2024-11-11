from collections import OrderedDict
from typing import List, Any, Optional
import time

class CacheBase:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: OrderedDict = OrderedDict()
        self.hits = 0
        self.total_accesses = 0
    
    def get_hit_rate(self) -> float:
        """计算缓存命中率"""
        if self.total_accesses == 0:
            return 0.0
        return self.hits / self.total_accesses * 100
    
    def _debug_print(self, page: Any, is_hit: bool):
        """打印当前缓存状态，用于调试"""
        status = "Hit" if is_hit else "Miss"
        print(f"Access {page}: {status} - Cache: {list(self.cache.keys())}")
    
    def access(self, page: Any, debug: bool = False) -> bool:
        """访问一个页面，返回是否命中"""
        raise NotImplementedError("Subclasses must implement access()")

class LRUCache(CacheBase):
    def access(self, page: Any, debug: bool = False) -> bool:
        """
        访问一个页面，如果页面在缓存中，更新其位置；
        如果不在缓存中，添加到缓存，必要时删除最久未使用的页面
        """
        self.total_accesses += 1
        is_hit = False
        
        if page in self.cache:
            # 页面命中，移动到OrderedDict的末尾（表示最近使用）
            self.cache.move_to_end(page)
            self.hits += 1
            is_hit = True
        else:
            # 页面未命中，需要载入
            if len(self.cache) >= self.capacity:
                # 缓存已满，删除最久未使用的页面（OrderedDict的第一个元素）
                self.cache.popitem(last=False)
            self.cache[page] = True  # 值不重要，我们只关心键
            
        if debug:
            self._debug_print(page, is_hit)
        return is_hit

class MRUCache(CacheBase):
    def access(self, page: Any, debug: bool = False) -> bool:
        """
        访问一个页面，如果页面在缓存中，更新其位置；
        如果不在缓存中，添加到缓存，必要时删除最近使用的页面
        """
        self.total_accesses += 1
        is_hit = False
        
        if page in self.cache:
            # 页面命中
            self.cache.move_to_end(page)
            self.hits += 1
            is_hit = True
        else:
            # 页面未命中，需要载入
            if len(self.cache) >= self.capacity:
                # 缓存已满，删除最近使用的页面（OrderedDict的最后一个元素）
                self.cache.popitem(last=True)  # last=True表示移除最近的元素
            self.cache[page] = True
            self.cache.move_to_end(page)  # 将新页面移到末尾
            
        if debug:
            self._debug_print(page, is_hit)
        return is_hit

class FIFOCache(CacheBase):
    def access(self, page: Any, debug: bool = False) -> bool:
        """
        访问一个页面，如果页面在缓存中，保持其位置不变；
        如果不在缓存中，添加到缓存，必要时删除最先进入的页面
        """
        self.total_accesses += 1
        is_hit = False
        
        if page in self.cache:
            # 页面命中，位置保持不变
            self.hits += 1
            is_hit = True
        else:
            # 页面未命中，需要载入
            if len(self.cache) >= self.capacity:
                # 缓存已满，删除最先进入的页面
                self.cache.popitem(last=False)
            self.cache[page] = True
            
        if debug:
            self._debug_print(page, is_hit)
        return is_hit

def test_cache_replacement():
    # 测试序列
    page_sequence = ['P1', 'P2', 'P1', 'P4', 'P3', 'P7', 'P2', 'P1', 'P4', 'P5', 'P8', 'P6', 'P8', 'P2', 'P8']
    buffer_size = 3
    
    # 创建三种不同的缓存
    lru_cache = LRUCache(buffer_size)
    mru_cache = MRUCache(buffer_size)
    fifo_cache = FIFOCache(buffer_size)
    
    print("\nLRU Cache Simulation:")
    for page in page_sequence:
        lru_cache.access(page, debug=True)
    print(f"LRU Hit Rate: {lru_cache.get_hit_rate():.2f}%")
    
    print("\nMRU Cache Simulation:")
    for page in page_sequence:
        mru_cache.access(page, debug=True)
    print(f"MRU Hit Rate: {mru_cache.get_hit_rate():.2f}%")
    
    print("\nFIFO Cache Simulation:")
    for page in page_sequence:
        fifo_cache.access(page, debug=True)
    print(f"FIFO Hit Rate: {fifo_cache.get_hit_rate():.2f}%")

if __name__ == "__main__":
    test_cache_replacement()