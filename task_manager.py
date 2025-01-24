from datetime import datetime, date
from typing import List, Dict, Optional
from enum import Enum
import json

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Task:
    def __init__(
        self,
        title: str,
        description: str,
        priority: Priority,
        due_date: Optional[date] = None
    ):
        self.id = None  # Will be set by TaskManager
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = False
        self.created_at = datetime.now()
        self.completed_at = None

    def to_dict(self) -> Dict:
        """Convert task to dictionary for serialization"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority.name,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class TaskManager:
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self._last_id = 0

    def add_task(self, task: Task) -> int:
        """Add a new task and return its ID"""
        self._last_id += 1
        task.id = self._last_id
        self.tasks[task.id] = task
        return task.id

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID"""
        return self.tasks.get(task_id)

    def complete_task(self, task_id: int) -> bool:
        """Mark a task as complete"""
        task = self.get_task(task_id)
        if task and not task.completed:
            task.completed = True
            task.completed_at = datetime.now()
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """Get all tasks with specified priority"""
        return [task for task in self.tasks.values() if task.priority == priority]

    def get_overdue_tasks(self) -> List[Task]:
        """Get all overdue and incomplete tasks"""
        today = date.today()
        return [
            task for task in self.tasks.values()
            if task.due_date and task.due_date < today and not task.completed
        ]

    def save_to_file(self, filename: str):
        """Save tasks to JSON file"""
        with open(filename, 'w') as f:
            json_data = {str(tid): task.to_dict() for tid, task in self.tasks.items()}
            json.dump(json_data, f, indent=2)

    def load_from_file(self, filename: str):
        """Load tasks from JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                for task_dict in data.values():
                    task = Task(
                        title=task_dict['title'],
                        description=task_dict['description'],
                        priority=Priority[task_dict['priority']],
                        due_date=date.fromisoformat(task_dict['due_date']) if task_dict['due_date'] else None
                    )
                    task.id = task_dict['id']
                    task.completed = task_dict['completed']
                    task.created_at = datetime.fromisoformat(task_dict['created_at'])
                    task.completed_at = (datetime.fromisoformat(task_dict['completed_at']) 
                                       if task_dict['completed_at'] else None)
                    self.tasks[task.id] = task
        except FileNotFoundError:
            pass  # Ignore if file doesn't exist 