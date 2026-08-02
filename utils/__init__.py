def detect_room_number(subject):

    room = re.findall(r"[A-Z]*-?\d+", subject)

    if room:

        location = room[-1]

        subject = re.sub(r"[A-Z]*-?\d+", "", subject).strip()

        return subject, location

    return subject, ""
def detect_named_location(subject):

    LOCATION_END_WORDS = {
        "lab",
        "lib",
        "library",
        "hall",
        "auditorium",
        "centre",
        "center",
        "block",
        "building",
    }

    words = subject.split()

    if len(words) < 2:
        return subject, ""

    last = words[-1].lower()

    if last not in LOCATION_END_WORDS:
        return subject, ""

    # Build location from the end
    location_words = [words[-1]]

    i = len(words) - 2

    while i >= 0:

        word = words[i]

        # Stop if we reach obvious subject separators
        if word in {"-", "(", ")"}:
            break

        # Allow up to 3 words before Lab/Library/etc.
        location_words.insert(0, word)

        if len(location_words) >= 3:
            break

        i -= 1

    location = " ".join(location_words)

    subject = " ".join(words[: i + 1]).strip()

    return subject, location

def extract_location(subject):

    # Step 1: Room number detector
    subject, location = detect_room_number(subject)

    if location:
        return subject, location

    # Step 2: Named location detector
    subject, location = detect_named_location(subject)

    if location:
        return subject, location

    return subject, ""   