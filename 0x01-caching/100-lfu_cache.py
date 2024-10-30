#!/usr/bin/env python3
""" LFU Caching module """

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache defines a Least Frequently Used (LFU) caching system """

    def __init__(self):
        """ Initialize LFUCache """
        super().__init__()
        self.usage_frequency = {}
        self.access_order = {}

    def put(self, key, item):
        """ Add an item in the cache with LFU policy """
        if key is None or item is None:
            return

        # Insert/update cache and usage tracking
        self.cache_data[key] = item
        if key in self.usage_frequency:
            self.usage_frequency[key] += 1
        else:
            self.usage_frequency[key] = 1

        self.access_order[key] = len(self.access_order)

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            lfu_key = min(self.usage_frequency, key=lambda k: (
                self.usage_frequency[k], self.access_order[k]))
            print(f"DISCARD: {lfu_key}")
            del self.cache_data[lfu_key]
            del self.usage_frequency[lfu_key]
            del self.access_order[lfu_key]

    def get(self, key):
        """ Get an item by key, increasing its usage frequency """
        if key is None or key not in self.cache_data:
            return None
        self.usage_frequency[key] += 1
        self.access_order[key] = len(self.access_order)
        return self.cache_data[key]
