import csv
import random
from faker import Faker
from pathlib import Path

fake = Faker("en_IN")

BASE_DIR = Path(__file__).resolve().parent.parent

RAW = BASE_DIR / "data" / "raw"

RAW.mkdir(parents=True, exist_ok=True)


faculty = []

designations = [
    "Assistant Professor",
    "Associate Professor",
    "Professor"
]

departments = [
    "D001",
    "D002",
    "D003",
    "D004",
    "D005"
]

for i in range(1,1001):

    faculty.append([

        f"F{i:04d}",
        fake.name(),
        random.choice(designations),
        random.choice(departments),
        fake.email(),
        fake.phone_number()[:10],
        random.randint(2,25)

    ])

with open(RAW/"faculty.csv","w",newline="",encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "faculty_id",
        "faculty_name",
        "designation",
        "department_id",
        "email",
        "phone",
        "experience"
    ])

    writer.writerows(faculty)

print("✅ faculty.csv (1000 Records) created successfully!")

subjects = []

subject_names = [
    "Programming in C",
    "Programming in Python",
    "Programming in Java",
    "Object Oriented Programming",
    "Data Structures",
    "Algorithms",
    "Operating Systems",
    "Database Management System",
    "Computer Networks",
    "Software Engineering",
    "Compiler Design",
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Cloud Computing",
    "Big Data",
    "Cyber Security",
    "Data Mining",
    "Data Analytics",
    "Computer Graphics",
    "Digital Logic",
    "Engineering Mathematics",
    "Statistics",
    "Discrete Mathematics",
    "Microprocessors"
]

courses = [
    "C001","C002","C003","C004","C005",
    "C006","C007","C008","C009","C010"
]

for i in range(1,1001):

    subjects.append([

        f"SUB{i:04d}",
        random.choice(subject_names),
        random.randint(1,8),
        random.randint(2,5),
        random.choice(courses)

    ])

with open(RAW/"subjects.csv","w",newline="",encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "subject_id",
        "subject_name",
        "semester",
        "credits",
        "course_id"
    ])

    writer.writerows(subjects)

print("✅ subjects.csv (1000 Records) created successfully!")


attendance = []

status = ["Present","Absent","Leave"]

for i in range(1,50001):

    attendance.append([

        i,
        f"S{random.randint(1,1000):04d}",
        f"SUB{random.randint(1,1000):04d}",
        fake.date_between("-365d","today"),
        random.choice(status)

    ])

with open(RAW/"attendance.csv","w",newline="",encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "attendance_id",
        "student_id",
        "subject_id",
        "date",
        "status"
    ])

    writer.writerows(attendance)

print("✅ attendance.csv (50000 Records) created successfully!")


results = []

grades = ["A+", "A", "B+", "B", "C", "D", "F"]

for i in range(1,10001):

    marks = random.randint(35,100)

    results.append([

        i,
        f"S{random.randint(1,1000):04d}",
        f"SUB{random.randint(1,1000):04d}",
        marks,
        random.choice(grades),
        random.randint(2022,2026),
        random.randint(1,8)

    ])

with open(RAW/"results.csv","w",newline="",encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([
        "result_id",
        "student_id",
        "subject_id",
        "marks",
        "grade",
        "year",
        "semester"
    ])

    writer.writerows(results)

print("✅ results.csv (10000 Records) created successfully!")

# -----------------------------
# FEES DATA
# -----------------------------

fees = []

status = ["Paid", "Pending", "Partial"]

for i in range(1,1001):

    fees.append([

        f"FEE{i:04d}",
        f"S{i:04d}",
        random.choice([50000,65000,70000,80000,90000]),
        random.choice(status),
        fake.date_between(
            start_date="-2y",
            end_date="today"
        )

    ])

with open(RAW/"fees.csv","w",newline="",encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([

        "fee_id",
        "student_id",
        "amount",
        "status",
        "payment_date"

    ])

    writer.writerows(fees)

print("✅ fees.csv (1000 Records) created successfully!")


# -----------------------------
# LIBRARY BOOKS DATA
# -----------------------------

book_titles = [

    "Operating Systems",
    "Database Management Systems",
    "Computer Networks",
    "Artificial Intelligence",
    "Machine Learning",
    "Python Programming",
    "Java Programming",
    "Data Structures",
    "Algorithms",
    "Compiler Design",
    "Digital Logic",
    "Cloud Computing",
    "Cyber Security",
    "Data Mining",
    "Big Data",
    "Software Engineering",
    "Discrete Mathematics",
    "Microprocessors",
    "Statistics",
    "Deep Learning"

]

authors = [

    "Silberschatz",
    "Galvin",
    "Tanenbaum",
    "Stallings",
    "Korth",
    "Cormen",
    "Goodfellow",
    "Sutton",
    "Ross",
    "James"

]

publishers = [

    "Pearson",
    "McGraw Hill",
    "Springer",
    "Oxford",
    "Wiley"

]

books = []

for i in range(1,5001):

    books.append([

        f"B{i:05d}",
        random.choice(book_titles),
        random.choice(authors),
        random.choice(publishers),
        random.randint(2010,2026)

    ])

with open(RAW/"library_books.csv","w",newline="",encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([

        "book_id",
        "book_name",
        "author",
        "publisher",
        "publication_year"

    ])

    writer.writerows(books)

print("✅ library_books.csv (5000 Records) created successfully!")



# -----------------------------
# LIBRARY TRANSACTIONS DATA
# -----------------------------

transactions = []

status_list = [
    "Issued",
    "Returned",
    "Late Return"
]

for i in range(1,20001):

    issue_date = fake.date_between(
        start_date="-2y",
        end_date="today"
    )

    transactions.append([

        f"T{i:05d}",
        f"S{random.randint(1,1000):04d}",
        f"B{random.randint(1,5000):05d}",
        issue_date,
        fake.date_between(
            start_date=issue_date,
            end_date="+30d"
        ),
        random.choice(status_list)

    ])

with open(RAW/"library_transactions.csv",
          "w",
          newline="",
          encoding="utf-8") as f:

    writer = csv.writer(f)

    writer.writerow([

        "transaction_id",
        "student_id",
        "book_id",
        "issue_date",
        "return_date",
        "status"

    ])

    writer.writerows(transactions)

print("✅ library_transactions.csv (20000 Records) created successfully!")

# -----------------------------
# PLACEMENTS DATA
# -----------------------------

companies = [

    "Google",
    "Microsoft",
    "Amazon",
    "Infosys",
    "TCS",
    "Wipro",
    "Accenture",
    "Oracle",
    "IBM",
    "Adobe",
    "Deloitte",
    "Capgemini",
    "HCL",
    "Cisco",
    "Intel"

]

placements = []

for i in range(1,1001):

    placements.append([

        f"P{i:04d}",
        f"S{i:04d}",
        random.choice(companies),
        random.choice([
            "Software Engineer",
            "Data Engineer",
            "Data Analyst",
            "ML Engineer",
            "Backend Developer",
            "Cloud Engineer"
        ]),
        random.randint(4,40),
        random.choice([2024,2025,2026])

    ])

with open(
    RAW/"placements.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([

        "placement_id",
        "student_id",
        "company_name",
        "job_role",
        "package_lpa",
        "placement_year"

    ])

    writer.writerows(placements)

print("✅ placements.csv (1000 Records) created successfully!")

# -----------------------------
# HOSTEL DATA
# -----------------------------

hostels = []

hostel_names = [
    "Boys Hostel A",
    "Boys Hostel B",
    "Girls Hostel A",
    "Girls Hostel B"
]

for i in range(1,501):

    hostels.append([

        f"H{i:04d}",
        random.choice(hostel_names),
        random.randint(101,450),
        random.choice([
            "Single",
            "Double",
            "Triple"
        ]),
        f"S{random.randint(1,1000):04d}"

    ])

with open(
    RAW/"hostel.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([

        "hostel_id",
        "hostel_name",
        "room_number",
        "room_type",
        "student_id"

    ])

    writer.writerows(hostels)

print("✅ hostel.csv (500 Records) created successfully!")


# -----------------------------
# TIMETABLE DATA
# -----------------------------

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday"
]

slots = [
    "09:00-10:00",
    "10:00-11:00",
    "11:15-12:15",
    "12:15-01:15",
    "02:00-03:00",
    "03:00-04:00"
]

rooms = []

for i in range(101,151):
    rooms.append(f"A{i}")

for i in range(201,251):
    rooms.append(f"B{i}")

timetable = []

for i in range(1,2001):

    timetable.append([

        f"TT{i:04d}",
        random.choice(days),
        random.choice(slots),
        f"SUB{random.randint(1,1000):04d}",
        f"F{random.randint(1,1000):04d}",
        random.choice(rooms)

    ])

with open(
    RAW/"timetable.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([

        "timetable_id",
        "day",
        "time_slot",
        "subject_id",
        "faculty_id",
        "room"

    ])

    writer.writerows(timetable)

print("✅ timetable.csv (2000 Records) created successfully!")


# -----------------------------
# EXAM SCHEDULE DATA
# -----------------------------

exam_types = [
    "Mid Semester",
    "End Semester",
    "Practical"
]

exam_schedule = []

for i in range(1,1001):

    exam_schedule.append([

        f"E{i:04d}",
        f"SUB{random.randint(1,1000):04d}",
        fake.date_between(
            start_date="-180d",
            end_date="+180d"
        ),
        random.choice([
            "09:00 AM",
            "02:00 PM"
        ]),
        random.choice([
            "Hall A",
            "Hall B",
            "Hall C",
            "Hall D",
            "Hall E"
        ]),
        random.choice(exam_types)

    ])

with open(
    RAW/"exam_schedule.csv",
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.writer(f)

    writer.writerow([

        "exam_id",
        "subject_id",
        "exam_date",
        "exam_time",
        "exam_hall",
        "exam_type"

    ])

    writer.writerows(exam_schedule)

print("✅ exam_schedule.csv (1000 Records) created successfully!")