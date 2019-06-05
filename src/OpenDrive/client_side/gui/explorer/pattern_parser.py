from typing import Tuple, Union, List
import re


def parse_patterns(patterns: str) -> List[str]:
    """
    good resource for some rules: https://freefilesync.org/manual.php?topic=exclude-items

    valid:

    - Everything *
    - Single file C:/Source/file.txt 	                            /file.txt
    - Single folder C:/Source/SubFolder 	                        /SubFolder/
    - All files (and folders) named thumbs.db 	                    */thumbs.db
    - All *.tmp files located in SubFolder 	                        /SubFolder/*.tmp
    - Files and folders containing temp somewhere in their path 	*temp*
    - File extension	                                            *.tmp
    - All subdirectories of the base directories 	                */
    - *.txt files located in subdirectories of base directories     /*/*.txt


    :param patterns: any string, validity is checked here
    :return: parsing successful: True, list with all regular expressions, which matches the patterns.
    parsing fails: False, Error message
    """
    patterns = patterns.replace("\\", r"/")
    patterns = patterns.replace(".", r"\.")
    patterns = patterns.replace("*", ".*")
    patterns = patterns.replace("/", r"[\/|\\]")
    regex_patterns = patterns.split(",")
    return regex_patterns
