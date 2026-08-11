"""
==========================================================
UniSched AI Platform
Project Manager
==========================================================

Responsible for

• Creating Projects
• Opening Projects
• Deleting Projects
• Project Metadata
• Project Folder Structure

Author:
UniSched AI Team
==========================================================
"""

from pathlib import Path
import json
from datetime import datetime
from typing import List


class ProjectManager:

    ROOT = Path("projects")

    REQUIRED_FOLDERS = [
        "uploads",
        "cache",
        "logs",
        "exports",
        "temp"
    ]

    DEFAULT_FILES = {
        "chat_history.json": [],
        "analytics.json": {},
        "settings.json": {},
    }

    @classmethod
    def initialize(cls):
        """
        Create root project folder if missing.
        """

        cls.ROOT.mkdir(exist_ok=True)

    @classmethod
    def project_exists(cls, project_name: str) -> bool:

        return (cls.ROOT / project_name).exists()

    @classmethod
    def create_project(
        cls,
        project_name: str,
        university: str,
        academic_year: str
    ) -> Path:

        cls.initialize()

        project = cls.ROOT / project_name

        if project.exists():

            raise FileExistsError(
                f"Project '{project_name}' already exists."
            )

        project.mkdir()

        for folder in cls.REQUIRED_FOLDERS:

            (project / folder).mkdir()

        # Create empty database placeholder
        (project / "database.db").touch()

        # Metadata

        metadata = {

            "project_name": project_name,

            "university": university,

            "academic_year": academic_year,

            "created_at": datetime.now().isoformat(),

            "last_opened": datetime.now().isoformat(),

            "status": "CREATED"

        }

        with open(
            project / "metadata.json",
            "w",
            encoding="utf8"
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4
            )

        # Default files

        for filename, content in cls.DEFAULT_FILES.items():

            with open(
                project / filename,
                "w",
                encoding="utf8"
            ) as file:

                json.dump(
                    content,
                    file,
                    indent=4
                )

        return project

    @classmethod
    def list_projects(cls) -> List[str]:

        cls.initialize()

        return sorted(

            [

                folder.name

                for folder in cls.ROOT.iterdir()

                if folder.is_dir()

            ]

        )

    @classmethod
    def get_metadata(cls, project_name: str):

        metadata_file = (
            cls.ROOT
            / project_name
            / "metadata.json"
        )

        if not metadata_file.exists():

            return None

        with open(
            metadata_file,
            encoding="utf8"
        ) as file:

            return json.load(file)

    @classmethod
    def update_last_opened(cls, project_name: str):

        metadata = cls.get_metadata(project_name)

        if metadata is None:

            return

        metadata["last_opened"] = datetime.now().isoformat()

        with open(
            cls.ROOT / project_name / "metadata.json",
            "w",
            encoding="utf8"
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4
            )

    @classmethod
    def delete_project(cls, project_name: str):

        import shutil

        project = cls.ROOT / project_name

        if project.exists():

            shutil.rmtree(project)