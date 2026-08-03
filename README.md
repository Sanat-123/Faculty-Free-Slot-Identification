# 🎓 Faculty Free Slot Identification

NLP-powered chatbot that identifies free faculty, teachers, subjects, rooms and
timetables from **faculty timetable PDFs**.

## ✨ PDF Chatbot (upload a PDF and chat)

The quickest way to use the project: upload a faculty-wise timetable PDF and ask
questions in plain English.

```bash
pip install -r requirements.txt
streamlit run pdf_chatbot_app.py
```

Then open **http://localhost:8501** in your browser.

- 📄 Upload any faculty-wise timetable PDF (one page per teacher, starting with
  `Teacher <Name>`, with a Mo–Sa / slot 1–8 table — same format as
  `data/Facultywise TT 20 sep.pdf`)
- 💬 Or click **📥 Load sample PDF** to try it instantly with the bundled timetable
- 🤖 Ask things like:
  - *"Who is free on Monday slot 3?"*
  - *"Who teaches Python?"*
  - *"Show timetable of 3CS-DS-A"*
  - *"Where is Python for DS Lab?"*
  - *"Subjects of Dr. Pankaj Dadheech"*
  - *"Which rooms are free on Tuesday slot 4?"*
  - *"Who is busy on Friday slot 2?"*

### How it works

```
Uploaded PDF
   │  pdf_pipeline.parse_faculty_pdf()   (pdfplumber + CellParser)
   ▼
{teacher: {day: [{slot, subject, room, class, group, type}]}}
   │  pdf_pipeline.build_database()      (fresh SQLite DB, same schema as faculty.db)
   ▼
temporary .db  ── pdf_pipeline.activate()  re-points database.db_manager.DB_FILE
   │
   ▼
Your question  ── engine pipeline ──►  QueryTokenizer → StopWordFilter
                                        → DaySlotExtractor → EntityExtractor
                                        → IntentDetector → QueryPlanner
                                        → ResponseGenerator  →  answer
```

The uploaded PDF is parsed into a **temporary** SQLite database, so the
project's own `database/faculty.db` and JSON files are never modified.

## 🧪 Tests

```bash
python test_pdf_chatbot_app.py     # end-to-end chatbot test (Streamlit AppTest)
python pdf_pipeline.py             # pipeline smoke test on the sample PDF
python test_query_planner.py       # core NLP engine test
```

## 🗂️ Project structure (main pieces)

| Path            | Purpose                                                |
|-----------------|--------------------------------------------------------|
| `pdf_chatbot_app.py` | Streamlit chat UI with PDF upload (the chatbot)   |
| `pdf_pipeline.py`    | PDF → SQLite ingestion + chat answering pipeline   |
| `parser/`           | PDF reading and timetable cell parsing/cleaning      |
| `database/`         | SQLite `faculty.db`, repositories, knowledge loader  |
| `engine/`           | NLP pipeline (intent, entities, day/slot, planner)   |
| `data/`             | Sample timetable PDFs                                |
| `chatbot/`          | Earlier chatbot experiments (analytics / CLI bots)   |
