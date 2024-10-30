from typing import Dict


class Server:
    # Keep the previous implementation

    def indexed_dataset(self) -> Dict[int, List]:
        """Provides an indexed dataset."""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {i: dataset[i] for i in range(
                len(dataset))}
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = 0, page_size: int = 10) -> Dict:
        """Pagination with dynamic indexing after deletions."""
        assert 0 <= index < len(self.indexed_dataset())

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
