import bleach
from django.conf import settings


def html_sanitizer(content: str) -> str:
    return bleach.clean(
        content,
        tags=settings.ALLOWED_TAGS,
        attributes=settings.ALLOWED_ATTRIBUTES,
        strip=settings.STRIP,
    )
