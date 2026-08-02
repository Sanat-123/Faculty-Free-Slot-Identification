import re
import spacy
from spacy.matcher import Matcher
from chatbot.subject_matcher import SubjectMatcher

nlp = spacy.load("en_core_web_sm")

matcher = Matcher(nlp.vocab)

# Free Faculty Pattern
matcher.add("FREE_FACULTY", [[
    {"LOWER": {"IN": ["free", "available"]}}
]])

# Busy Faculty Pattern
matcher.add("BUSY_FACULTY", [[
    {"LOWER": {"IN": ["busy", "occupied"]}}
]])
# Subject Search Pattern
matcher.add("SUBJECT_SEARCH", [[
    {"LOWER": {"IN": ["teach", "teaches", "subject"]}}
]])




def analyze_query(query):
    doc = nlp(query)

    matches = matcher(doc)

    intent = None

    for match_id, start, end in matches:
        intent = nlp.vocab.strings[match_id]

    # -----------------------
    # Day
    # -----------------------

    day = None

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
    ]

    for d in days:
        if d.lower() in query.lower():
            day = d
            break

    # -----------------------
    # Slot
    # -----------------------

    slot = None

    match = re.search(r"\b([1-8])\b", query)

    if match:
        slot = int(match.group(1))

    # -----------------------
    # Subject
    # -----------------------

    subject = SubjectMatcher.find_subject(query)

    return intent, day, slot, subject