from os import remove, unlink
from pathlib import Path
from datetime import datetime
from shutil import copy2
import sqlite3

print("\n")

# main program files
# uncomment for proj_dir in user's home dir
# proj_dir = Path.home()/"todo-txt"
proj_dir = Path(__file__).parent.resolve()
print(Path(__file__).parents[1])
db_file = proj_dir / "todo_db.sqlite3"
# todo_file = proj_dir / "todo.txt"
# config_file = proj_dir / "config.ini"
attachments_dir = proj_dir / "attachments"


# check if files exists and create if not
def check_exist(mode="r"):
    if proj_dir.exists():
        print("main directory is there")
    else:
        proj_dir.mkdir()
        print("main directory created")
    if attachments_dir.exists():
        print("attachments directory is there")
    else:
        attachments_dir.mkdir()
        print("attachments directory created")
    # if config_file.exists():
    #     print("config is there")
    # else:
    #     config_file.touch()
    #     print("config created")
    # if todo_file.exists():
    #     print("file is there")
    # else:
    #     todo_file.touch()
    #     print("todo file created")
    if db_file.exists():
        print("db file is there\n")
    else:
        db_file.touch()
        print("db file created\n")


check_exist()

# new_task = {
#     "task_id": None,
#     "completed": 0,
#     "task": "task1 text",
#     "priority": "",
#     "project": "project1",
#     "context": "context1",
#     "date": "2023-12-16",
#     "attachment": "link to attachment",
#     "date_modified": str(datetime.utcnow()),
# }

# with open(todo_file, "a") as f:
#     print(new_task, file=f)

conn = sqlite3.connect(db_file)
cur = conn.cursor()


cur.execute(
    """CREATE TABLE IF NOT EXISTS tasks(
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        completed INT DEFAULT None,
        task TEXT DEFAULT None,
        priority TEXT DEFAULT None,
        project TEXT DEFAULT None,
        context TEXT DEFAULT None,
        date TEXT DEFAULT None,
        attachment TEXT DEFAULT None,
        date_modified TEXT UNIQUE);
"""
)
conn.commit()

# cur.execute(
#     """CREATE TABLE IF NOT EXISTS metadata(
#    task_id INT PRIMARY KEY,
#    date_created TEXT);
# """
# )
# conn.commit()

new_task = {
    "task_id": None,
    "completed": None,
    "task": "task1 text",
    "priority": None,
    "project": None,
    "context": None,
    "date": "2023-12-16",
    # "attachment": str(Path(__file__).parents[1] / "тест вложения 1.txt"),
    # "attachment": str(Path(__file__).parents[1] / "py03.pdf"),
    "attachment": None,
    "date_modified": str(datetime.utcnow()),
}


def add_task(new_task):
    add_query = f"""INSERT INTO tasks VALUES({", ".join("?"*len(new_task.keys()))})"""
    if new_task["attachment"] != None:
        copy2(Path(new_task["attachment"]), attachments_dir)
        new_task["attachment"] = Path(new_task["attachment"]).name

    cur.execute(add_query, list(new_task.values()))
    conn.commit()
    print("+++ row added")
    # print(add_query, list(new_task.values()))


# add_task(new_task)


changed_task = {
    "task": "upd text",
    "completed": None,
    "priority": None,
    "project": None,
    "context": None,
    "date": "2023-12-26",
    "attachment": str(Path(__file__).parents[1] / "тест вложения 1.txt"),
    # "attachment": str(Path(__file__).parents[1] / "py03.pdf"),
    # "attachment": None,
    "date_modified": str(datetime.utcnow()),
}


def update_task(changed_task, task_id):
    # разберемся с вложением
    cur.execute("SELECT attachment FROM tasks WHERE task_id = ?", [task_id])
    attachment_in_db = cur.fetchone()[0]
    cur.execute(
        "SELECT task_id FROM tasks WHERE attachment =? LIMIT 2", [attachment_in_db]
    )
    count_in_db = len(cur.fetchall())

    if attachment_in_db != None and changed_task["attachment"] is None:
        if count_in_db <= 1:
            Path(attachments_dir / attachment_in_db).unlink()
    elif (
        attachment_in_db != None
        and attachment_in_db != Path(changed_task["attachment"]).name
    ):
        if count_in_db <= 1:
            Path(attachments_dir / attachment_in_db).unlink()
        copy2(changed_task["attachment"], attachments_dir)
        changed_task["attachment"] = Path(changed_task["attachment"]).name
    elif attachment_in_db is None and changed_task["attachment"] != None:
        copy2(changed_task["attachment"], attachments_dir)
        changed_task["attachment"] = Path(changed_task["attachment"]).name

    update_query = (
        f"""UPDATE tasks SET {"=?, ".join(changed_task.keys())}=? WHERE task_id=?"""
    )
    update_args = list(changed_task.values()) + [task_id]
    cur.execute(update_query, update_args)
    conn.commit()
    print(f"Строка #{task_id} обновлена")
    # print(update_query, "\n", update_args)


# update_task(changed_task, 1)


def del_task(task_id):
    cur.execute("DELETE FROM tasks where task_id=?", [task_id])
    conn.commit()
    print(f"строка #{task_id} удалена")


# del_task(input("номер записи для удаления: "))


def get_info(task_id):
    get_query = """SELECT * FROM tasks WHERE task_id = ?"""
    cur.execute(get_query, [task_id])
    print(cur.fetchone())


# get_info(1)

# очищаем таблицу и обнуляем инкремент ключевого поля
# cur.execute("DELETE FROM tasks")
# cur.execute("delete from sqlite_sequence where name='tasks'")
# conn.commit()

# удаляем таблицы
# cur.execute("DROP TABLE metadata")
# cur.execute("DROP TABLE tasks")
# conn.commit()

cur.execute("SELECT * FROM tasks")
print("\nВсего строк в БД:", len(cur.fetchall()))
conn.execute("VACUUM")
conn.close()
print("Соединение SQLite закрыто")
