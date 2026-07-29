import re

def clean_text(text: str) -> str:
    """
    Clean and normalize extracted PDF text while preserving 
    technical skill syntax (e.g. C++, C#, .NET, Node.js).
    """
    # 1) Convert to lowercase
    text = text.lower()

    # 2) Replace multiple spaces/newlines with a single space
    text = re.sub(r'\s+', ' ', text)

    # 3) Preserve technical characters (+, #, ., -) attached to skill words
    # Remove unwanted punctuation while keeping alphanumeric, spaces, +, #, ., and -
    text = re.sub(r'[^a-z0-9\s+#\.-]', '', text)

    # 4) Trim leading/trailing spaces
    text = text.strip()

    return text