import pytest
from datetime import date, datetime, timedelta
from task_manager import TaskManager, Task, Priority
import os

@pytest.fixture
def task_manager():
    return TaskManager()

@pytest.fixture
def sample_task():
    return Task(
        title="Test Task",
        description="This is a test task",
        priority=Priority.MEDIUM,
        due_date=date.today() + timedelta(days=1)
    )

def test_add_task(task_manager, sample_task):
    task_id = task_manager.add_task(sample_task)
    assert task_id == 1
    assert task_manager.get_task(task_id) == sample_task
    assert sample_task.id == task_id

def test_complete_task(task_manager, sample_task):
    task_id = task_manager.add_task(sample_task)
    assert not sample_task.completed
    assert task_manager.complete_task(task_id)
    assert sample_task.completed
    assert sample_task.completed_at is not None

def test_delete_task(task_manager, sample_task):
    task_id = task_manager.add_task(sample_task)
    assert task_manager.delete_task(task_id)
    assert task_manager.get_task(task_id) is None

def test_get_tasks_by_priority(task_manager):
    # Add tasks with different priorities
    high_task = Task("High", "High priority task", Priority.HIGH, date.today())
    med_task = Task("Medium", "Medium priority task", Priority.MEDIUM, date.today())
    low_task = Task("Low", "Low priority task", Priority.LOW, date.today())
    
    task_manager.add_task(high_task)
    task_manager.add_task(med_task)
    task_manager.add_task(low_task)
    
    high_priority_tasks = task_manager.get_tasks_by_priority(Priority.HIGH)
    assert len(high_priority_tasks) == 1
    assert high_priority_tasks[0] == high_task

def test_get_overdue_tasks(task_manager):
    # Create tasks with different due dates
    overdue_task = Task(
        "Overdue",
        "This task is overdue",
        Priority.HIGH,
        date.today() - timedelta(days=1)
    )
    future_task = Task(
        "Future",
        "This task is not due yet",
        Priority.LOW,
        date.today() + timedelta(days=1)
    )
    
    task_manager.add_task(overdue_task)
    task_manager.add_task(future_task)
    
    overdue_tasks = task_manager.get_overdue_tasks()
    assert len(overdue_tasks) == 1
    assert overdue_tasks[0] == overdue_task

def test_save_and_load(task_manager, sample_task):
    filename = "test_tasks.json"
    task_id = task_manager.add_task(sample_task)
    task_manager.complete_task(task_id)
    
    # Save tasks to file
    task_manager.save_to_file(filename)
    
    # Create new task manager and load tasks
    new_manager = TaskManager()
    new_manager.load_from_file(filename)
    
    # Verify loaded task matches original
    loaded_task = new_manager.get_task(task_id)
    assert loaded_task.title == sample_task.title
    assert loaded_task.description == sample_task.description
    assert loaded_task.priority == sample_task.priority
    assert loaded_task.completed == sample_task.completed
    
    # Cleanup
    os.remove(filename) 