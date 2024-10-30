#!/usr/bin/env python3
""" FIFOCache module """

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFO caching system """

    def __init__(self):
        super().__init__()
        self.keys_order = []

    def put(self, key, item):
        """ Add an item in the cache """
        if key is not None and item is not None:
            if len(self.cache_data) >= self.MAX_ITEMS:
                first_key = self.keys_order.pop(0)
                del self.cache_data[first_key]
                print(f"DISCARD: {first_key}")
            self.cache_data[key] = item
            if key not in self.keys_order:
                self.keys_order.append(key)

    def get(self, key):
        """ Get an item by key """
        return self.cache_data.get(key, None)
