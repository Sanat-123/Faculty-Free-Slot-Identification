from dataset_manager.universal_dataset import UniversalDataset


print("=" * 70)
print("UNISCHED AI - UNIVERSAL DATASET TEST")
print("=" * 70)


dataset = UniversalDataset()


# ----------------------------------------------------------
# PDF RECORD
# ----------------------------------------------------------

pdf_records = [

    {
        "teacher": "Dr. Mehul Mahrishi",
        "day": "Monday",
        "slot": 1,
        "slot_time": "8:15 - 9:15",
        "subject": "Project/Spoken-Latex IAI",
        "room": "",
        "class_name": "7CSA",
        "source_file": "Facultywise TT 20 sep.pdf",
        "source_type": "pdf",
        "source_page": 1,
    },

    {
        "teacher": "Dr. Mehul Mahrishi",
        "day": "Monday",
        "slot": 2,
        "slot_time": "9:15 - 10:15",
        "subject": "",
        "room": "",
        "class_name": "",
        "source_file": "Facultywise TT 20 sep.pdf",
        "source_type": "pdf",
        "source_page": 1,
    },

]


dataset.add_records(
    pdf_records
)


# ----------------------------------------------------------
# EXCEL RECORD
# ----------------------------------------------------------

excel_records = [

    {
        "teacher": "Dr. Niketa Sharma",
        "subject": "DE Lab",
        "room": "7F:EE-Lab13",
        "class_name": "3CS A",
        "group_name": "Group 2",
        "type": "Lab",
        "length": "Triple",
        "lessons_per_week": 1,
        "available_classrooms":
            "Shared room, ECL-08, 7F:EE-Lab13",
        "cycle": "All weeks",
        "source_file": "timetable.xlsx",
        "source_type": "excel",
    }

]


dataset.add_records(
    excel_records
)


# ----------------------------------------------------------
# CSV RECORD
# ----------------------------------------------------------

csv_records = [

    {
        "teacher": "Dr. Arpita Sharma",
        "subject": "SE Lab",
        "room": "CL-22",
        "class_name": "3CS A",
        "group_name": "Group 1",
        "type": "Lab",
        "length": "Triple",
        "lessons_per_week": 1,
        "source_file":
            "test_timetable.csv",
        "source_type":
            "csv",
    }

]


dataset.add_records(
    csv_records
)


# ----------------------------------------------------------
# SUMMARY
# ----------------------------------------------------------

summary = dataset.summary()


print()
print("DATASET SUMMARY")
print("-" * 70)

print(
    "Total records:",
    summary["record_count"]
)

print(
    "Total source files:",
    summary["source_file_count"]
)

print(
    "Teachers:",
    summary["teacher_count"]
)

print(
    "Subjects:",
    summary["subject_count"]
)

print(
    "Classes:",
    summary["class_count"]
)

print(
    "Rooms:",
    summary["room_count"]
)


print()
print("SOURCE FILES")

for source in summary[
    "source_files"
]:

    print(
        "  ✓",
        source
    )


print()
print("AVAILABLE FIELDS")

for field in summary[
    "available_fields"
]:

    print(
        "  ✓",
        field
    )


print()
print("=" * 70)
print("UNIVERSAL DATASET TEST PASSED")
print("=" * 70)