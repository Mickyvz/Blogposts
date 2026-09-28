import bleach
from markupsafe import Markup

ALLOWED_TAGS = [
    'p', 'br', 'hr', 'div', 'span', 'blockquote', 'pre', 'code',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'strong', 'b', 'em', 'i', 'u', 's', 'sub', 'sup',
    'ul', 'ol', 'li',
    'a', 'img', 'figure', 'figcaption',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
    '*': ['class'],
}

ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']


def clean_html(html):
    cleaned = bleach.clean(
        html or '',
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )
    return Markup(cleaned)
