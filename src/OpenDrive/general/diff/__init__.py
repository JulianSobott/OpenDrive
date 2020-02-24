"""
:module: OpenDrive.general.diff
:synopsis: calculating and working with differences of two files.
:author: Julian Sobott


public classes
---------------

.. autoclass:: XXX
    :members:


public functions
----------------

.. autofunction:: XXX

private functions
-----------------


"""
from dataclasses import dataclass
from typing import List, Tuple, Callable, NewType

diff_table = List[List[int]]


OperationType = NewType("OperationType", int)
REPLACE = OperationType(0)
INSERT_AFTER = OperationType(1)
REMOVE = OperationType(2)


@dataclass
class Operation:
    type: OperationType
    index1: int
    index2: int
    char1: str
    char2: str = ""


def diff_text(text1: str, text2: str) -> diff_table:
    text1 = ' ' + text1
    text2 = ' ' + text2
    arr = [[0 for _ in text2] for _ in text1]
    for i1, c1 in enumerate(text1):
        for i2, c2 in enumerate(text2):
            if i1 == i2 == 0:
                arr[i1][i2] = 0
            elif i1 == 0:
                arr[i1][i2] = i2
            elif i2 == 0:
                arr[i1][i2] = i1
            else:
                arr[i1][i2] = min(
                    arr[i1 - 1][i2] + 1,
                    arr[i1][i2 - 1] + 1,
                    arr[i1 - 1][i2 - 1] + int(c1 != c2)     # c1 == c2 -> 0, else 1
                )
    return arr


def edit_distance(text1: str, text2: str) -> int:
    return diff_text(text1, text2)[len(text1)][len(text2)]


# def diff_operations(text1: str, text2: str) -> List[Operation]:
#     """
#     Operations to fulfill, to get from text1 to text2
#     :param text1:
#     :param text2:
#     :return:
#     """
#     operations = []
#     table = diff_text(text1, text2)
#     i1, i2 = len(text1), len(text2)
#     while i1 != 0 or i2 != 0:
#         min_value = min(up := table[max(0, i1)][max(0, i2 - 1)],  # up
#                         left := table[max(0, i1 - 1)][max(0, i2)],  # left
#                         vertical := table[max(0, i1 - 1)][max(0, i2 - 1)])  # vertical
#         if up == min_value:
#             operations.append(Operation(REMOVE, i1, i2, text2[i2]))
#             new_i1 = i1 - 1
#             new_i2 = i2
#         elif left == min_value:
#             operations.append(Operation(INSERT_AFTER, i1, i2, text1[i1]))
#             new_i1 = i1
#             new_i2 = i2 - 1
#         else:   # vert
#             if vertical != 0:
#                 operations.append(Operation(REPLACE, i1, i2, text2[i2], text1[i1]))
#             else:
#                 pass    # Nothing: chars are equal
#             new_i1 = i1 - 1
#             new_i2 = i2 - 1
#         i1, i2 = max(0, new_i1), max(0, new_i2)
#     return operations
