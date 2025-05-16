def shorten_string(text: str, threshold: int, suffix: str = "...") -> str:
    if len(text) > threshold:
        return text[:threshold - len(suffix)] + suffix
    return text