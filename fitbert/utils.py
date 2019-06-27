from typing import Tuple


def mask(s: str, span: Tuple[int, int], mask_token="***mask***") -> Tuple[str, str]:
    subs = s[span[0] : span[1]]
    return s.replace(subs, mask_token), subs

