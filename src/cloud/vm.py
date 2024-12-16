from src.cloud.task import Task

class VM:
    max_cpu_utilization = 0.9
    vm_counter = 0

    def __init__(self, pm_id, cpu_core, cpu_speed, memory):
        VM.vm_counter += 1
        self.vm_id = VM.vm_counter
        self.pm_id = pm_id
        self.cpu_core = cpu_core
        self.memory = memory
        self.cpu_speed = cpu_speed  # CPU speed in MHz
        self.memory_usage = 0  # Memory currently in use
        self.tasks = []  # List of tasks assigned to this VM
        self.total_executed_tasks = 0
        self.executed_tasks_interval = 0
        self.total_executed_time = 0

    def cpu_usage_percent(self):
        cpu_usage = 0
        for task in self.tasks:
            if task.is_complete():
                self.tasks.remove(task)
                continue
            else:
                cpu_usage += task.cpu_demand

        return cpu_usage

    def free_cpu_percent(self):
        """
        Calculates the free CPU percentage after accounting for task demands.

        Returns:
            float: Free CPU percentage.
        """
        cpu_usage = self.cpu_usage_percent()

        return self.max_cpu_utilization - cpu_usage

    def free_memory(self):
        """
        Calculates free memory available.

        Returns:
            int: Free memory in KB.
        """
        return self.memory - self.memory_usage

    def allocate_task(self, task):
        """
        Allocates a task to this VM if resources permit.

        Args:
            task (Task): Task object to allocate.

        Returns:
            bool: True if allocation was successful, False otherwise.
        """
        allocated = False
        if (self.free_cpu_percent() >= task.cpu_demand and
                self.free_memory() >= task.memory_demand):
            self.memory_usage += task.memory_demand
            self.tasks.append(task)
            allocated = True
            self.total_executed_time += task.execution_time
        
        self.show_cpu_utilization()
        return allocated
    
    def show_cpu_utilization(self):
        print("vm", self.vm_id, self.cpu_usage_percent())

    def monitor_resources(self):
        """
        Monitors the resource usage of the VM, including CPU and memory.

        Returns:
            dict: Dictionary with resource usage details.
        """
        cpu_usage = sum(task.cpu_demand for task in self.tasks if not task.is_complete())
        memory_usage = self.memory_usage
        return {
            "vm_id": self.vm_id,
            "cpu_usage_percent": cpu_usage,
            "memory_usage_percent": 0,
            "active_tasks": len(self.tasks),
            "free_cpu_percent":1 - cpu_usage,
            "free_memory_kb": self.free_memory()
        }
    
    def calculate_makespan(self):
        """
        Calculates the makespan of tasks running on this VM.

        Returns:
            float: Maximum end time of all tasks.
        """
        max_end_time = 0
        for task in self.tasks:
            max_end_time = max(max_end_time, task.end_time)
        return max_end_time

    def calculate_makespan2(self):
        """
        Calculates the makespan of tasks running on this VM.

        Returns:
            float: Maximum end time of all tasks.
        """
        # sum_time = 0
        # for task in self.tasks:
        #     sum_time += task.execution_time
        return self.total_executed_time / self.cpu_core