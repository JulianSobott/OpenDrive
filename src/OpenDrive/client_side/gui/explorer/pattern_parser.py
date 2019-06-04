from typing import Tuple, Union, List
import re


def parse_file_extensions(extensions: str) -> List[str]:
    """
    valid: "*.txt, *.py, *.pdf"
    :param extensions: any string, but only comma separated file extensions are allowed
    :return: parsing successful: True, list with all regular expressions, which matches the file extensions.
    parsing fails: False, Error message
    """
    regex_patterns = []
    extensions = extensions.split(",")
    for ext in extensions:
        ext = ext.strip()
        regex_patterns.append(fr".*{ext}")
    return regex_patterns
