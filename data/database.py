import platform
import sqlite3
from pathlib import Path


class Database:
    def __init__(self):
        if platform.system() == "Android":
            from android.storage import primary_external_storage_path

            primary_ext_storage = Path(primary_external_storage_path())
            cutt_data_dir = Path(primary_ext_storage / "Clean up the tasks")
        else:
            cutt_data_dir = Path.home() / "Clean up the tasks"

        self.con = sqlite3.connect(cutt_data_dir / "todo.db")
        self.cursor = self.con.cursor()
        self.create_task_table()  # create the tasks table

    def create_task_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS tasks(id integer PRIMARY KEY AUTOINCREMENT, task varchar(50) NOT NULL, due_date varchar(50), completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)))"
        )
        self.con.commit()

    def create_task(self, task, due_date=None):
        self.cursor.execute(
            "INSERT INTO tasks(task, due_date, completed) VALUES(?, ?, ?)",
            (task, due_date, 0),
        )
        self.con.commit()

        # GETTING THE LAST ENTERED ITEM SO WE CAN ADD IT TO THE TASK LIST
        created_task = self.cursor.execute(
            "SELECT id, task, due_date FROM tasks WHERE task = ? and completed = 0",
            (task,),
        ).fetchall()
        return created_task[-1]

    def update_task(self, taskid, task, due_date):
        self.cursor.execute(
            "UPDATE tasks SET task=?, due_date=? WHERE id=?",
            (task, due_date, taskid),
        )
        self.con.commit()

    def get_tasks(self):
        uncomplete_tasks = self.cursor.execute(
            "SELECT id, task, due_date FROM tasks WHERE completed = 0 ORDER BY due_date ASC"
        ).fetchall()
        completed_tasks = self.cursor.execute(
            "SELECT id, task, due_date FROM tasks WHERE completed = 1"
        ).fetchall()
        # return the tasks to be added to the list when the application starts
        return completed_tasks, uncomplete_tasks

    def get_task_data(self, taskid):
        task_data = self.cursor.execute(
            "SELECT id, completed, task, due_date FROM tasks WHERE id = ? ORDER BY due_date ASC",
            (taskid,),
        ).fetchone()
        return task_data

    def mark_task_as_complete(self, taskid):
        self.cursor.execute("UPDATE tasks SET completed=1 WHERE id=?", (taskid,))
        self.con.commit()

    def mark_task_as_incomplete(self, taskid):
        self.cursor.execute("UPDATE tasks SET completed=0 WHERE id=?", (taskid,))
        self.con.commit()

        # return the task text
        task_text = self.cursor.execute(
            "SELECT task FROM tasks WHERE id=?", (taskid,)
        ).fetchall()
        return task_text[0][0]

    def delete_task(self, taskid):
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (taskid,))
        self.con.commit()

    def close_db_connection(self):
        self.con.close()
