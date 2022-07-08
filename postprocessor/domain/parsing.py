import re

from schemas import Extra


def get_links(text: str):
    """Находит ссылки в тексте"""
    pattern = r'(https?://[^\s]+)'
    links = re.findall(pattern, text)

    result = []
    for link in links:
        result.append(
            Extra(text=link, offset=text.find(link), length=len(link))
        )

    return result


def get_tags(text: str):
    """Находит теги в тексте"""
    tags = re.findall(r'(#\w+)', text)

    return tags


def get_extra(text: str):
    """Находит в тексте экстра-данные: ссылки, упоминания и т.д."""
    extra = []

    extra += get_links(text)

    return extra

def get_extra_tags(text: str):
    """Находит в тексте тэги"""
    extra = []

    extra += get_tags(text)

    return extra