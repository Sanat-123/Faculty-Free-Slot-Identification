import re

def is_valid_teacher(name: str) -> bool:

    name = name.strip()

    if len(name) < 5:
        return False

    prefixes = ("Dr.", "Mr.", "Ms.", "Mrs.", "Prof.")

    # Remove prefix before validation
    for p in prefixes:
        if name.startswith(p):
            name = name[len(p):].strip()
            break

    # Reject abbreviations like AS, SK, XE1, X2, MnB...
    if re.fullmatch(r"[A-Z]{1,4}\d*", name):
        return False

    # Require at least two words after removing prefix
    if len(name.split()) < 2:
        return False

    return True