from datetime import date, datetime
from models import Task, Note
from database import DatabaseManager

class TaskService:
    """
    Implements business logic for Task management.
    """
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def add_task(self, task: Task) -> bool:
        """
        Validates and adds a new task to the database.
        """
        if not task.title.strip():
            raise ValueError("Görev başlığı boş olamaz.")
        
        query = """
        INSERT INTO tasks (title, description, category, due_date, priority, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            task.title.strip(),
            task.description.strip(),
            task.category,
            str(task.due_date) if task.due_date else None,
            task.priority,
            task.status
        )
        
        last_id = self.db.execute_non_query(query, params)
        if last_id:
            task.id = last_id
            return True
        return False

    def get_all_tasks(self) -> list:
        """
        Retrieves all tasks from database as Task objects.
        """
        query = "SELECT id, title, description, category, due_date, priority, status FROM tasks ORDER BY id DESC"
        rows = self.db.fetch_all(query)
        return [Task.from_row(row) for row in rows]

    def get_pending_tasks(self) -> list:
        """
        Retrieves pending tasks.
        """
        query = "SELECT id, title, description, category, due_date, priority, status FROM tasks WHERE status = 'Bekliyor' ORDER BY due_date ASC"
        rows = self.db.fetch_all(query)
        return [Task.from_row(row) for row in rows]

    def get_completed_tasks(self) -> list:
        """
        Retrieves completed tasks.
        """
        query = "SELECT id, title, description, category, due_date, priority, status FROM tasks WHERE status = 'Tamamlandı' ORDER BY id DESC"
        rows = self.db.fetch_all(query)
        return [Task.from_row(row) for row in rows]

    def complete_task(self, task_id: int) -> bool:
        """
        Marks task status as Completed ('Tamamlandı').
        """
        query = "UPDATE tasks SET status = 'Tamamlandı' WHERE id = ?"
        return bool(self.db.execute_non_query(query, (task_id,)))

    def delete_task(self, task_id: int) -> bool:
        """
        Deletes task by id.
        """
        query = "DELETE FROM tasks WHERE id = ?"
        return bool(self.db.execute_non_query(query, (task_id,)))

    def get_tasks_due_today(self) -> list:
        """
        Fetches pending tasks that are due today.
        """
        today_str = str(date.today())
        query = """
        SELECT id, title, description, category, due_date, priority, status 
        FROM tasks 
        WHERE status = 'Bekliyor' AND due_date = ?
        """
        rows = self.db.fetch_all(query, (today_str,))
        return [Task.from_row(row) for row in rows]

    def get_tasks_due_tomorrow(self) -> list:
        """
        Fetches pending tasks that are due tomorrow.
        """
        from datetime import timedelta
        tomorrow_str = str(date.today() + timedelta(days=1))
        query = """
        SELECT id, title, description, category, due_date, priority, status 
        FROM tasks 
        WHERE status = 'Bekliyor' AND due_date = ?
        """
        rows = self.db.fetch_all(query, (tomorrow_str,))
        return [Task.from_row(row) for row in rows]


class NoteService:
    """
    Implements business logic for Note management.
    """
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def add_note(self, note: Note) -> bool:
        """
        Validates and adds a new note.
        """
        if not note.title.strip():
            raise ValueError("Not başlığı boş olamaz.")
        
        created_at_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
        INSERT INTO notes (title, content, category, created_at)
        VALUES (?, ?, ?, ?)
        """
        params = (
            note.title.strip(),
            note.content.strip(),
            note.category,
            created_at_str
        )
        
        last_id = self.db.execute_non_query(query, params)
        if last_id:
            note.id = last_id
            note.created_at = created_at_str
            return True
        return False

    def get_all_notes(self) -> list:
        """
        Retrieves all notes as Note objects.
        """
        query = "SELECT id, title, content, category, created_at FROM notes ORDER BY id DESC"
        rows = self.db.fetch_all(query)
        return [Note.from_row(row) for row in rows]

    def delete_note(self, note_id: int) -> bool:
        """
        Deletes a note by id.
        """
        query = "DELETE FROM notes WHERE id = ?"
        return bool(self.db.execute_non_query(query, (note_id,)))