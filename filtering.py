BAD_WORDS = {"badword1","badword2","slur1","slur2"}

def needs_filter(text: str) -> bool:
    low = text.lower()
    return any(b in low for b in BAD_WORDS)

def sanitize(text: str) -> str:
    out = text
    for w in BAD_WORDS:
        out = out.replace(w, "*"*len(w))
    return out
