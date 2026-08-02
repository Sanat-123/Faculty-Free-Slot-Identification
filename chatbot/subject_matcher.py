import re


from database.subject_repository import SubjectRepository
from config.subject_aliases import SUBJECT_ALIASES


class SubjectMatcher:

    @staticmethod
    def normalize(text):

        text = text.lower()

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    @staticmethod
    def find_subject(query):
        query = SubjectMatcher.normalize(query)

        # ---------- Check aliases first ----------
        for alias, actual_subject in SUBJECT_ALIASES.items():

            if SubjectMatcher.normalize(alias) in query:
                return actual_subject
        # ---------- Check actual database subjects ----------
        subjects = SubjectRepository.get_all_subjects()

        subjects = sorted(
            subjects,
            key=len,
            reverse=True
        )

        for subject in subjects:

            normalized_subject = SubjectMatcher.normalize(subject)

            if normalized_subject in query:
                return subject

        return ""