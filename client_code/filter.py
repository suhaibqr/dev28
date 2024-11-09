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

    def search_by_string(self, search_string, search_keys=None):
        """
        Filters the data based on a search string and a list of keys.
        Searches inside the values of the keys for string matches, and for `ACCOUNT_LIST`,
        also searches inside the dictionaries within the list for specified fields.
    
        :param search_string: String containing words to search for, separated by spaces.
        :param search_keys: List of keys to search in. If None, uses the fixed set of keys.
        :return: List of dictionaries matching all search criteria.
        """
        # Fixed keys for this method
        fixed_keys = [
            "RESOURCE_NAME", "RESOURCE_TYPE", "RESOURCE_DESCRIPTION", "DNS_NAME", 
            "DOMAIN_NAME", "RESOURCE_URL", "LOCATION", "opdevicedisplayName", 
            "opdevice_ipaddress", "opdevice_vandorName", "opdevice_deviceName", 
            "opdevice_category", "opdevice_groupDisplayName", "ACCOUNT_LIST"
        ]
        search_keys = search_keys or fixed_keys
    
        if not isinstance(search_string, str):
            raise ValueError("Search string must be a string.")
    
        # Clean and split the search string into words
        words = [word.strip() for word in search_string.split() if word.strip()]
    
        # Perform case-insensitive search for all words
        filtered_data = self.filtered_list[:]
    
        for word in words:
            word_pattern = re.compile(re.escape(word), re.IGNORECASE)
    
            def matches_any_field(item, keys):
                """Helper function to check if the word matches any key's value in the item."""
                for key in keys:
                    if key not in item or item[key] is None:
                        continue
                    if key == "ACCOUNT_LIST" and isinstance(item[key], list):
                        # Handle ACCOUNT_LIST specifically
                        for account in item[key]:
                            if not isinstance(account, dict):
                                continue
                            if any(
                                word_pattern.search(str(account.get(field, "")))
                                for field in ["ACCOUNT_DESCRIPTION", "ACCOUNT NAME"]
                            ):
                                return True
                    elif isinstance(item[key], str):
                        # Check regular string fields
                        if word_pattern.search(item[key]):
                            return True
                return False
    
            # Filter items based on whether they match the current word
            filtered_data = [item for item in filtered_data if matches_any_field(item, search_keys)]
    
        # Ensure that only items matching all words remain
        return filtered_data