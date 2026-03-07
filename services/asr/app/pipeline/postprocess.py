def clean_transcript(text: str) -> str:
    return " ".join(text.split()).strip()
