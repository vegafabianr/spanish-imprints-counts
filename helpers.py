"""Small functions shared by the notebooks: spelling normalization, author names and Jesuit rules."""
import re
import unicodedata


# Spelling normalization for early modern Spanish: "Exercicios spirituales" -> "ejercicios spirituales":
def norm(s):
    s = unicodedata.normalize("NFD", str(s or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    for old, new in [("v", "u"), ("y", "i"), ("ph", "f"), ("ss", "s"), ("x", "j"), ("ç", "z")]:
        s = s.replace(old, new)
    return re.sub(r"[^a-z ]+", " ", s)


# A name becomes a set of words, so "Juan Eusebio Nieremberg" matches "Nieremberg, Juan Eusebio, (1595-1658)":
STOP = {"de", "la", "las", "los", "del", "i", "san", "st", "santo", "fl", "ca", "padre", "p"}

def name_key(s):
    return frozenset(w for w in norm(s).split() if w not in STOP and len(w) > 1)


# Author statement in a title: "por el padre Luis de la Puente, de la Compañía de Jesús".
# It also catches translators ("traducido por el padre ... de la Compañía"), so it overcounts:
SJ_TITLE = re.compile(r"\b(?:religios[oa]s?|padre|padres|p|pe|hermano|maestro|doctor|lector|rector|provincial|predicador"
                      r"|cathedratico|catedratico|misionero|missionero|qualificador|calificador|theologo|teologo)\b"
                      r"[^.;]{0,90}?\bde la (?:extinguida )?compania de (?:iesus|jesus|iesu|ihesus)")

# Jesuit works without a personal author ("Institutum Societatis Iesu", heading "Ecclesia Catholica - Jesuitas"):
SJ_CORPORATE = re.compile(r"jesuitas|iesuitas|societatis iesu|societas iesu|compania de (?:iesus|jesus|iesu|ihesus)")


# Non-Jesuit homonyms of listed Jesuits; compared by name key, so dates and roles do not matter.
# Check the author tables of notebooks 3 and 4 and add names here:
NOT_JESUIT = [
    "Molina, Antonio de",   # Carthusian (Instrucción de sacerdotes).
    "Ávila, Juan de",       # Secular priest.
    "Solís, Antonio de",    # Antonio de Solís y Rivadeneyra, chronicler.
    "Pérez, Antonio",       # Philip II's secretary.
    "Ferreras, Juan de",    # Historian, secular priest.
]
NOT_JESUIT_KEYS = {" ".join(sorted(name_key(n))) for n in NOT_JESUIT}


# Page counts from the physical description. Leaves (ff., h.) count as two pages; plates do not count.
ROMAN = dict(i=1, v=5, x=10, l=50, c=100, d=500, m=1000)


# "cli" -> 151:
def roman(s):
    if not s or any(c not in ROMAN for c in s):
        return None
    total = 0
    for a, b in zip(s, s[1:] + " "):
        v = ROMAN[a]
        total += -v if b in ROMAN and ROMAN[b] > v else v
    return total


# USTC pagination: "ff. cli [1]." -> 304, "pp. [4] 46 [2]" -> 52, "1 h." -> 2:
def ustc_pages(pagination):
    if not isinstance(pagination, str):
        return None
    total, found = 0, False
    for part in re.split(r"[;,]", pagination.lower()):
        if re.search(r"\b(plates?|lám|maps?|tables?)\b", part):
            continue
        part = re.sub(r"\S+-\S+\s*\[=(\d+)\]", r"\1", part)  # "161-280 [=244]" -> 244
        part = re.sub(r"\b(\d+)-(\d+)\b", lambda m: str(max(int(m.group(2)) - int(m.group(1)) + 1, 0)), part)
        leaves = bool(re.search(r"\b(ff?|fol|h|hs|leaves)\b", part))
        for tok in re.findall(r"\[?([0-9]+|[ivxlcdm]+)\]?", part):
            n = int(tok) if tok.isdigit() else roman(tok)
            if n is None or n > 3000:
                continue
            total += n * (2 if leaves else 1)
            found = True
    return total if found else None


# "p." -> 1 page per number, "h." -> 2, no unit -> None:
def unit_of(part):
    if re.search(r"\b(p|pp|pág|págs|página|páginas)\b", part):
        return 1
    if re.search(r"\b(h|hs|hoja|hojas|f|ff|fol|folio|folios)\b", part):
        return 2
    return None


# BNE extension: "[8], 240 p." -> 248 ("[8]" takes the unit of the next number), "5 hojas" -> 10:
def bne_pages(extension):
    if not isinstance(extension, str):
        return None
    s = extension.lower()
    total, pending, found = 0, 0, False
    for part in s.split(","):
        if re.search(r"lám|grab|map|retr|estampa", part):
            continue
        numbers = [int(t) if t.isdigit() else roman(t) for t in re.findall(r"\b([0-9]+|[ivxlcdm]+)\b", part)]
        n = sum(x for x in numbers if x is not None and x < 3000)
        unit = unit_of(part)
        if unit is None:
            pending += n
            continue
        total += (n + pending) * unit
        pending = 0
        found = True
    return total if found else None


# "7 volúmenes" -> 7, "2 v." -> 2, "v." -> 1 (number unknown):
def volumes(extension):
    m = re.search(r"(\d+)?\s*\b(?:v|vol|volúmenes|t|tomos)\b\.?", str(extension).lower())
    if not m:
        return 1
    return int(m.group(1)) if m.group(1) else 1
