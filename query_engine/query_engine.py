"""
UNISCHED AI - QUERY ENGINE

Purpose:
    Provides a query layer on top of CanonicalEventMatcher.

The Query Engine does NOT:
    - read PDF files
    - read Excel files
    - read CSV files
    - perform data fusion
    - perform canonical event matching

Those responsibilities are handled by the existing project modules.

This module only queries the canonical data.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


class QueryEngine:
    """
    Query layer for UNISCHED AI.

    Parameters
    ----------
    matcher:
        A processed CanonicalEventMatcher instance.
    """

    def __init__(self, matcher: Any):

        if matcher is None:
            raise ValueError(
                "QueryEngine requires a CanonicalEventMatcher."
            )

        self.matcher = matcher

    # =========================================================
    # GENERIC HELPERS
    # =========================================================

    @staticmethod
    def _clean(value: Any) -> str:
        """Clean display text."""

        if value is None:
            return ""

        return " ".join(
            str(value)
            .replace("\xa0", " ")
            .strip()
            .split()
        )

    @staticmethod
    def _normalize(value: Any) -> str:
        """Normalize text for comparison."""

        return QueryEngine._clean(value).lower()

    @staticmethod
    def _get(
        record: Dict[str, Any],
        *keys: str
    ) -> Any:
        """
        Safely retrieve a field using multiple possible names.
        """

        if not isinstance(record, dict):
            return ""

        for key in keys:

            if key in record:

                value = record[key]

                if value is not None:
                    return value

        return ""

    @classmethod
    def _day(cls, value: Any) -> str:
        """Normalize day names."""

        if not value:
            return ""

        text = cls._normalize(value)

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

        return mapping.get(text, text)

    @classmethod
    def _slot(cls, value: Any) -> Optional[Any]:
        """Normalize slot numbers."""

        if value is None:
            return None

        text = cls._clean(value)

        if not text:
            return None

        try:

            number = float(text)

            if number.is_integer():
                return int(number)

            return number

        except (ValueError, TypeError):

            return text.lower()

    @classmethod
    def _same_day(
        cls,
        a: Any,
        b: Any
    ) -> bool:

        return cls._day(a) == cls._day(b)

    @classmethod
    def _same_slot(
        cls,
        a: Any,
        b: Any
    ) -> bool:

        return cls._slot(a) == cls._slot(b)

    @classmethod
    def _contains(
        cls,
        value: Any,
        query: Any
    ) -> bool:
        """Case-insensitive substring matching."""

        value_text = cls._normalize(value)
        query_text = cls._normalize(query)

        if not value_text or not query_text:
            return False

        return query_text in value_text

    # =========================================================
    # MATCHER ACCESS
    # =========================================================

    def _events(self) -> List[Dict[str, Any]]:
        """Get canonical scheduled events."""

        try:

            return list(
                self.matcher.get_events()
            )

        except Exception:

            return list(
                getattr(
                    self.matcher,
                    "events",
                    []
                )
            )

    def _faculty_free(self) -> List[Dict[str, Any]]:
        """Get faculty free slots."""

        try:

            return list(
                self.matcher.get_faculty_free_slots()
            )

        except Exception:

            return list(
                getattr(
                    self.matcher,
                    "faculty_free_slots",
                    []
                )
            )

    def _class_free(self) -> List[Dict[str, Any]]:
        """Get class free slots."""

        try:

            return list(
                self.matcher.get_class_free_slots()
            )

        except Exception:

            return list(
                getattr(
                    self.matcher,
                    "class_free_slots",
                    []
                )
            )

    def _room_free(self) -> List[Dict[str, Any]]:
        """Get room free slots."""

        try:

            return list(
                self.matcher.get_room_free_slots()
            )

        except Exception:

            return list(
                getattr(
                    self.matcher,
                    "room_free_slots",
                    []
                )
            )

    def _contracts(self) -> List[Dict[str, Any]]:
        """Get contract records."""

        try:

            return list(
                self.matcher.get_contract_records()
            )

        except Exception:

            return list(
                getattr(
                    self.matcher,
                    "contract_records",
                    []
                )
            )

    # =========================================================
    # FACULTY FREE SLOTS
    # =========================================================

    def faculty_free_slots(
        self,
        teacher: Optional[str] = None,
        day: Optional[str] = None,
        slot: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Find faculty free slots.

        Examples:

            engine.faculty_free_slots(
                day="Monday",
                slot=2
            )

            engine.faculty_free_slots(
                teacher="Dr. Mehul Mahrishi",
                day="Monday",
                slot=2
            )
        """

        results = []

        for record in self._faculty_free():

            record_teacher = self._get(
                record,
                "teacher",
                "faculty"
            )

            record_day = self._get(
                record,
                "day"
            )

            record_slot = self._get(
                record,
                "slot"
            )

            if teacher:

                if not self._contains(
                    record_teacher,
                    teacher
                ):
                    continue

            if day:

                if not self._same_day(
                    record_day,
                    day
                ):
                    continue

            if slot is not None:

                if not self._same_slot(
                    record_slot,
                    slot
                ):
                    continue

            results.append(record)

        return {
            "query_type": "faculty_free",
            "teacher": teacher,
            "day": self._day(day) if day else None,
            "slot": self._slot(slot),
            "count": len(results),
            "results": results,
        }

    # =========================================================
    # TEACHER SCHEDULE
    # =========================================================

    def teacher_schedule(
        self,
        teacher: str,
        day: Optional[str] = None,
        slot: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Find scheduled classes for a teacher."""

        results = []

        for event in self._events():

            record_teacher = self._get(
                event,
                "teacher",
                "faculty"
            )

            if not self._contains(
                record_teacher,
                teacher
            ):
                continue

            record_day = self._get(
                event,
                "day"
            )

            record_slot = self._get(
                event,
                "slot"
            )

            if day:

                if not self._same_day(
                    record_day,
                    day
                ):
                    continue

            if slot is not None:

                if not self._same_slot(
                    record_slot,
                    slot
                ):
                    continue

            results.append(event)

        return {
            "query_type": "teacher_schedule",
            "teacher": teacher,
            "day": self._day(day) if day else None,
            "slot": self._slot(slot),
            "count": len(results),
            "results": results,
        }

    # =========================================================
    # CLASS SCHEDULE
    # =========================================================

    def class_schedule(
        self,
        class_name: str,
        day: Optional[str] = None,
        slot: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Find scheduled events for a class."""

        results = []

        for event in self._events():

            record_class = self._get(
                event,
                "class_name",
                "class"
            )

            if not self._contains(
                record_class,
                class_name
            ):
                continue

            record_day = self._get(
                event,
                "day"
            )

            record_slot = self._get(
                event,
                "slot"
            )

            if day:

                if not self._same_day(
                    record_day,
                    day
                ):
                    continue

            if slot is not None:

                if not self._same_slot(
                    record_slot,
                    slot
                ):
                    continue

            results.append(event)

        return {
            "query_type": "class_schedule",
            "class_name": class_name,
            "day": self._day(day) if day else None,
            "slot": self._slot(slot),
            "count": len(results),
            "results": results,
        }

    # =========================================================
    # CLASS FREE SLOTS
    # =========================================================

    def class_free_slots(
        self,
        class_name: Optional[str] = None,
        day: Optional[str] = None,
        slot: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Find class free slots."""

        results = []

        for record in self._class_free():

            record_class = self._get(
                record,
                "class_name",
                "class"
            )

            record_day = self._get(
                record,
                "day"
            )

            record_slot = self._get(
                record,
                "slot"
            )

            if class_name:

                if not self._contains(
                    record_class,
                    class_name
                ):
                    continue

            if day:

                if not self._same_day(
                    record_day,
                    day
                ):
                    continue

            if slot is not None:

                if not self._same_slot(
                    record_slot,
                    slot
                ):
                    continue

            results.append(record)

        return {
            "query_type": "class_free",
            "class_name": class_name,
            "day": self._day(day) if day else None,
            "slot": self._slot(slot),
            "count": len(results),
            "results": results,
        }

    # =========================================================
    # ROOM SCHEDULE
    # =========================================================

    def room_schedule(
        self,
        room: str,
        day: Optional[str] = None,
        slot: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Find events scheduled in a room."""

        results = []

        for event in self._events():

            record_room = self._get(
                event,
                "room",
                "classroom"
            )

            if not self._contains(
                record_room,
                room
            ):
                continue

            record_day = self._get(
                event,
                "day"
            )

            record_slot = self._get(
                event,
                "slot"
            )

            if day:

                if not self._same_day(
                    record_day,
                    day
                ):
                    continue

            if slot is not None:

                if not self._same_slot(
                    record_slot,
                    slot
                ):
                    continue

            results.append(event)

        return {
            "query_type": "room_schedule",
            "room": room,
            "day": self._day(day) if day else None,
            "slot": self._slot(slot),
            "count": len(results),
            "results": results,
        }

    # =========================================================
    # ROOM FREE SLOTS
    # =========================================================

    def room_free_slots(
        self,
        room: Optional[str] = None,
        day: Optional[str] = None,
        slot: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Find room free slots."""

        results = []

        for record in self._room_free():

            record_room = self._get(
                record,
                "room",
                "classroom"
            )

            record_day = self._get(
                record,
                "day"
            )

            record_slot = self._get(
                record,
                "slot"
            )

            if room:

                if not self._contains(
                    record_room,
                    room
                ):
                    continue

            if day:

                if not self._same_day(
                    record_day,
                    day
                ):
                    continue

            if slot is not None:

                if not self._same_slot(
                    record_slot,
                    slot
                ):
                    continue

            results.append(record)

        return {
            "query_type": "room_free",
            "room": room,
            "day": self._day(day) if day else None,
            "slot": self._slot(slot),
            "count": len(results),
            "results": results,
        }

    # =========================================================
    # SUBJECT SEARCH
    # =========================================================

    def subject_search(
        self,
        subject: str
    ) -> Dict[str, Any]:
        """Search scheduled and contract records by subject."""

        results = []

        for event in self._events():

            record_subject = self._get(
                event,
                "subject"
            )

            if self._contains(
                record_subject,
                subject
            ):
                results.append(event)

        for record in self._contracts():

            record_subject = self._get(
                record,
                "subject"
            )

            if self._contains(
                record_subject,
                subject
            ):
                results.append(record)

        return {
            "query_type": "subject_search",
            "subject": subject,
            "count": len(results),
            "results": results,
        }

    # =========================================================
    # TEACHER SEARCH
    # =========================================================

    def teacher_search(
        self,
        teacher: str
    ) -> Dict[str, Any]:
        """Search scheduled and contract records by teacher."""

        results = []

        for event in self._events():

            record_teacher = self._get(
                event,
                "teacher",
                "faculty"
            )

            if self._contains(
                record_teacher,
                teacher
            ):
                results.append(event)

        for record in self._contracts():

            record_teacher = self._get(
                record,
                "teacher",
                "faculty"
            )

            if self._contains(
                record_teacher,
                teacher
            ):
                results.append(record)

        return {
            "query_type": "teacher_search",
            "teacher": teacher,
            "count": len(results),
            "results": results,
        }

    # =========================================================
    # FACULTY STATUS
    # =========================================================

    def faculty_status(
        self,
        teacher: str,
        day: str,
        slot: Any
    ) -> Dict[str, Any]:
        """
        Determine whether a faculty member is busy or free.
        """

        schedule = self.teacher_schedule(
            teacher=teacher,
            day=day,
            slot=slot
        )

        if schedule["count"] > 0:

            return {
                "query_type": "faculty_status",
                "teacher": teacher,
                "day": self._day(day),
                "slot": self._slot(slot),
                "status": "busy",
                "is_free": False,
                "events": schedule["results"],
            }

        free = self.faculty_free_slots(
            teacher=teacher,
            day=day,
            slot=slot
        )

        if free["count"] > 0:

            return {
                "query_type": "faculty_status",
                "teacher": teacher,
                "day": self._day(day),
                "slot": self._slot(slot),
                "status": "free",
                "is_free": True,
                "free_slots": free["results"],
            }

        return {
            "query_type": "faculty_status",
            "teacher": teacher,
            "day": self._day(day),
            "slot": self._slot(slot),
            "status": "unknown",
            "is_free": None,
            "events": [],
            "free_slots": [],
            "message": (
                "No matching scheduled event or explicit "
                "free-slot record was found."
            ),
        }

    # =========================================================
    # GENERAL SEARCH
    # =========================================================

    def search(
        self,
        text: str
    ) -> Dict[str, Any]:
        """
        Simple keyword search across canonical events.
        """

        query = self._normalize(text)

        results = []

        for event in self._events():

            fields = [
                self._get(
                    event,
                    "teacher"
                ),
                self._get(
                    event,
                    "subject"
                ),
                self._get(
                    event,
                    "room"
                ),
                self._get(
                    event,
                    "class_name",
                    "class"
                ),
                self._get(
                    event,
                    "day"
                ),
                self._get(
                    event,
                    "slot"
                ),
            ]

            combined = " ".join(
                self._normalize(field)
                for field in fields
            )

            if query in combined:

                results.append(event)

        return {
            "query_type": "search",
            "query": text,
            "count": len(results),
            "results": results,
        }

    # =========================================================
    # DATASET SUMMARY
    # =========================================================

    def summary(self) -> Dict[str, Any]:
        """Return query-friendly dataset statistics."""

        events = self._events()

        faculty_free = self._faculty_free()

        class_free = self._class_free()

        room_free = self._room_free()

        contracts = self._contracts()

        return {
            "canonical_events": len(events),
            "faculty_free_slots": len(faculty_free),
            "class_free_slots": len(class_free),
            "room_free_slots": len(room_free),
            "contract_records": len(contracts),
        }


__all__ = [
    "QueryEngine"
]