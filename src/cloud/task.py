import time

class Task:
    task_counter = 0  # Static counter for auto-incrementing Task IDs

    def __init__(self, cpu_demand, memory_demand=0, execution_time=1):
        Task.task_counter += 1
        self.task_id = Task.task_counter  # Auto-increment Task ID
        self.cpu_demand = cpu_demand
        self.memory_demand = memory_demand or 0
        self.execution_time = execution_time  # Time required to execute (seconds)
        self.start_time = time.time()
        self.end_time = self.start_time + self.execution_time  # Calculate the end time

    def is_complete(self):
        """Checks if the task is complete."""
        return time.time() >= self.end_time if self.end_time else False
