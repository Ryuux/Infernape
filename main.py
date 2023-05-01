import argparse
import sqlite3
from prettytable import PrettyTable
from termcolor import colored

class TaskManager:
    def __init__(self):
        self.conn = sqlite3.connect('tasks.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                deadline TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_task(self, description, deadline):
        self.cursor.execute('INSERT INTO tasks (description, deadline) VALUES (?, ?)', (description, deadline))
        self.conn.commit()
        print(colored(f"Task '{description}' added successfully!", 'green'))

    def delete_task(self, task_id):
        self.cursor.execute('SELECT description FROM tasks WHERE id = ?', (task_id,))
        task = self.cursor.fetchone()
        if task is not None:
            self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            self.conn.commit()
            print(colored(f"Task '{task[0]}' deleted successfully!", 'green'))
        else:
            print(colored("Invalid task ID", 'red'))

    def edit_task(self, task_id, new_description, new_deadline):
        self.cursor.execute('SELECT description FROM tasks WHERE id = ?', (task_id,))
        task = self.cursor.fetchone()
        if task is not None:
            self.cursor.execute('UPDATE tasks SET description = ?, deadline = ? WHERE id = ?', (new_description, new_deadline, task_id))
            self.conn.commit()
            print(colored(f"Task '{new_description}' edited successfully!", 'green'))
        else:
            print(colored("Invalid task ID", 'red'))

    def show_tasks(self):
        self.cursor.execute('SELECT * FROM tasks')
        tasks = self.cursor.fetchall()
        if len(tasks) > 0:
            print(colored("Current tasks:", 'yellow'))
            x = PrettyTable()
            x.field_names = [colored("ID", 'blue'), colored("Description", 'blue'), colored("Deadline", 'blue')]
            for task in tasks:
                x.add_row([task[0], task[1], task[2]])
            print(x)
        else:
            print(colored("No tasks found", 'yellow'))

parser = argparse.ArgumentParser(description='Manage your tasks')
parser.add_argument('--add', nargs=2, type=str, help='Add a new task with description and deadline')
parser.add_argument('--delete', type=int, help='Delete a task by ID')
parser.add_argument('--edit', nargs=3, type=str, help='Edit a task by ID with new description and deadline')
parser.add_argument('--show', action='store_true', help='Show current tasks')
args = parser.parse_args()

task_manager = TaskManager()

if args.add:
    task_manager.add_task(args.add[0], args.add[1])
elif args.delete is not None:
    task_manager.delete_task(args.delete)
elif args.edit:
    task_manager.edit_task(int(args.edit[0]), args.edit[1], args.edit[2])
elif args.show:
    task_manager.show_tasks()
else:
    parser.print_help()

task_manager.conn.close()
