import inflect


from enum import Enum


def to_plural(word):
    """Used to pluralize a word

    Args:
        - word (str): The word to be pluralized

    Return:
        - str: The pluralized word
    """
    p = inflect.engine()
    return p.plural(word)


class Enumeration(str, Enum):
    @classmethod
    def choices(cls):
        return tuple((x.value, x.name) for x in cls)

    def __str__(self):
        return f"{self.value}"
