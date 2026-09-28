import re
import unicodedata


def slugify(text):
    """Convierte un texto en un slug seguro para usarlo en una URL
    (minúsculas, sin acentos, sin espacios ni símbolos)."""
    text = unicodedata.normalize('NFKD', text or '').encode('ascii', 'ignore').decode('ascii')
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text or 'post'
