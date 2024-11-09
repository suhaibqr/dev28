import anvil.server
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#
import re

class DictFilter:
    def __init__(self, data, keys):
        self.original_list = data
        self.filtered_list = data[:]
        self.keys = keys
        self.available_options = self._generate_available_options()

    def _generate_available_options(self):
        options = {}
        for key in self.keys:
            options[key] = {item[key] for item in self.filtered_list if key in item and item[key] is not None}
        return options

    def get_unique_options(self, key):
        if key in self.keys:
            return self.available_options.get(key, set())
        else:
            raise ValueError(f"Key '{key}' is not in the list of keys to filter on.")

    def filter_by_criteria(self, criteria):
        for key, values in criteria.items():
            if key in self.keys:
                self.filtered_list = [
                    item for item in self.filtered_list if item.get(key) in values
                ]
        self.available_options = self._generate_available_options()

    def reset_filter(self):
        self.filtered_list = self.original_list[:]
        self.available_options = self._generate_available_options()

    def search_by_string(self, search_string, search_keys):
        """
        Filters the data based on a search string and a list of keys.
        Only items matching all words in the search string across the specified keys are returned.

        :param search_string: String containing words to search for, separated by spaces.
        :param search_keys: List of keys to search in.
        :return: List of dictionaries matching all search criteria.
        """
        if not isinstance(search_string, str):
            raise ValueError("Search string must be a string.")
        if not isinstance(search_keys, list):
            raise ValueError("Search keys must be a list.")

        # Clean and split the search string into words
        words = [word.strip() for word in search_string.split() if word.strip()]

        # Perform case-insensitive search for all words
        filtered_data = self.filtered_list[:]
        for word in words:
            word_pattern = re.compile(re.escape(word), re.IGNORECASE)
            filtered_data = [
                item for item in filtered_data
                if any(
                    key in item and item[key] is not None and isinstance(item[key], str) and word_pattern.search(item[key])
                    for key in search_keys
                )
            ]
        
        # Ensure that only items matching all words remain
        return filtered_data