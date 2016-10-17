"""
:::Author:  Derrick Beckman
:::File:    ex4_1_sample.py
:::Desc:    This program will decode a caesar ciphered document given
            a cipher setting.
"""
import string


base = string.ascii_uppercase

def rot13Convert(data):
    """
    Takes a text string encodes/decodes it via ROT-13
    :param data: string text
    :return: encoded/decoded string
    """

    result = ''
    for letter in data:
        if letter.isalpha():
            base_position = base.find(letter.upper())
            encoded_position = (base_position - 13) % len(base)
            result += base[encoded_position]
        else:
            result += letter
    return result


