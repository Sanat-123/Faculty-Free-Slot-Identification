from automation.project_manager import ProjectManager


ProjectManager.create_project(

    project_name="SKIT_2026",

    university="SKIT Jaipur",

    academic_year="2026-27"

)

print()

print(ProjectManager.list_projects())

print()

print(ProjectManager.get_metadata("SKIT_2026"))