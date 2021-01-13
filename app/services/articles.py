from slugify import slugify


def get_slug_for_article(title: str) -> str:
    return slugify(title)
