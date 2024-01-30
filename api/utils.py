import inflect


def to_plural(word):
    """Used to pluralize a word

    Args:
        - word (str): The word to be pluralized
    
    Return:
        - str: The pluralized word
    """
    p = inflect.engine()
    return p.plural(word)
