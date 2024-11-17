from typing import Dict, Any, List
import heapq
from thefuzz import fuzz


class FuzzyHeap:
    """
    A heap-based data structure for fuzzy string matching and sorting using Levenshtein distance.

    This class implements a priority queue that stores items and sorts them based on
    their Levenshtein distance against a search query. Items with higher match
    ratios get higher priority in the heap.

    Attributes:
        heap (list): Internal heap structure storing tuples of (ratio, counter, item)
        counter (int): Monotonically increasing counter for stable sorting
    """
    def __init__(self):
        """
        Initialize an empty FuzzyHeap.
        
        Creates an empty heap list and initializes a counter for stable sorting
        when items have the same fuzzy match ratio.
        """
        self.heap = []
        self.counter = 0

    def push(self, item: Dict[str, Any], search_query, dictKey):
        """
        Push a new item onto the heap with its fuzzy match ratio.

        Args:
            item (Dict[str, Any]): Dictionary containing the item's data
            search_query (str): The search string to match against
            dict_key (str): The key in the item dictionary whose value should be
                           matched against the search query

        Notes:
            The ratio is negated because heapq implements a min heap, but we want
            items with higher match ratios to have higher priority.
        """
        ratio = -fuzz.ratio(search_query.lower(), item[dictKey].lower())
        self.counter += 1
        heapq.heappush(self.heap, (ratio, self.counter, item))

    def pop(self) -> Dict[str, Any]:
        """
        Remove and return the item with the highest fuzzy match ratio.

        Returns:
            Dict[str, Any]: The item dictionary with the highest match ratio,
                           or None if the heap is empty.
        """
        if self.heap:
            val = heapq.heappop(self.heap)
            return val[2]
        return None

    def get_sorted_results(self) -> List[Dict[str, Any]]:
        """
        Return all items sorted by their fuzzy match ratios in descending order.

        This method empties the heap as it builds the sorted list.

        Returns:
            List[Dict[str, Any]]: List of item dictionaries sorted by their
                                 fuzzy match ratios in descending order.
        """
        sorted_results = []
        while self.heap:
            sorted_results.append(self.pop())
        return sorted_results