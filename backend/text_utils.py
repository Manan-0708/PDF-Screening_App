import re

def clean_text(text: str) -> str:
    """
    Clean and normalize extracted PDF text
    """

    #1)Convert to lowercase
    text = text.lower()

    #2)Replace multiple spaces/newlines with a single space
    text = re.sub(r'\s+', ' ', text)

    #3)Remove special characters except basic punctuation(letters, numbers and spaces)
    text = re.sub(r'[^a-z0-9 ]', '', text)

    #4)Trim leading/trailing spaces
    text = text.strip()

    return text