
class VM:
    vm_counter = 0
    lower_bound = 15
    upper_bound = 90
    """
    Represents a Virtual Machine (VM) that runs on a Physical Machine (PM).
    """ 
    def __init__(self, cpu_core, cpu_speed, memory):
        VM.vm_counter += 1
        self.vm_id = VM.vm_counter
        self.cpu_core = cpu_core
        self.memory = memory
        self.free_cpu = cpu_core
        self.cpu_speed = cpu_speed
        self.free_memory = memory
        self.cpu_usage = 0
        self.memory_usage = 0
        self.status = "Normal"  # Status can be "Underloaded", "Overloaded", or "Normal"
        self.tasks = []

    def update_status(self, overload_threshold, underload_threshold):
        """
        Updates the status of the VM based on resource usage thresholds.
        """
        if self.cpu_usage > overload_threshold:
            self.status = "Overloaded"
        elif self.cpu_usage < underload_threshold:
            self.status = "Underloaded"
        else:
            self.status = "Normal"

    def allocate_task(self, task):
        """
        Allocates a task to this VM if resources permit.
        """
        if self.cpu_usage + task.cpu_demand <= self.cpu_core and \
           self.memory_usage + task.memory_demand <= self.memory:
            self.cpu_usage += task.cpu_demand
            self.memory_usage += task.memory_demand
            self.tasks.append(task)
            task.assign_to_vm(self)
            return True
        return False
