"""Keyword lexicon for spiritual and other pastoral titles, with spelling folding for early modern Spanish."""
import re
from helpers import norm


# Extra spelling folding on top of helpers.norm: "christiana" -> "cristiana", "theologia" -> "teologia":
def fold(s):
    s = " " + norm(s) + " "
    for old, new in [("christ", "crist"), ("th", "t"), ("qua", "cua"), ("quo", "cuo"), ("sanct", "sant"),
                     ("ejemp", "ejem"), ("mm", "m"), ("nn", "n"), ("cc", "c"), ("  ", " ")]:
        s = s.replace(old, new)
    return s


# Terms are written in modern spelling and folded like the titles.
# A term matches at the start of a word: "sermon" matches "sermones", "sermonario".
SPIRITUAL = [
    "espiritual", "ejercicios espirituales", "santos ejercicios", "ejercicio cotidiano", "ejercicio de la oracion",
    "oracion mental", "oraciones devotas", "oraciones para", "modo de orar", "meditacion", "meditaciones",
    "contemplacion", "devocion", "devocionario", "devoto", "devota", "novena", "septenario", "triduo",
    "rosario", "via crucis", "via sacra", "estaciones de la", "ofrecimiento", "jaculatoria", "letania",
    "perfeccion cristiana", "perfeccion religiosa", "camino de perfeccion", "la perfeccion", "ascetic", "mistica", "mistico",
    "contemptus mundi", "imitacion de cristo", "guia de pecadores", "camino del cielo", "camino real",
    "desengano", "vanidad del mundo", "menosprecio del mundo", "temporal y eterno", "eternidad",
    "bien morir", "buena muerte", "preparacion para la muerte", "agonizantes", "arte de morir",
    "sagrada comunion", "comulgar", "frecuente comunion", "preparacion para", "del alma", "el alma", "las almas", "alma ", "almas ",
    "amor de dios", "amor divino", "amor de jesus", "pasion de cristo", "pasion de nuestro", "sagrada pasion", "la pasion",
    "dolores de", "afectos", "soliloquio", "consideraciones", "conversion del pecador", "pecador", "despertador", "escala", "escalera del cielo", "excelencias de", "oracion para", "paraiso celestial", "comulgador",
    "vida cristiana", "vida espiritual", "vida devota", "combate espiritual", "consuelo", "tribulacion",
    "subida del monte", "noche oscura", "cantico espiritual", "llama de amor", "moradas", "castillo interior",
    "conceptos del amor", "cartas espirituales", "epistolario espiritual", "purgatorio", "presencia de dios",
    "conocimiento de si", "trabajos de jesus", "misterios del rosario", "esclavitud", "esclavos de",
    "horas de recogimiento", "recogimiento", "retiro espiritual", "mistica ciudad", "oratorio", "jardin de flores",
    "ejercicios", "ejercicio de perfeccion", "imitacion de", "kempis", "simbolo de la fe", "guia de la virtud", "de la virtud",
    "las virtudes", "reflexiones cristianas", "dia cristiano", "obras cristianas", "cristiano instruido", "verdades eternas",
    "maximas eternas", "salvacion", "vida eterna", "camino espiritual", "soliloquios", "favores de", "dia lleno",
    "oraciones", "manual del cristiano", "manual de oraciones", "amar a dios", "monte calvario", "lagrimas de", "escuela de jesus",
    "consideracion", "condenados", "infierno", "misericordia divina", "cristiano sabio", "consolacion", "sacramento del altar",
    "instruccion de la oracion", "tratado de la oracion", "libro de la oracion", "arte de servir a dios",
]
PREACHING = [
    "sermon", "predico", "predicado", "predicable", "predicables", "oracion funebre", "oracion panegirica",
    "oracion evangelica", "oracion gratulatoria", "panegiric", "funebre", "honras", "exequias", "cuaresma",
    "adviento", "platica", "homilia", "dominicas", "marial", "santoral", "despertador cristiano", "discursos predicables",
    "que dijo", "dijo en", "practica de misiones", "oraciones evangelicas", "exhortacion", "discursos morales",
    "hacimiento de gracias", "accion de gracias", "conceptos escriturales", "conceptos predicables", "concionatori", "mision ", "misiones ",
]
SACRED_HISTORY = [
    "vida de san", "vida de santa", "vida del santo", "vida de la santa", "vida de s ", "vida y milagros", "vida i milagros",
    "vida del venerable", "vida de la venerable", "vida del padre", "vida de la madre", "vida del bienaventurado",
    "vida de la bienaventurada", "vida de nuestra senora", "vida de la virgen", "vida de el ", "vida de los santos",
    "vida y muerte", "vida virtudes", "vida y virtudes", "vida admirable", "vida ejemplar", "vida prodigiosa",
    "vida maravillosa", "vida del glorioso", "vida de la gloriosa", "vida del beato", "vida de la beata",
    "vida del siervo", "vida de la sierva", "vida del ilustrisimo", "vida de fray", "vida del apostol", "vidas de",
    "milagro", "martirio", "martir", "canonizacion", "beatificacion", "flos santorum", "siervo de dios",
    "sierva de dios", "bienaventurad", "santuario", "aparicion de", "traslacion", "reliquia", "historia de la orden",
    "cronica de la orden", "cronica de la provincia", "historia de la provincia", "historia eclesiastica",
    "historia pontifical", "fundacion del convento", "fundacion de la", "imagen de nuestra senora", "milagrosa imagen",
    "virtudes y milagros", "glorioso patriarca", "fundador", "fundadora",
    "los santos", "santos de", "santos ", "vida y purgatorio", "vida del ilustrisimo", "historia eclesiastica", "historia sagrada", "espana sagrada", "historia de la compania", "cronohistoria",
    "crono historia", "varones ilustres", "cronicas de la", "coronica", "cronica de la", "historia de la virgen",
    "historia de nuestra senora", "elogios", "glorias del", "misiones de", "relacion historial",
]
MORAL_THEOLOGY = [
    "casos de conciencia", "casos morales", "teologia moral", "suma moral", "suma de casos", "suma de teologia moral",
    "confesor", "confesion", "confesionario", "confesar", "penitentes", "examen de confesores", "materias morales",
    "proposiciones condenadas", "promptuario", "instruccion de sacerdotes", "examen de conciencia",
]
CATECHISM = [
    "doctrina cristiana", "catecismo", "cartilla", "declaracion copiosa", "explicacion de la doctrina",
    "misterios de la fe", "doctrina y catecismo",
]
# Unmistakably spiritual: they win over the other groups ("Obras espirituales del venerable padre...",
# "Meditaciones espirituales para los dias de cuaresma"):
STRONG_SPIRITUAL = [
    "obras espirituales", "ejercicios espirituales", "meditaciones", "meditacion", "oracion mental", "mistica ciudad",
    "camino real para la perfeccion", "vida divina", "guia de pecadores", "contemptus mundi", "imitacion de", "kempis",
    "devocionario", "novena", "via crucis", "preparacion para la muerte", "ayudar a bien morir", "ayudar a morir",
]
# Church government, lawsuits and songs, not pastoral even when they name a devotion
# ("Por el prior del convento de nuestra señora del Rosario...", "Villancicos que se cantaron..."):
NOT_PASTORAL = [
    "villancico", "letras de los villancicos", "letras que se cantaron", "muy poderoso senor", "maestranza", "estatutos",
    "constituciones", "ordenanzas", "en lo espiritual", "lo espiritual y temporal", "pleito", "ejecutoria", "alegacion",
    "edicto", "bula de", "bulla de", "comedia", "entremes", "letras que se cantan", "orden de predicadores", "predicadores", "en consideracion de", "fray gerundio", "novelas", "calendario", "indulgencias", "jubileo", "sinodales", "sinodo", "cofradia", "hermandad", "concordia entre el",
]
STARTS_NOT_PASTORAL = re.compile(r"^\W*(?:por (?:el|la|los|las|don|dona|parte) |senor |senora |ecelentisimo senor|muy reuerendo |nos (?:don|el|fr) |don [a-z]+ (?:de |por )|memorial (?:de|dado|que|a|al) (?!la uida))")
GROUPS = {"strong_spiritual": STRONG_SPIRITUAL, "not_pastoral": NOT_PASTORAL, "spiritual": SPIRITUAL, "preaching": PREACHING, "sacred_history": SACRED_HISTORY,
          "moral_theology": MORAL_THEOLOGY, "catechism": CATECHISM}


# "alma " (with a final space) matches only the whole word, so not "almanaque":
def folded_term(term):
    return fold(term).strip() + (" " if term.endswith(" ") else "")


def compile_terms(terms):
    return re.compile(r"\s(?:" + "|".join(re.escape(folded_term(t)) for t in terms) + ")")

PATTERNS = {group: compile_terms(terms) for group, terms in GROUPS.items()}


PRIORITY = ["strong_spiritual", "not_pastoral", "preaching", "sacred_history", "moral_theology", "catechism", "spiritual"]


# "Sermon que predico..." -> {"preaching"}; the first group in PRIORITY wins:
def match_groups(title):
    t = fold(title)
    if STARTS_NOT_PASTORAL.match(t):
        return set()
    if PATTERNS["strong_spiritual"].search(t):
        return {"spiritual"}
    for group in PRIORITY:
        if PATTERNS[group].search(t):
            return set() if group == "not_pastoral" else {"spiritual" if group == "strong_spiritual" else group}
    return set()


def matched_terms(title, group):
    t = fold(title)
    if group == "spiritual":
        return matched_terms(title, "strong_spiritual") + [term for term in SPIRITUAL if re.search(r"\s" + re.escape(folded_term(term)), t)]
    return [term for term in GROUPS[group] if re.search(r"\s" + re.escape(folded_term(term)), t)]


# Authors of spiritual books ("Granada, Luis de" -> spiritual) when the title says nothing ("Las obras", "Epistolas").
# Every word of an entry must be in the author field:
SPIRITUAL_AUTHORS = [
    "luis granada", "kempis", "teresa jesus", "juan cruz", "juan auila", "luis puente", "nieremberg", "francisco sales",
    "francois sales", "osuna", "estella", "alonso orozco", "pedro alcantara", "malon", "scupoli", "escupoli", "uilacastin",
    "francisco arias", "luis palma", "bernardino uillegas", "juan angeles", "laredo", "segneri", "seneri", "croiset",
    "nepueu", "agreda", "miguel molinos",
]


def spiritual_author(author_text):
    words = set(fold(author_text).split())
    return any(all(w in words for w in entry.split()) for entry in SPIRITUAL_AUTHORS)
