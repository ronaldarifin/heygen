import time
from threading import Thread
from typing import Dict

class Status:
    _tasks: Dict[str, dict] = {}

    @classmethod
    def get_status(cls, task_id: str) -> dict:
        if task_id not in cls._tasks:
            # Create new task if it doesn't exist
            cls._tasks[task_id] = {
                "status": "pending",
            }
            # Start background task
            thread = Thread(target=cls._process_task, args=(task_id,))
            thread.start()
            
        return cls._tasks[task_id]
    
    @classmethod
    def get_all_status(cls) -> dict:
        output = {}
        for task_id, task_dict in cls._tasks.items():
            output[f"Task {task_id}"] = task_dict['status']
        return output

    @classmethod
    def _process_task(cls, task_id: str):
        time.sleep(5)  # Simulate work for 5 seconds
        cls._tasks[task_id]["status"] = "completed"