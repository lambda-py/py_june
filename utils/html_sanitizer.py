import bleach

from py_june import settings


def html_sanitizer(content: str) -> str:
    allowed_tags = getattr(settings, "ALLOWED_TAGS")
    allowed_attributes = getattr(settings, "ALLOWED_ATTRIBUTES")
    strip = getattr(settings, "STRIP")

    cleaned_content = bleach.clean(
        content,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=strip,
    )

    return cleaned_content
