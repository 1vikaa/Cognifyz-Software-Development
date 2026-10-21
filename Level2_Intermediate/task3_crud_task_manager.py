"""
Cognifyz Technologies - Software Development Internship
Level 2 - Task 3: Console application for CRUD operations on a list of tasks

Data is stored in memory using a Python list.
"""

from datetime import date


class Task:
    def __init__(self, task_id, title, description="", priority="Medium",
                 due_date="", completed=False):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = completed

    def __str__(self):
        status = "Done" if self.completed else "Pending"
        due = self.due_date or "-"
        return (f"[{self.task_id}] {self.title} | Priority: {self.priority} | "
                f"Due: {due} | Status: {status}\n     {self.description}")


class TaskManager:
    PRIORITIES = ("Low", "Medium", "High")

    def __init__(self):
        self.tasks = []
        self.next_id = 1

    # CREATE
    def create_task(self, title, description="", priority="Medium", due_date=""):
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        if priority not in self.PRIORITIES:
            raise ValueError(f"Priority must be one of {self.PRIORITIES}.")
        if due_date:
            date.fromisoformat(due_date)  # raises ValueError if invalid
        task = Task(self.next_id, title.strip(), description.strip(), priority, due_date)
        self.tasks.append(task)
        self.next_id += 1
        return task

    # READ
    def get_all_tasks(self):
        return list(self.tasks)

    def find_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    # UPDATE
    def update_task(self, task_id, title=None, description=None,
                    priority=None, due_date=None, completed=None):
        task = self.find_task(task_id)
        if task is None:
            raise KeyError(f"Task {task_id} not found.")
        if title is not None:
            if not title.strip():
                raise ValueError("Title cannot be empty.")
            task.title = title.strip()
        if description is not None:
            task.description = description.strip()
        if priority is not None:
            if priority not in self.PRIORITIES:
                raise ValueError(f"Priority must be one of {self.PRIORITIES}.")
            task.priority = priority
        if due_date is not None:
            if due_date:
                date.fromisoformat(due_date)
            task.due_date = due_date
        if completed is not None:
            task.completed = completed
        return task

    # DELETE
    def delete_task(self, task_id):
        task = self.find_task(task_id)
        if task is None:
            raise KeyError(f"Task {task_id} not found.")
        self.tasks.remove(task)
        return task


# ---------------- Console interface ----------------

def ask_priority(default="Medium"):
    value = input(f"Priority (Low/Medium/High) [{default}]: ").strip().capitalize()
    return value or default


def ask_int(prompt):
    value = input(prompt).strip()
    if not value.isdigit():
        print("Please enter a valid number.")
        return None
    return int(value)


def show_tasks(manager):
    tasks = manager.get_all_tasks()
    if not tasks:
        print("No tasks yet.")
        return
    print(f"\n--- {len(tasks)} task(s) ---")
    for task in tasks:
        print(task)


def run_console(manager, on_change=None):
    """Main menu loop. on_change is called after every modification
    (used by the Level 3 version to save to a file)."""
    menu = """
========== TASK MANAGER ==========
 1. Add task
 2. View all tasks
 3. Update task
 4. Mark task as completed
 5. Delete task
 0. Exit
=================================="""
    while True:
        print(menu)
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                title = input("Title: ")
                desc = input("Description: ")
                priority = ask_priority()
                due = input("Due date (YYYY-MM-DD, optional): ").strip()
                task = manager.create_task(title, desc, priority, due)
                print(f"Task {task.task_id} created.")
                if on_change: on_change()

            elif choice == "2":
                show_tasks(manager)

            elif choice == "3":
                show_tasks(manager)
                task_id = ask_int("ID of task to update: ")
                if task_id is None:
                    continue
                task = manager.find_task(task_id)
                if task is None:
                    print("Task not found.")
                    continue
                print("Press Enter to keep the current value.")
                title = input(f"Title [{task.title}]: ") or None
                desc = input(f"Description [{task.description}]: ") or None
                priority = ask_priority(task.priority)
                due = input(f"Due date [{task.due_date}]: ").strip() or None
                manager.update_task(task_id, title, desc, priority, due)
                print("Task updated.")
                if on_change: on_change()

            elif choice == "4":
                task_id = ask_int("ID of task to mark completed: ")
                if task_id is None:
                    continue
                manager.update_task(task_id, completed=True)
                print("Task marked as completed.")
                if on_change: on_change()

            elif choice == "5":
                task_id = ask_int("ID of task to delete: ")
                if task_id is None:
                    continue
                confirm = input(f"Delete task {task_id}? (y/n): ").strip().lower()
                if confirm == "y":
                    manager.delete_task(task_id)
                    print("Task deleted.")
                    if on_change: on_change()

            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")
        except (ValueError, KeyError) as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    run_console(TaskManager())
