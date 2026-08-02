class TypeParser:

    @staticmethod
    def detect(subject):

        s = subject.lower()

        if "lab" in s:
            return "Lab"

        if "seminar" in s:
            return "Seminar"

        if "project" in s:
            return "Project"

        return "Theory"