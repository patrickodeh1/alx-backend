#!/usr/bin/env python3
"""pagination"""
import csv
import math
from typing import List, Dict, Any, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """Calculate the start and end index for pagination.

    Args:
        page (int): The current page number.
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing the start and end index.
    """
    start = (page - 1) * page_size
    end = start + page_size
    return start, end


class Server:
    """Server class to paginate a dataset of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize the Server with no dataset loaded and
        an indexed dataset."""
        self.__dataset = None
        self.__indexed_dataset = None

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

    def indexed_dataset(self) -> Dict[int, List[str]]:
        """Provides an indexed dataset.

        Returns:
            Dict[int, List[str]]: A dictionary mapping indices to dataset rows.
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {i: dataset[i] for i in range(
                len(dataset))}
        return self.__indexed_dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List[str]]:
        """Returns the specified page of data.

        Args:
            page (int): The page number to retrieve. Defaults to 1.
            page_size (int): The number of records per page. Defaults to 10.

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
            page (int): The current page number. Defaults to 1.
            page_size (int): The number of records per page. Defaults to 10.

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

    def get_hyper_index(self, index: int = 0, page_size: int = 10
                        ) -> Dict[str, Any]:
        """Pagination with dynamic indexing after deletions.

        Args:
            index (int): The starting index for pagination. Defaults to 0.
            page_size (int): The number of records per page. Defaults to 10.

        Returns:
            Dict[str, Any]: A dictionary containing pagination
            metadata and data.
        """
        assert 0 <= index < len(self.indexed_dataset()), \
            "Index is out of bounds."

        data = []
        next_index = index
        for _ in range(page_size):
            while next_index not in self.indexed_dataset():
                next_index += 1
            data.append(self.indexed_dataset()[next_index])
            next_index += 1

        return {
            'index': index,
            'next_index': next_index,
            'page_size': len(data),
            'data': data
        }
