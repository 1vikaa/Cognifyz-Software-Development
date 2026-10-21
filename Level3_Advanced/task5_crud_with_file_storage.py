"""
Cognifyz Technologies - Software Development Internship
Level 3 - Task 5: CRUD application with persistent file storage

Extends the Task 3 task manager so tasks are saved to and loaded
from a text file (tasks.txt). Each line holds one task, with fields
separated by '|'. Any '|' or newline in user text is escaped.
"""

import os
import shutil
import sys

# Reuse the Task / TaskManager classes from Level 2
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "Level2_Intermediate"))
from task3_crud_task_manager import Task, TaskManager, run_console  # noqa: E402

DEFAULT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.txt")
SEPARATOR = "|"


def escape(text):
    return text.replace("\\", "\\\\").replace("|", "\\p").replace("\n", "\\n")


def unescape(text):
    result, i = [], 0
    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text):
            nxt = text[i + 1]
            result.append({"\\": "\\", "p": "|", "n": "\n"}.get(nxt, nxt))
            i += 2
        else:
            result.append(text[i])
            i += 1
    return "".join(result)


class FileTaskManager(TaskManager):
    def __init__(self, file_path=DEFAULT_FILE):
        super().__init__()
        self.file_path = file_path
        self.load()

    def save(self):
        """Write all tasks to a temp file, then replace the real file,
        so a crash mid-write never corrupts existing data."""
        temp_path = self.file_path + ".tmp"
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                for t in self.tasks:
                    fields = [str(t.task_id), escape(t.title), escape(t.description),
                              t.priority, t.due_date, "1" if t.completed else "0"]
                    f.write(SEPARATOR.join(fields) + "\n")
            os.replace(temp_path, self.file_path)
        except OSError as e:
            print(f"Error: could not save tasks to '{self.file_path}': {e}")

    def load(self):
        """Load tasks from the file. Skips (and reports) corrupted lines."""
        if not os.path.exists(self.file_path):
            return
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except OSError as e:
            print(f"Error: could not read '{self.file_path}': {e}")
            return

        bad_lines = 0
        for line_no, line in enumerate(lines, start=1):
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split(SEPARATOR)
            try:
                if len(parts) != 6:
                    raise ValueError("wrong number of fields")
                task = Task(int(parts[0]), unescape(parts[1]), unescape(parts[2]),
                            parts[3], parts[4], parts[5] == "1")
                self.tasks.append(task)
            except ValueError as e:
                bad_lines += 1
                print(f"Warning: skipped line {line_no} in tasks file ({e}).")

        if bad_lines:
            backup = self.file_path + ".bak"
            shutil.copy(self.file_path, backup)
            print(f"A backup of the original file was saved to '{backup}'.")

        if self.tasks:
            self.next_id = max(t.task_id for t in self.tasks) + 1
        print(f"Loaded {len(self.tasks)} task(s) from '{os.path.basename(self.file_path)}'.")


def test_persistence():
    """Create tasks, reload from file, and check the data survived."""
    import tempfile
    path = os.path.join(tempfile.mkdtemp(), "test_tasks.txt")

    m1 = FileTaskManager(path)
    m1.create_task("Buy milk", "2 litres | full cream", "Low")
    m1.create_task("Finish report", "Line one\nLine two", "High", "2026-12-31")
    m1.save()
    m1.update_task(1, completed=True)
    m1.delete_task(2)
    m1.create_task("Call mom")
    m1.save()

    m2 = FileTaskManager(path)
    assert len(m2.tasks) == 2
    assert m2.find_task(1).completed is True
    assert m2.find_task(1).description == "2 litres | full cream"
    assert m2.find_task(2) is None
    assert m2.find_task(3).title == "Call mom"
    assert m2.next_id == 4

    with open(path, "a", encoding="utf-8") as f:
        f.write("this line is corrupted\n")
    m3 = FileTaskManager(path)
    assert len(m3.tasks) == 2
    print("Persistence tests passed.\n")


if __name__ == "__main__":
    if "--test" in sys.argv:
        test_persistence()
    else:
        manager = FileTaskManager()
        run_console(manager, on_change=manager.save)
