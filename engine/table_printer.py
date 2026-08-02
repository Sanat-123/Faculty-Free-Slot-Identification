from rich.console import Console
from rich.table import Table

console = Console()


def print_timetable(rows, title):

    table = Table(
        title=title,
        show_lines=True,
        expand=True
    )

    table.add_column("Teacher", style="cyan", no_wrap=True)
    table.add_column("Day", style="green")
    table.add_column("Slot", justify="center", no_wrap=True)
    table.add_column("Subject", style="yellow")
    table.add_column("Location", justify="center")
    table.add_column("Class", no_wrap=True)
    table.add_column("Type", justify="center", no_wrap=True)

    for teacher, day, slot, subject_name, room, class_name, group_name, class_type in rows:

        display_subject = subject_name

        if class_type == "Lab" and group_name:
            display_subject = f"{subject_name} ({group_name})"

        table.add_row(
            teacher,
            day,
            str(slot),
            display_subject,
            room,
            class_name,
            class_type
        )

    console.print(table)

    print(f"\nTotal Records : {len(rows)}")