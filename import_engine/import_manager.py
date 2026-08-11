"""
==========================================================
UNISCHED AI - UNIVERSAL IMPORT MANAGER
==========================================================

Purpose
-------
Universal entry point for importing user-uploaded:

    PDF
    XLSX
    XLS
    CSV

The manager automatically detects the file type and
calls the appropriate importer.

Architecture:

    User File
        |
        v
    ImportManager
        |
        +---- PDFImporter
        |
        +---- ExcelImporter
        |
        +---- CSVImporter
        |
        v
    Universal Records

The manager does NOT depend on a particular university,
teacher name, subject, class, room, or timetable format.

==========================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from import_engine.pdf_importer import PDFImporter
from import_engine.excel_importer import ExcelImporter
from import_engine.csv_importer import CSVImporter


class ImportManager:

    # ======================================================
    # SUPPORTED FILE TYPES
    # ======================================================

    SUPPORTED_EXTENSIONS = {

        ".pdf": "pdf",

        ".xlsx": "xlsx",

        ".xls": "xls",

        ".csv": "csv",

    }

    # ======================================================
    # CONSTRUCTOR
    # ======================================================

    def __init__(self):

        self.imported_files: List[str] = []

        self.failed_files: List[str] = []

    # ======================================================
    # DETECT FILE TYPE
    # ======================================================

    @staticmethod
    def detect_file_type(
        file_path: str | Path
    ) -> str:

        path = Path(
            file_path
        )

        extension = (
            path.suffix
            .lower()
        )

        return ImportManager.SUPPORTED_EXTENSIONS.get(
            extension,
            "unknown"
        )

    # ======================================================
    # VALIDATE FILE
    # ======================================================

    @staticmethod
    def validate_file(
        file_path: str | Path
    ) -> Dict[str, Any]:

        path = Path(
            file_path
        )

        # --------------------------------------------------
        # Does file exist?
        # --------------------------------------------------

        if not path.exists():

            return {

                "valid":
                    False,

                "filename":
                    path.name,

                "extension":
                    path.suffix.lower(),

                "size_bytes":
                    0,

                "implemented":
                    False,

                "reason":
                    "File does not exist."

            }

        # --------------------------------------------------
        # Must be a file
        # --------------------------------------------------

        if not path.is_file():

            return {

                "valid":
                    False,

                "filename":
                    path.name,

                "extension":
                    path.suffix.lower(),

                "size_bytes":
                    0,

                "implemented":
                    False,

                "reason":
                    "Path is not a file."

            }

        # --------------------------------------------------
        # Extension
        # --------------------------------------------------

        extension = (
            path.suffix
            .lower()
        )

        # --------------------------------------------------
        # File size
        # --------------------------------------------------

        size_bytes = path.stat().st_size

        if size_bytes <= 0:

            return {

                "valid":
                    False,

                "filename":
                    path.name,

                "extension":
                    extension,

                "size_bytes":
                    size_bytes,

                "implemented":
                    extension
                    in ImportManager.SUPPORTED_EXTENSIONS,

                "reason":
                    "File is empty."

            }

        # --------------------------------------------------
        # Supported?
        # --------------------------------------------------

        if extension not in (
            ImportManager.SUPPORTED_EXTENSIONS
        ):

            return {

                "valid":
                    False,

                "filename":
                    path.name,

                "extension":
                    extension,

                "size_bytes":
                    size_bytes,

                "implemented":
                    False,

                "reason":
                    (
                        "Unsupported file type: "
                        f"{extension}"
                    )

            }

        # --------------------------------------------------
        # Valid
        # --------------------------------------------------

        return {

            "valid":
                True,

            "filename":
                path.name,

            "extension":
                extension,

            "size_bytes":
                size_bytes,

            "implemented":
                True,

            "reason":
                None

        }

    # ======================================================
    # IMPORT FILE
    # ======================================================

    def import_file(
        self,
        file_path: str | Path
    ) -> Dict[str, Any]:

        """
        Import one file.

        Returns:

            {
                "success": True,
                "filename": "...",
                "file_type": "pdf",
                "records": [...],
                "record_count": 123,
                "inspection": {...},
                "warnings": [...]
            }
        """

        path = Path(
            file_path
        )

        # --------------------------------------------------
        # Validate
        # --------------------------------------------------

        validation = self.validate_file(
            path
        )

        if not validation["valid"]:

            self.failed_files.append(
                path.name
            )

            return {

                "success":
                    False,

                "filename":
                    path.name,

                "file_type":
                    self.detect_file_type(
                        path
                    ),

                "records":
                    [],

                "record_count":
                    0,

                "inspection":
                    None,

                "warnings":
                    [
                        validation[
                            "reason"
                        ]
                    ],

                "error":
                    validation[
                        "reason"
                    ],

            }

        # --------------------------------------------------
        # Detect type
        # --------------------------------------------------

        file_type = (
            self.detect_file_type(
                path
            )
        )

        try:

            # ==================================================
            # PDF
            # ==================================================

            if file_type == "pdf":

                importer = PDFImporter()

                records = importer.import_file(
                    path
                )

                inspection = importer.inspect_file(
                    path
                )

            # ==================================================
            # EXCEL
            # ==================================================

            elif file_type in (
                "xlsx",
                "xls"
            ):

                importer = ExcelImporter()

                records = importer.import_file(
                    path
                )

                # Some Excel importers may provide
                # inspect_file(). If not, inspection
                # will simply be None.

                if hasattr(
                    importer,
                    "inspect_file"
                ):

                    inspection = importer.inspect_file(
                        path
                    )

                else:

                    inspection = None

            # ==================================================
            # CSV
            # ==================================================

            elif file_type == "csv":

                importer = CSVImporter()

                records = importer.import_file(
                    path
                )

                if hasattr(
                    importer,
                    "inspect_file"
                ):

                    inspection = importer.inspect_file(
                        path
                    )

                else:

                    inspection = None

            # ==================================================
            # UNKNOWN
            # ==================================================

            else:

                raise ValueError(
                    (
                        "Unsupported file type: "
                        f"{path.suffix}"
                    )
                )

            # --------------------------------------------------
            # Make sure records is a list
            # --------------------------------------------------

            if records is None:

                records = []

            elif isinstance(
                records,
                tuple
            ):

                records = list(
                    records
                )

            elif not isinstance(
                records,
                list
            ):

                records = list(
                    records
                )

            # --------------------------------------------------
            # Success
            # --------------------------------------------------

            self.imported_files.append(
                path.name
            )

            # --------------------------------------------------
            # Generate warnings
            # --------------------------------------------------

            warnings = []

            if inspection:

                if (
                    inspection.get(
                        "has_day"
                    ) is False
                ):

                    warnings.append(
                        "Dataset does not contain Day information."
                    )

                if (
                    inspection.get(
                        "has_slot"
                    ) is False
                ):

                    warnings.append(
                        "Dataset does not contain Slot information."
                    )

            return {

                "success":
                    True,

                "filename":
                    path.name,

                "file_type":
                    file_type,

                "records":
                    records,

                "record_count":
                    len(records),

                "inspection":
                    inspection,

                "warnings":
                    warnings,

                "error":
                    None,

            }

        except Exception as error:

            self.failed_files.append(
                path.name
            )

            return {

                "success":
                    False,

                "filename":
                    path.name,

                "file_type":
                    file_type,

                "records":
                    [],

                "record_count":
                    0,

                "inspection":
                    None,

                "warnings":
                    [],

                "error":
                    str(error),

            }

    # ======================================================
    # IMPORT MULTIPLE FILES
    # ======================================================

    def import_files(
        self,
        file_paths: List[
            str | Path
        ]
    ) -> Dict[str, Any]:

        """
        Import multiple user files.

        Example:

            manager.import_files([
                "faculty.pdf",
                "class.pdf",
                "timetable.xlsx",
                "timetable.csv"
            ])
        """

        results = []

        all_records = []

        for file_path in file_paths:

            result = self.import_file(
                file_path
            )

            results.append(
                result
            )

            if result[
                "success"
            ]:

                all_records.extend(
                    result[
                        "records"
                    ]
                )

        return {

            "success":
                all(
                    result[
                        "success"
                    ]
                    for result in results
                )
                if results
                else False,

            "files":
                results,

            "records":
                all_records,

            "record_count":
                len(
                    all_records
                ),

            "file_count":
                len(
                    results
                ),

            "successful_files":
                len(
                    [
                        result
                        for result in results
                        if result[
                            "success"
                        ]
                    ]
                ),

            "failed_files":
                len(
                    [
                        result
                        for result in results
                        if not result[
                            "success"
                        ]
                    ]
                ),

        }

    # ======================================================
    # RESET
    # ======================================================

    def reset(self):

        self.imported_files.clear()

        self.failed_files.clear()


# ==========================================================
# DIRECT TEST
# ==========================================================

if __name__ == "__main__":

    print("=" * 80)

    print(
        "UNISCHED AI - IMPORT MANAGER"
    )

    print("=" * 80)

    manager = ImportManager()

    print()

    print(
        "Supported file types:"
    )

    for extension in (
        ImportManager.SUPPORTED_EXTENSIONS
    ):

        print(
            "  ✓",
            extension
        )

    print()

    print(
        "Import Manager loaded successfully."
    )

    print("=" * 80)