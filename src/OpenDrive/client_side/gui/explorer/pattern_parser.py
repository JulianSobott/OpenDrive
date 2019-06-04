from typing import Tuple, Union, List
import re


def parse_patterns(extensions: str) -> List[str]:
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


    :param extensions: any string, validity is checked here
    :return: parsing successful: True, list with all regular expressions, which matches the patterns.
    parsing fails: False, Error message
    """
    extensions = extensions.replace("\\", r"/")
    extensions = extensions.replace("*", ".*")
    extensions = extensions.replace(".", r"\.")
    extensions = extensions.replace("/", r"[\/|\\]")
    regex_patterns = extensions.split(",")
    return regex_patterns
