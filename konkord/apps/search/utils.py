# -*- coding: utf-8 -*-

import string


def exclude_special_symbols(text):
    """
        Return string with only letters and numbers
        without special symbols, like "+", ",", "#" etc
    """
    if text is None:
        text = ''
    text = str(text).lower()

    latin_letters = str(string.ascii_lowercase)
    digits = str(string.digits)
    cyrillic_letters = u'абвгдеёжзийклмнопрстуфхцчшщъыьэюяіїє'

    all_symbols = latin_letters + digits + cyrillic_letters

    res = u''
    for s in text:
        if s in all_symbols:
            res += s

    return res
