#!/usr/bin/env python3
"""
To-Do List Application (Console-based)
A persistent CLI to-do list manager with file storage.
"""

import os
import json
from datetime import datetime

class TodoApp:
    def __init__(self, filename="tasks.txt"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    if content:
                        # Try to load as JSON first (for enhanced format)
                        try:
                            data = json.loads(content)
                            if isinstance(data, list):
                                self.tasks = data
                            else:
                                # Old format compatibility
                                self.tasks = [{"task": line.strip(), "completed": False, "created": ""} 
                                            for line in content.split('\n') if line.strip()]
                        except json.JSONDecodeError:
                            # Plain text format (backward compatibility)
                            self.tasks = [{"task": line.strip(), "completed": False, "created": ""} 
                                        for line in content.split('\n') if line.strip()]
                    else:
                        self.tasks = []
            else:
                self.tasks = []
                print(f"Creating new task file: {self.filename}")
        except Exception as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to file"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(self.tasks, file, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving tasks: {e}")
            return False
    
    def add_task(self, task_description):
        """Add a new task"""
        if not task_description.strip():
            print("Task description cannot be empty!")
            return False
        
        new_task = {
            "task": task_description.strip(),
            "completed": False,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.tasks.append(new_task)
        if self.save_tasks():
            print(f"✓ Task added: '{task_description}'")
            return True
        else:
            print("✗ Failed to save task")
            return False
    
    def remove_task(self, task_index):
        """Remove a task by index"""
        try:
            if 1 <= task_index <= len(self.tasks):
                removed_task = self.tasks.pop(task_index - 1)
                if self.save_tasks():
                    print(f"✓ Task removed: '{removed_task['task']}'")
                    return True
                else:
                    print("✗ Failed to save changes")
                    return False
            else:
                print(f"Invalid task number! Please enter a number between 1 and {len(self.tasks)}")
                return False
        except Exception as e:
            print(f"Error removing task: {e}")
            return False
    
    def mark_complete(self, task_index):
        """Mark a task as complete"""
        try:
            if 1 <= task_index <= len(self.tasks):
                self.tasks[task_index - 1]["completed"] = True
                if self.save_tasks():
                    print(f"✓ Task marked as complete: '{self.tasks[task_index - 1]['task']}'")
                    return True
                else:
                    print("✗ Failed to save changes")
                    return False
            else:
                print(f"Invalid task number! Please enter a number between 1 and {len(self.tasks)}")
                return False
        except Exception as e:
            print(f"Error marking task complete: {e}")
            return False
    
    def mark_incomplete(self, task_index):
        """Mark a task as incomplete"""
        try:
            if 1 <= task_index <= len(self.tasks):
                self.tasks[task_index - 1]["completed"] = False
                if self.save_tasks():
                    print(f"✓ Task marked as incomplete: '{self.tasks[task_index - 1]['task']}'")
                    return True
                else:
                    print("✗ Failed to save changes")
                    return False
            else:
                print(f"Invalid task number! Please enter a number between 1 and {len(self.tasks)}")
                return False
        except Exception as e:
            print(f"Error marking task incomplete: {e}")
            return False
    
    def edit_task(self, task_index, new_description):
        """Edit an existing task"""
        try:
            if 1 <= task_index <= len(self.tasks):
                if not new_description.strip():
                    print("Task description cannot be empty!")
                    return False
                
                old_task = self.tasks[task_index - 1]["task"]
                self.tasks[task_index - 1]["task"] = new_description.strip()
                
                if self.save_tasks():
                    print(f"✓ Task updated: '{old_task}' → '{new_description}'")
                    return True
                else:
                    print("✗ Failed to save changes")
                    return False
            else:
                print(f"Invalid task number! Please enter a number between 1 and {len(self.tasks)}")
                return False
        except Exception as e:
            print(f"Error editing task: {e}")
            return False
    
    def view_tasks(self, show_completed=True):
        """Display all tasks"""
        if not self.tasks:
            print("\n📝 No tasks found! Your to-do list is empty.")
            return
        
        print(f"\n{'='*60}")
        print("                    YOUR TO-DO LIST")
        print(f"{'='*60}")
        
        completed_count = sum(1 for task in self.tasks if task["completed"])
        pending_count = len(self.tasks) - completed_count
        
        print(f"Total Tasks: {len(self.tasks)} | Completed: {completed_count} | Pending: {pending_count}")
        print("-" * 60)
        
        for i, task in enumerate(self.tasks, 1):
            status = "✓" if task["completed"] else "○"
            status_text = "DONE" if task["completed"] else "TODO"
            created = task.get("created", "")
            created_text = f" (Created: {created})" if created else ""
            
            if show_completed or not task["completed"]:
                print(f"{i:2d}. [{status}] {task['task']:<40} [{status_text}]{created_text}")
        
        print(f"{'='*60}")
    
    def view_pending_tasks(self):
        """Display only pending tasks"""
        pending_tasks = [task for task in self.tasks if not task["completed"]]
        
        if not pending_tasks:
            print("\n🎉 Great! No pending tasks. You're all caught up!")
            return
        
        print(f"\n{'='*60}")
        print("                   PENDING TASKS")
        print(f"{'='*60}")
        
        pending_count = 0
        for i, task in enumerate(self.tasks, 1):
            if not task["completed"]:
                pending_count += 1
                created = task.get("created", "")
                created_text = f" (Created: {created})" if created else ""
                print(f"{i:2d}. [○] {task['task']:<40} [TODO]{created_text}")
        
        print(f"{'='*60}")
        print(f"Total Pending Tasks: {pending_count}")
    
    def clear_completed(self):
        """Remove all completed tasks"""
        completed_tasks = [task for task in self.tasks if task["completed"]]
        
        if not completed_tasks:
            print("No completed tasks to clear!")
            return False
        
        print(f"\nFound {len(completed_tasks)} completed task(s):")
        for task in completed_tasks:
            print(f"  • {task['task']}")
        
        confirm = input(f"\nAre you sure you want to delete these {len(completed_tasks)} completed task(s)? (y/N): ").strip().lower()
        
        if confirm in ['y', 'yes']:
            self.tasks = [task for task in self.tasks if not task["completed"]]
            if self.save_tasks():
                print(f"✓ {len(completed_tasks)} completed task(s) cleared!")
                return True
            else:
                print("✗ Failed to save changes")
                return False
        else:
            print("Operation cancelled.")
            return False
    
    def get_task_stats(self):
        """Display task statistics"""
        if not self.tasks:
            print("\n📊 No tasks to analyze!")
            return
        
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task["completed"])
        pending = total - completed
        completion_rate = (completed / total) * 100 if total > 0 else 0
        
        print(f"\n{'='*40}")
        print("           TASK STATISTICS")
        print(f"{'='*40}")
        print(f"Total Tasks:      {total}")
        print(f"Completed Tasks:  {completed}")
        print(f"Pending Tasks:    {pending}")
        print(f"Completion Rate:  {completion_rate:.1f}%")
        print(f"{'='*40}")


def display_menu():
    """Display the main menu"""
    print(f"\n{'='*50}")
    print("              TO-DO LIST MANAGER")
    print(f"{'='*50}")
    print("1.  Add Task")
    print("2.  View All Tasks")
    print("3.  View Pending Tasks")
    print("4.  Mark Task as Complete")
    print("5.  Mark Task as Incomplete")
    print("6.  Edit Task")
    print("7.  Remove Task")
    print("8.  Clear Completed Tasks")
    print("9.  Task Statistics")
    print("10. Exit")
    print("-" * 50)


def get_menu_choice():
    """Get valid menu choice from user"""
    while True:
        choice = input("Enter your choice (1-10): ").strip()
        if choice in [str(i) for i in range(1, 11)]:
            return int(choice)
        print("Invalid choice! Please enter a number between 1-10.")


def get_task_number(todo_app, prompt="Enter task number: "):
    """Get valid task number from user"""
    if not todo_app.tasks:
        print("No tasks available!")
        return None
    
    while True:
        try:
            task_num = int(input(prompt).strip())
            if 1 <= task_num <= len(todo_app.tasks):
                return task_num
            else:
                print(f"Please enter a number between 1 and {len(todo_app.tasks)}")
        except ValueError:
            print("Please enter a valid number!")


def main():
    """Main application loop"""
    print("🎯 Welcome to To-Do List Manager!")
    print("Your tasks are automatically saved to 'tasks.txt'")
    
    todo_app = TodoApp()
    
    # Show initial task count
    if todo_app.tasks:
        completed = sum(1 for task in todo_app.tasks if task["completed"])
        pending = len(todo_app.tasks) - completed
        print(f"📋 Loaded {len(todo_app.tasks)} task(s): {pending} pending, {completed} completed")
    
    while True:
        display_menu()
        choice = get_menu_choice()
        
        if choice == 1:  # Add Task
            task = input("\nEnter new task: ").strip()
            if task:
                todo_app.add_task(task)
            else:
                print("Task cannot be empty!")
        
        elif choice == 2:  # View All Tasks
            todo_app.view_tasks()
        
        elif choice == 3:  # View Pending Tasks
            todo_app.view_pending_tasks()
        
        elif choice == 4:  # Mark Complete
            todo_app.view_tasks()
            task_num = get_task_number(todo_app, "Enter task number to mark as complete: ")
            if task_num:
                todo_app.mark_complete(task_num)
        
        elif choice == 5:  # Mark Incomplete
            todo_app.view_tasks()
            task_num = get_task_number(todo_app, "Enter task number to mark as incomplete: ")
            if task_num:
                todo_app.mark_incomplete(task_num)
        
        elif choice == 6:  # Edit Task
            todo_app.view_tasks()
            task_num = get_task_number(todo_app, "Enter task number to edit: ")
            if task_num:
                current_task = todo_app.tasks[task_num - 1]["task"]
                print(f"Current task: {current_task}")
                new_task = input("Enter new task description: ").strip()
                if new_task:
                    todo_app.edit_task(task_num, new_task)
                else:
                    print("Task description cannot be empty!")
        
        elif choice == 7:  # Remove Task
            todo_app.view_tasks()
            task_num = get_task_number(todo_app, "Enter task number to remove: ")
            if task_num:
                # Show task before confirmation
                task_to_remove = todo_app.tasks[task_num - 1]["task"]
                confirm = input(f"Are you sure you want to remove '{task_to_remove}'? (y/N): ").strip().lower()
                if confirm in ['y', 'yes']:
                    todo_app.remove_task(task_num)
                else:
                    print("Task removal cancelled.")
        
        elif choice == 8:  # Clear Completed
            todo_app.clear_completed()
        
        elif choice == 9:  # Statistics
            todo_app.get_task_stats()
        
        elif choice == 10:  # Exit
            print("\n🎯 Thank you for using To-Do List Manager!")
            if todo_app.tasks:
                pending = sum(1 for task in todo_app.tasks if not task["completed"])
                if pending > 0:
                    print(f"📌 You have {pending} pending task(s) remaining.")
                else:
                    print("🎉 Congratulations! All tasks completed!")
            print(f"📁 Your tasks are saved in '{todo_app.filename}'")
            print("Goodbye! 👋")
            break
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
