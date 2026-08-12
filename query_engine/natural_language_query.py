"""
UNISCHED AI - NATURAL LANGUAGE QUERY ENGINE

Converts natural-language questions into structured queries
against the UniSched QueryEngine.

Supported query types:

1. Faculty free
2. Faculty status
3. Teacher schedule
4. Subject search
5. Class schedule
6. Room free
7. Room status
8. Free class
9. General schedule queries

Examples:

    Which faculty is free on Monday slot 2?
    Is Dr. Mehul Mahrishi free on Monday slot 3?
    What is Dr. Mehul Mahrishi teaching on Monday?
    Who teaches OS III?
    What is the schedule of Dr. Mehul Mahrishi on Monday?
    What is the timetable of 3CS-D on Monday?
    Which room is free on Monday slot 4?
"""

from __future__ import annotations

import inspect
import re
from typing import Any, Dict, List, Optional


class NaturalLanguageQuery:
    """
    Natural-language interface over the existing QueryEngine.

    The QueryEngine is expected to provide methods/data such as:

        faculty_free_slots
        class_free_slots
        room_free_slots
        faculty_status
        teacher_schedule
        class_schedule
        subject_search

    The implementation intentionally uses room_free_slots()
    because that is the public API currently available in
    query_engine.py.
    """

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self, engine):
        self.engine = engine

    # =========================================================
    # BASIC NORMALIZATION
    # =========================================================

    @staticmethod
    def normalize_text(value: Any) -> str:
        if value is None:
            return ""

        return " ".join(
            str(value)
            .replace("\xa0", " ")
            .strip()
            .split()
        )

    @classmethod
    def normalize_lower(cls, value: Any) -> str:
        return cls.normalize_text(value).lower()

    # =========================================================
    # DAY NORMALIZATION
    # =========================================================

    @classmethod
    def normalize_day(cls, value: Any) -> str:
        value = cls.normalize_lower(value)

        mapping = {
            "mo": "monday",
            "mon": "monday",
            "monday": "monday",

            "tu": "tuesday",
            "tue": "tuesday",
            "tues": "tuesday",
            "tuesday": "tuesday",

            "we": "wednesday",
            "wed": "wednesday",
            "wednesday": "wednesday",

            "th": "thursday",
            "thu": "thursday",
            "thur": "thursday",
            "thurs": "thursday",
            "thursday": "thursday",

            "fr": "friday",
            "fri": "friday",
            "friday": "friday",

            "sa": "saturday",
            "sat": "saturday",
            "saturday": "saturday",

            "su": "sunday",
            "sun": "sunday",
            "sunday": "sunday",
        }

        return mapping.get(value, value)

    # =========================================================
    # SLOT NORMALIZATION
    # =========================================================

    @classmethod
    def normalize_slot(cls, value: Any) -> Optional[int]:
        if value is None:
            return None

        text = cls.normalize_text(value)

        if not text:
            return None

        match = re.search(r"\b([1-8])\b", text)

        if match:
            return int(match.group(1))

        return None

    # =========================================================
    # QUERY PARSING - DAY
    # =========================================================

    @classmethod
    def extract_day(cls, query: str) -> Optional[str]:

        text = cls.normalize_lower(query)

        patterns = [
            ("monday", r"\bmonday\b|\bmon\b"),
            ("tuesday", r"\btuesday\b|\btue\b|\btues\b"),
            ("wednesday", r"\bwednesday\b|\bwed\b"),
            ("thursday", r"\bthursday\b|\bthu\b|\bthur\b|\bthurs\b"),
            ("friday", r"\bfriday\b|\bfri\b"),
            ("saturday", r"\bsaturday\b|\bsat\b"),
            ("sunday", r"\bsunday\b|\bsun\b"),
        ]

        for day, pattern in patterns:
            if re.search(pattern, text):
                return day

        return None

    # =========================================================
    # QUERY PARSING - SLOT
    # =========================================================

    @classmethod
    def extract_slot(cls, query: str) -> Optional[int]:

        text = cls.normalize_lower(query)

        patterns = [
            r"\bslot\s*([1-8])\b",
            r"\bperiod\s*([1-8])\b",
            r"\bperiod\s+([1-8])\b",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)

            if match:
                return int(match.group(1))

        return None

    # =========================================================
    # QUERY PARSING - FACULTY NAME
    # =========================================================

    def extract_teacher(self, query: str) -> Optional[str]:

        text = self.normalize_text(query)

        # First try exact known teachers from QueryEngine data.
        known_teachers = self.get_known_teachers()

        if known_teachers:
            lowered = text.lower()

            matches = []

            for teacher in known_teachers:
                teacher_clean = self.normalize_text(teacher)

                if not teacher_clean:
                    continue

                if teacher_clean.lower() in lowered:
                    matches.append(teacher_clean)

            if matches:
                return max(matches, key=len)

        # Generic faculty-title pattern.
        pattern = re.compile(
            r"\b(?:Dr\.?|Mr\.?|Mrs\.?|Ms\.?)\s+"
            r"[A-Za-z][A-Za-z.\-']*(?:\s+[A-Za-z][A-Za-z.\-']*){1,6}",
            re.IGNORECASE,
        )

        match = pattern.search(text)

        if match:
            return self.normalize_text(match.group(0))

        return None

    # =========================================================
    # QUERY PARSING - CLASS
    # =========================================================

    @classmethod
    def extract_class(cls, query: str) -> Optional[str]:

        text = cls.normalize_text(query)

        # Examples:
        # 3CS-D
        # 3CS-D
        # 3CSA
        # 3CS A
        # 5CSB
        # 7CSA

        patterns = [
            r"\b\d+\s*CS[- ]?[A-Z](?:[- ]?[A-Z])?\b",
            r"\b\d+\s*CS[- ]?[A-Z]\b",
        ]

        for pattern in patterns:
            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:
                value = cls.normalize_text(match.group(0))

                value = re.sub(
                    r"\s+",
                    "",
                    value
                )

                return value

        return None

    # =========================================================
    # QUERY PARSING - ROOM
    # =========================================================

    @classmethod
    def extract_room(cls, query: str) -> Optional[str]:

        text = cls.normalize_text(query)

        # Only extract a room when the query explicitly
        # talks about a room.
        if not re.search(r"\broom\b|\bclassroom\b", text, re.I):
            return None

        # Room identifier can be:
        # 303
        # CL-22
        # 7F:EE-Lab13
        # 5F::CP5
        pattern = re.compile(
            r"\b(?:room\s*)?"
            r"([A-Za-z0-9]+(?::+|-)[A-Za-z0-9:_-]+|\d{2,4})\b",
            re.IGNORECASE,
        )

        match = pattern.search(text)

        if match:
            return cls.normalize_text(match.group(1))

        return None

    # =========================================================
    # KNOWN TEACHERS
    # =========================================================

    def get_known_teachers(self) -> List[str]:

        candidates = []

        # Try QueryEngine attributes.
        possible_attributes = [
            "teachers",
            "teacher_names",
            "faculty",
        ]

        for attribute in possible_attributes:

            try:
                value = getattr(
                    self.engine,
                    attribute,
                    None
                )

                if value:
                    if isinstance(value, dict):
                        candidates.extend(
                            str(k) for k in value.keys()
                        )

                    elif isinstance(value, (list, tuple, set)):
                        candidates.extend(
                            str(x) for x in value
                        )

            except Exception:
                pass

        # Try matcher records.
        try:
            matcher = getattr(
                self.engine,
                "matcher",
                None
            )

            if matcher is not None:

                records = getattr(
                    matcher,
                    "records",
                    []
                )

                for record in records:

                    if isinstance(record, dict):

                        teacher = record.get(
                            "teacher",
                            ""
                        )

                        if teacher:
                            candidates.append(
                                str(teacher)
                            )

                events = getattr(
                    matcher,
                    "events",
                    []
                )

                for event in events:

                    if isinstance(event, dict):

                        teacher = event.get(
                            "teacher",
                            ""
                        )

                        if teacher:
                            candidates.append(
                                str(teacher)
                            )

        except Exception:
            pass

        # Remove duplicates.
        result = []
        seen = set()

        for teacher in candidates:

            teacher = self.normalize_text(
                teacher
            )

            key = teacher.lower()

            if teacher and key not in seen:
                seen.add(key)
                result.append(teacher)

        return result

    # =========================================================
    # GENERIC ENGINE CALL
    # =========================================================

    def call_engine_method(
        self,
        method_name: str,
        **kwargs
    ):

        method = getattr(
            self.engine,
            method_name,
            None
        )

        if method is None:
            return []

        try:
            signature = inspect.signature(method)

            accepted = {}

            for name in signature.parameters:

                if name == "self":
                    continue

                if name in kwargs:
                    accepted[name] = kwargs[name]

            return method(**accepted)

        except TypeError:

            # Fallback: call with no arguments if the method
            # has an unusual signature.
            try:
                return method()
            except Exception:
                return []

        except Exception:
            return []

    # =========================================================
    # CONVERT RESULT TO LIST
    # =========================================================

    @staticmethod
    def result_to_list(result: Any) -> List[Dict[str, Any]]:

        if result is None:
            return []

        if isinstance(result, list):
            return result

        if isinstance(result, tuple):
            return list(result)

        if isinstance(result, dict):

            # Some QueryEngine methods return:
            # {"results": [...]}
            for key in (
                "results",
                "events",
                "records",
                "data",
            ):
                value = result.get(key)

                if isinstance(value, list):
                    return value

            return [result]

        return []

    # =========================================================
    # FIND FIELD VALUE
    # =========================================================

    @staticmethod
    def field(
        record: Dict[str, Any],
        *names: str
    ) -> Any:

        if not isinstance(record, dict):
            return ""

        for name in names:

            if name in record:
                return record[name]

        return ""

    # =========================================================
    # FILTER BY DAY
    # =========================================================

    def filter_day(
        self,
        records: List[Dict[str, Any]],
        day: Optional[str]
    ) -> List[Dict[str, Any]]:

        if not day:
            return records

        day = self.normalize_day(day)

        output = []

        for record in records:

            record_day = self.normalize_day(
                self.field(
                    record,
                    "day"
                )
            )

            if record_day == day:
                output.append(record)

        return output

    # =========================================================
    # FILTER BY SLOT
    # =========================================================

    def filter_slot(
        self,
        records: List[Dict[str, Any]],
        slot: Optional[int]
    ) -> List[Dict[str, Any]]:

        if slot is None:
            return records

        output = []

        for record in records:

            record_slot = self.normalize_slot(
                self.field(
                    record,
                    "slot"
                )
            )

            if record_slot == slot:
                output.append(record)

        return output

    # =========================================================
    # FILTER BY TEACHER
    # =========================================================

    def filter_teacher(
        self,
        records: List[Dict[str, Any]],
        teacher: Optional[str]
    ) -> List[Dict[str, Any]]:

        if not teacher:
            return records

        target = self.normalize_lower(
            teacher
        )

        output = []

        for record in records:

            current = self.normalize_lower(
                self.field(
                    record,
                    "teacher"
                )
            )

            if current == target:
                output.append(record)

        return output

    # =========================================================
    # FILTER BY SUBJECT
    # =========================================================

    def filter_subject(
        self,
        records: List[Dict[str, Any]],
        subject: Optional[str]
    ) -> List[Dict[str, Any]]:

        if not subject:
            return records

        target = self.normalize_lower(
            subject
        )

        output = []

        for record in records:

            current = self.normalize_lower(
                self.field(
                    record,
                    "subject"
                )
            )

            if target in current:
                output.append(record)

        return output

    # =========================================================
    # FILTER BY CLASS
    # =========================================================

    def filter_class(
        self,
        records: List[Dict[str, Any]],
        class_name: Optional[str]
    ) -> List[Dict[str, Any]]:

        if not class_name:
            return records

        target = self.normalize_lower(
            class_name
        )

        target = target.replace(
            " ",
            ""
        )

        output = []

        for record in records:

            current = self.normalize_lower(
                self.field(
                    record,
                    "class_name",
                    "class"
                )
            )

            current = current.replace(
                " ",
                ""
            )

            if current == target:
                output.append(record)

        return output

    # =========================================================
    # PARSE SUBJECT
    # =========================================================

    @classmethod
    def extract_subject(cls, query: str) -> Optional[str]:

        text = cls.normalize_text(query)

        # "Who teaches OS III?"
        match = re.search(
            r"\bwho\s+teaches\s+(.+?)\s*\??$",
            text,
            re.IGNORECASE
        )

        if match:
            return cls.normalize_text(
                match.group(1)
            )

        # "faculty teaching OS III"
        match = re.search(
            r"(?:teaching|teach|subject)\s+(.+?)\s*\??$",
            text,
            re.IGNORECASE
        )

        if match:
            return cls.normalize_text(
                match.group(1)
            )

        return None

    # =========================================================
    # INTENT DETECTION
    # =========================================================

    def detect_intent(
        self,
        query: str
    ) -> str:

        text = self.normalize_lower(
            query
        )

        # -----------------------------------------------------
        # FACULTY FREE
        # -----------------------------------------------------

        if (
            (
                "faculty" in text
                or "teacher" in text
                or "professor" in text
            )
            and (
                "free" in text
                or "available" in text
            )
        ):

            return "faculty_free"

        # "who is free"
        if (
            ("who" in text or "which" in text)
            and (
                "free" in text
                or "available" in text
            )
            and (
                "faculty" in text
                or "teacher" in text
                or "professor" in text
            )
        ):
            return "faculty_free"

        # -----------------------------------------------------
        # ROOM FREE
        # -----------------------------------------------------

        if (
            (
                "room" in text
                or "classroom" in text
            )
            and (
                "free" in text
                or "available" in text
            )
        ):
            return "room_free"

        # -----------------------------------------------------
        # CLASS FREE
        # -----------------------------------------------------

        if (
            (
                "class" in text
                or "section" in text
            )
            and (
                "free" in text
                or "available" in text
            )
        ):
            return "class_free"

        # -----------------------------------------------------
        # FACULTY STATUS
        # -----------------------------------------------------

        teacher = self.extract_teacher(
            query
        )

        if teacher and (
            "free" in text
            or "available" in text
            or "busy" in text
        ):
            return "faculty_status"

        # -----------------------------------------------------
        # TEACHER SCHEDULE
        # -----------------------------------------------------

        if teacher and (
            "schedule" in text
            or "timetable" in text
            or "teaching" in text
            or "teach" in text
        ):
            return "teacher_schedule"

        # -----------------------------------------------------
        # SUBJECT SEARCH
        # -----------------------------------------------------

        if re.search(
            r"\bwho\s+teaches\b",
            text
        ):
            return "subject_search"

        if (
            "faculty teaching" in text
            or "teachers teaching" in text
        ):
            return "subject_search"

        # -----------------------------------------------------
        # CLASS SCHEDULE
        # -----------------------------------------------------

        class_name = self.extract_class(
            query
        )

        if class_name and (
            "schedule" in text
            or "timetable" in text
            or "classes" in text
        ):
            return "class_schedule"

        # -----------------------------------------------------
        # ROOM STATUS
        # -----------------------------------------------------

        if (
            (
                "room" in text
                or "classroom" in text
            )
            and (
                "schedule" in text
                or "occupied" in text
                or "busy" in text
            )
        ):
            return "room_status"

        return "unknown"

    # =========================================================
    # FACULTY FREE
    # =========================================================

    def execute_faculty_free(
        self,
        day: Optional[str],
        slot: Optional[int]
    ) -> List[Dict[str, Any]]:

        records = self.call_engine_method(
            "faculty_free_slots",
            day=day,
            slot=slot
        )

        records = self.result_to_list(
            records
        )

        records = self.filter_day(
            records,
            day
        )

        records = self.filter_slot(
            records,
            slot
        )

        return records

    # =========================================================
    # FACULTY STATUS
    # =========================================================

    def execute_faculty_status(
        self,
        teacher: Optional[str],
        day: Optional[str],
        slot: Optional[int]
    ) -> List[Dict[str, Any]]:

        if not teacher:
            return []

        # Prefer QueryEngine's faculty_status method.
        method = getattr(
            self.engine,
            "faculty_status",
            None
        )

        if method is not None:

            try:

                signature = inspect.signature(
                    method
                )

                kwargs = {}

                for name in signature.parameters:

                    if name == "self":
                        continue

                    if name in (
                        "teacher",
                        "faculty",
                        "name",
                    ):
                        kwargs[name] = teacher

                    elif name == "day":
                        kwargs[name] = day

                    elif name == "slot":
                        kwargs[name] = slot

                result = method(
                    **kwargs
                )

                if isinstance(
                    result,
                    dict
                ):

                    if "results" in result:
                        return self.result_to_list(
                            result["results"]
                        )

                    if "records" in result:
                        return self.result_to_list(
                            result["records"]
                        )

                    # Busy status can return a
                    # structured dictionary.
                    return [result]

                return self.result_to_list(
                    result
                )

            except Exception:
                pass

        # Fallback using events.
        events = self.call_engine_method(
            "teacher_schedule",
            teacher=teacher,
            day=day
        )

        events = self.result_to_list(
            events
        )

        events = self.filter_day(
            events,
            day
        )

        events = self.filter_slot(
            events,
            slot
        )

        return events

    # =========================================================
    # TEACHER SCHEDULE
    # =========================================================

    def execute_teacher_schedule(
        self,
        teacher: Optional[str],
        day: Optional[str]
    ) -> List[Dict[str, Any]]:

        if not teacher:
            return []

        records = self.call_engine_method(
            "teacher_schedule",
            teacher=teacher,
            day=day
        )

        records = self.result_to_list(
            records
        )

        records = self.filter_day(
            records,
            day
        )

        return records

    # =========================================================
    # SUBJECT SEARCH
    # =========================================================

    def execute_subject_search(
        self,
        subject: Optional[str]
    ) -> List[Dict[str, Any]]:

        if not subject:
            return []

        records = self.call_engine_method(
            "subject_search",
            subject=subject
        )

        records = self.result_to_list(
            records
        )

        if not records:

            # Fallback to canonical events.
            events = self.call_engine_method(
                "get_events"
            )

            records = self.result_to_list(
                events
            )

            records = self.filter_subject(
                records,
                subject
            )

        return records

    # =========================================================
    # CLASS SCHEDULE
    # =========================================================

    def execute_class_schedule(
        self,
        class_name: Optional[str],
        day: Optional[str]
    ) -> List[Dict[str, Any]]:

        if not class_name:
            return []

        records = self.call_engine_method(
            "class_schedule",
            class_name=class_name,
            day=day
        )

        records = self.result_to_list(
            records
        )

        records = self.filter_day(
            records,
            day
        )

        return records

    # =========================================================
    # ROOM FREE
    # =========================================================

    def execute_room_free(
        self,
        room: Optional[str],
        day: Optional[str],
        slot: Optional[int]
    ) -> List[Dict[str, Any]]:

        # IMPORTANT:
        #
        # QueryEngine provides:
        #
        #     room_free_slots()
        #
        # It does NOT provide:
        #
        #     find_room_free_slots()
        #
        # Therefore use room_free_slots here.

        records = self.call_engine_method(
            "room_free_slots",
            room=room,
            day=day,
            slot=slot
        )

        records = self.result_to_list(
            records
        )

        records = self.filter_day(
            records,
            day
        )

        records = self.filter_slot(
            records,
            slot
        )

        # If a specific room was requested,
        # filter to that room.
        if room:

            target = self.normalize_lower(
                room
            )

            filtered = []

            for record in records:

                current = self.normalize_lower(
                    self.field(
                        record,
                        "room"
                    )
                )

                if current == target:
                    filtered.append(
                        record
                    )

            records = filtered

        return records

    # =========================================================
    # CLASS FREE
    # =========================================================

    def execute_class_free(
        self,
        day: Optional[str],
        slot: Optional[int]
    ) -> List[Dict[str, Any]]:

        records = self.call_engine_method(
            "class_free_slots",
            day=day,
            slot=slot
        )

        records = self.result_to_list(
            records
        )

        records = self.filter_day(
            records,
            day
        )

        records = self.filter_slot(
            records,
            slot
        )

        return records

    # =========================================================
    # ROOM STATUS
    # =========================================================

    def execute_room_status(
        self,
        room: Optional[str],
        day: Optional[str],
        slot: Optional[int]
    ) -> List[Dict[str, Any]]:

        if not room:
            return []

        # Try QueryEngine's room schedule.
        records = self.call_engine_method(
            "room_schedule",
            room=room,
            day=day
        )

        records = self.result_to_list(
            records
        )

        records = self.filter_day(
            records,
            day
        )

        records = self.filter_slot(
            records,
            slot
        )

        return records

    # =========================================================
    # MAIN EXECUTE METHOD
    # =========================================================

    def execute(
        self,
        query: str
    ) -> Dict[str, Any]:

        query = self.normalize_text(
            query
        )

        if not query:

            return {
                "intent": "unknown",
                "success": False,
                "count": 0,
                "results": [],
                "message": (
                    "Please enter a timetable question."
                ),
            }

        # -----------------------------------------------------
        # Extract entities
        # -----------------------------------------------------

        day = self.extract_day(
            query
        )

        slot = self.extract_slot(
            query
        )

        teacher = self.extract_teacher(
            query
        )

        class_name = self.extract_class(
            query
        )

        room = self.extract_room(
            query
        )

        subject = self.extract_subject(
            query
        )

        # -----------------------------------------------------
        # Detect intent
        # -----------------------------------------------------

        intent = self.detect_intent(
            query
        )

        # -----------------------------------------------------
        # Execute intent
        # -----------------------------------------------------

        if intent == "faculty_free":

            results = self.execute_faculty_free(
                day,
                slot
            )

        elif intent == "faculty_status":

            results = self.execute_faculty_status(
                teacher,
                day,
                slot
            )

        elif intent == "teacher_schedule":

            results = self.execute_teacher_schedule(
                teacher,
                day
            )

        elif intent == "subject_search":

            results = self.execute_subject_search(
                subject
            )

        elif intent == "class_schedule":

            results = self.execute_class_schedule(
                class_name,
                day
            )

        elif intent == "room_free":

            results = self.execute_room_free(
                room,
                day,
                slot
            )

        elif intent == "class_free":

            results = self.execute_class_free(
                day,
                slot
            )

        elif intent == "room_status":

            results = self.execute_room_status(
                room,
                day,
                slot
            )

        else:

            return {
                "intent": "unknown",
                "success": False,
                "count": 0,
                "results": [],
                "message": (
                    "I could not understand the query. "
                    "Try asking about faculty, classes, "
                    "rooms, subjects, schedules, or free slots."
                ),
            }

        results = self.result_to_list(
            results
        )

        return {
            "intent": intent,
            "success": True,
            "count": len(results),
            "results": results,

            "day": day,
            "slot": slot,
            "teacher": teacher,
            "class_name": class_name,
            "room": room,
            "subject": subject,
        }

    # =========================================================
    # FRIENDLY ANSWER
    # =========================================================

    def answer(
        self,
        query: str
    ) -> str:

        result = self.execute(
            query
        )

        if not result.get(
            "success",
            False
        ):
            return result.get(
                "message",
                "I could not understand the query."
            )

        intent = result.get(
            "intent"
        )

        records = result.get(
            "results",
            []
        )

        count = result.get(
            "count",
            len(records)
        )

        day = result.get(
            "day"
        )

        slot = result.get(
            "slot"
        )

        teacher = result.get(
            "teacher"
        )

        # -----------------------------------------------------
        # Faculty free
        # -----------------------------------------------------

        if intent == "faculty_free":

            if not records:

                return (
                    f"No faculty member is free"
                    f"{' on ' + day if day else ''}"
                    f"{' at slot ' + str(slot) if slot else ''}."
                )

            names = []

            seen = set()

            for record in records:

                name = self.field(
                    record,
                    "teacher"
                )

                name = self.normalize_text(
                    name
                )

                if (
                    name
                    and name.lower() not in seen
                ):

                    seen.add(
                        name.lower()
                    )

                    names.append(
                        name
                    )

            if not names:

                return f"{count} free slot(s) found."

            return (
                f"Found {len(names)} free faculty member(s):\n"
                + "\n".join(
                    f"- {name}"
                    for name in names
                )
            )

        # -----------------------------------------------------
        # Faculty status
        # -----------------------------------------------------

        if intent == "faculty_status":

            if records:

                return (
                    f"{teacher} is busy"
                    f"{' on ' + day if day else ''}"
                    f"{', slot ' + str(slot) if slot else ''}."
                )

            return (
                f"{teacher} appears to be free"
                f"{' on ' + day if day else ''}"
                f"{', slot ' + str(slot) if slot else ''}."
            )

        # -----------------------------------------------------
        # Teacher schedule
        # -----------------------------------------------------

        if intent == "teacher_schedule":

            if not records:

                return (
                    f"No scheduled events found for "
                    f"{teacher}"
                    f"{' on ' + day if day else ''}."
                )

            lines = [
                f"Found {len(records)} scheduled event(s):"
            ]

            for record in records:

                lines.append(
                    "- "
                    + self.normalize_text(
                        self.field(
                            record,
                            "day"
                        )
                    )
                    + " | Slot "
                    + str(
                        self.field(
                            record,
                            "slot"
                        )
                    )
                    + " | "
                    + self.normalize_text(
                        self.field(
                            record,
                            "subject"
                        )
                    )
                    + " | Room: "
                    + self.normalize_text(
                        self.field(
                            record,
                            "room"
                        )
                    )
                    + " | Class: "
                    + self.normalize_text(
                        self.field(
                            record,
                            "class_name",
                            "class"
                        )
                    )
                )

            return "\n".join(lines)

        # -----------------------------------------------------
        # Subject search
        # -----------------------------------------------------

        if intent == "subject_search":

            teachers = []

            seen = set()

            for record in records:

                name = self.normalize_text(
                    self.field(
                        record,
                        "teacher"
                    )
                )

                if (
                    name
                    and name.lower() not in seen
                ):

                    seen.add(
                        name.lower()
                    )

                    teachers.append(
                        name
                    )

            if not teachers:

                return (
                    f"No faculty found teaching "
                    f"{subject}."
                )

            return (
                f"Faculty teaching this subject "
                f"({len(teachers)}):\n"
                + "\n".join(
                    f"- {name}"
                    for name in teachers
                )
            )

        # -----------------------------------------------------
        # Class schedule
        # -----------------------------------------------------

        if intent == "class_schedule":

            if not records:

                return (
                    f"No scheduled events found for "
                    f"{class_name}"
                    f"{' on ' + day if day else ''}."
                )

            lines = [
                f"Found {len(records)} scheduled event(s):"
            ]

            for record in records:

                lines.append(
                    "- "
                    + self.normalize_text(
                        self.field(
                            record,
                            "day"
                        )
                    )
                    + " | Slot "
                    + str(
                        self.field(
                            record,
                            "slot"
                        )
                    )
                    + " | "
                    + self.normalize_text(
                        self.field(
                            record,
                            "subject"
                        )
                    )
                    + " | Teacher: "
                    + self.normalize_text(
                        self.field(
                            record,
                            "teacher"
                        )
                    )
                    + " | Room: "
                    + self.normalize_text(
                        self.field(
                            record,
                            "room"
                        )
                    )
                )

            return "\n".join(lines)

        # -----------------------------------------------------
        # Room free
        # -----------------------------------------------------

        if intent == "room_free":

            if not records:

                return (
                    "No free room found"
                    f"{' on ' + day if day else ''}"
                    f"{', slot ' + str(slot) if slot else ''}."
                )

            rooms = []

            seen = set()

            for record in records:

                value = self.normalize_text(
                    self.field(
                        record,
                        "room"
                    )
                )

                if (
                    value
                    and value.lower() not in seen
                ):

                    seen.add(
                        value.lower()
                    )

                    rooms.append(
                        value
                    )

            if not rooms:

                return (
                    f"Found {len(records)} free room slot(s)."
                )

            return (
                f"Found {len(rooms)} free room(s):\n"
                + "\n".join(
                    f"- {room}"
                    for room in rooms
                )
            )

        # -----------------------------------------------------
        # Class free
        # -----------------------------------------------------

        if intent == "class_free":

            if not records:

                return (
                    "No free class slot found"
                    f"{' on ' + day if day else ''}"
                    f"{', slot ' + str(slot) if slot else ''}."
                )

            classes = []

            seen = set()

            for record in records:

                value = self.normalize_text(
                    self.field(
                        record,
                        "class_name",
                        "class"
                    )
                )

                if (
                    value
                    and value.lower() not in seen
                ):

                    seen.add(
                        value.lower()
                    )

                    classes.append(
                        value
                    )

            return (
                f"Found {len(classes)} free class(es):\n"
                + "\n".join(
                    f"- {value}"
                    for value in classes
                )
            )

        # -----------------------------------------------------
        # Room status
        # -----------------------------------------------------

        if intent == "room_status":

            if not records:

                return (
                    f"No schedule found for room {room}"
                    f"{' on ' + day if day else ''}"
                    f"{', slot ' + str(slot) if slot else ''}."
                )

            lines = [
                f"Found {len(records)} scheduled event(s):"
            ]

            for record in records:

                lines.append(
                    "- "
                    + self.normalize_text(
                        self.field(
                            record,
                            "day"
                        )
                    )
                    + " | Slot "
                    + str(
                        self.field(
                            record,
                            "slot"
                        )
                    )
                    + " | "
                    + self.normalize_text(
                        self.field(
                            record,
                            "subject"
                        )
                    )
                    + " | Teacher: "
                    + self.normalize_text(
                        self.field(
                            record,
                            "teacher"
                        )
                    )
                )

            return "\n".join(lines)

        return (
            "Query processed successfully."
        )


# =============================================================
# BACKWARD-COMPATIBILITY ALIAS
# =============================================================

NLQuery = NaturalLanguageQuery