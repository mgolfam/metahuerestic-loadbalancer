import time

class Task:
    task_counter = 0  # Static counter for auto-incrementing Task IDs
    
    # cpu_demand is cpu utilization we need, its percent.
    # deadline is in miliseconds.
    def __init__(self, cpu_demand, memory_demand=None, deadline=1):
        Task.task_counter += 1
        self.task_id = Task.task_counter  # Auto-increment Task ID
        self.cpu_demand = cpu_demand
        self.memory_demand = memory_demand
        self.arrival_time = time.time()  # Automatically set the arrival time to initialization time
        self.deadline = deadline
        self.assigned_vm = None

    def assign_to_vm(self, vm):
        self.assigned_vm = vm
