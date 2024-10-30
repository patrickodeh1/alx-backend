#!/usr/bin/env python3
"""Pagination helper functions"""


def index_range(page: int, page_size: int) -> tuple:
    """Returns a tuple of start and end indexes for pagination."""
    start = (page - 1) * page_size
    end = start + page_size
    return start, end
