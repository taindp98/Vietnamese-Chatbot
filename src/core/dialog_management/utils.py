import json


def load_pattern(pattern_file_path: str) -> dict:
    """
    Loading the pattern of intents
    args:
        - pattern_file_path: Path to the json file containing the patterns
    return:
        - the dictionary of content
    """
    return json.load(open(pattern_file_path, "r", encoding="utf8"))


def convert_list_to_dict(lst):
    """
    Convert list to dict where the keys are the list elements, and the values are the indices of the elements in the list.

    Parameters:
        lst (list)

    Returns:
        dict
    """

    if len(lst) > len(set(lst)):
        raise ValueError("List must be unique!")
    return {k: v for v, k in enumerate(lst)}
