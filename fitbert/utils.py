from typing import List


def sort_first_by_second(l1: List, l2: List):
    return [x for _, x in sorted(zip(l2, l1), key=lambda pair: pair[0], reverse=True)]
