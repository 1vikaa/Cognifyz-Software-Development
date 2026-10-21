# Cognifyz Technologies – Software Development Internship

All 6 tasks completed in Python 3 (only 4 of 6 are required).

| Level | Task | File | How to run |
|---|---|---|---|
| 1 Beginner | Task 1 – Text-based game (Number Guessing) | `Level1_Beginner/task1_number_guessing_game.py` | `python task1_number_guessing_game.py` |
| 1 Beginner | Task 2 – Number patterns | `Level1_Beginner/task2_number_patterns.py` | `python task2_number_patterns.py` |
| 2 Intermediate | Task 3 – CRUD task manager (in-memory list) | `Level2_Intermediate/task3_crud_task_manager.py` | `python task3_crud_task_manager.py` |
| 2 Intermediate | Task 4 – Temperature converter | `Level2_Intermediate/task4_temperature_converter.py` | `python task4_temperature_converter.py` |
| 3 Advanced | Task 5 – CRUD with file storage (`tasks.txt`) | `Level3_Advanced/task5_crud_with_file_storage.py` | `python task5_crud_with_file_storage.py` (add `--test` to run persistence tests) |
| 3 Advanced | Task 6 – Interactive web scraper | `Level3_Advanced/task6_web_scraper.py` | `pip install requests beautifulsoup4` then `python task6_web_scraper.py` |

## Features
- **Task 1:** 3 difficulty levels, limited attempts, too high/too low hints, scoring, input validation, replay.
- **Task 2:** 5 patterns (triangle, pyramid, inverted, Floyd's, Pascal's) built with nested loops, with built-in correctness checks.
- **Task 3:** `Task` class (id, title, description, priority, due date, status). Create, view, update, mark complete and delete, with validation.
- **Task 4:** C ↔ F ↔ K conversions, choice of direction, rejects values below absolute zero, built-in tests.
- **Task 5:** Extends Task 3. Auto-saves to a text file after every change, uses atomic writes, escapes special characters, skips and backs up corrupted lines.
- **Task 6:** Scrapes quotes (filter by tag) and books (sort by price or rating), plus headings and links from any URL. Shows results in tables, handles pagination and network errors, and can export to CSV.

#cognifyz #cognifyzTech #cognifyzTechnologies
