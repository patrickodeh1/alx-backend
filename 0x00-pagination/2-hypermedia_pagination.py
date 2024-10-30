#!/usr/bin/env python3
"""Pagination"""
import csv
import math
from typing import List, Dict, Any


def index_range(page: int, page_size: int) -> tuple:
    """Calculate the start and end index for pagination.

    Args:
        page (int): The current page number.
        page_size (int): The number of items per page.

    Returns:
        tuple: A tuple containing the start and end index.
    """
    start = (page - 1) * page_size
    end = start + page_size
    return start, end


class Server:
    """Server class to paginate a dataset of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize the Server with no dataset loaded."""
        self.__dataset = None

    def dataset(self) -> List[List[str]]:
        """Loads and caches the dataset from the CSV file.

        Returns:
            List[List[str]]: The cached dataset.
        """
        if self.__dataset is None:
            try:
                with open(self.DATA_FILE, newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    self.__dataset = [row for row in reader][1:]  # Skip header
            except FileNotFoundError:
                print(f"Error: {self.DATA_FILE} not found.")
                return []
        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List[str]]:
        """Returns the specified page of data.

        Args:
            page (int): The page number to retrieve.
            page_size (int): The number of records per page.

        Returns:
            List[List[str]]: The data for the specified page.
        """
        assert isinstance(page, int) and page > 0, \
            "Page must be a positive integer."
        assert isinstance(page_size, int) and page_size > 0, \
            "Page size must be a positive integer."
        start, end = index_range(page, page_size)
        return self.dataset()[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """Provides pagination metadata.

        Args:
            page (int): The current page number.
            page_size (int): The number of records per page.

        Returns:
            Dict[str, Any]: A dictionary containing pagination
            metadata and data.
        """
        data = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.dataset()) / page_size)
        return {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': page + 1 if page < total_pages else None,
            'prev_page': page - 1 if page > 1 else None,
            'total_pages': total_pages
        }
