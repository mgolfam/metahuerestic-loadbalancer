import time

class MetricMonitor:
    """
    MetricMonitor class for monitoring and analyzing system metrics.
    """

    def __init__(self):
        """
        Initializes the MetricMonitor with default values.
        """
        self.makespan = 0
        self.response_times = []
        self.resource_utilizations = []
        self.throughput = 0
        self.sla_violations = 0
        self.overhead = 0
        self.task_start_times = {}
        self.task_end_times = {}
        self.initial_resource_usage = 0
        self.final_resource_usage = 0

    def start_task(self, task_id):
        """
        Records the start time of a task.

        Args:
            task_id (str): Unique identifier for the task.
        """
        self.task_start_times[task_id] = time.time()

    def end_task(self, task_id, sla_time):
        """
        Records the end time of a task and calculates response time and SLA violations.

        Args:
            task_id (str): Unique identifier for the task.
            sla_time (float): SLA time for the task.

        Returns:
            None
        """
        end_time = time.time()
        self.task_end_times[task_id] = end_time

        # Calculate response time
        response_time = end_time - self.task_start_times.get(task_id, end_time)
        self.response_times.append(response_time)

        # Check SLA violation
        if response_time > sla_time:
            self.sla_violations += 1

    def calculate_makespan(self):
        """
        Calculates the makespan based on recorded task times.

        Returns:
            float: Makespan value.
        """
        if not self.task_start_times or not self.task_end_times:
            return 0
        self.makespan = max(self.task_end_times.values()) - min(self.task_start_times.values())
        return self.makespan

    def calculate_throughput(self, total_time):
        """
        Calculates the throughput of the system.

        Args:
            total_time (float): Total time the system was operational.

        Returns:
            float: Throughput value.
        """
        completed_tasks = len(self.task_end_times)
        self.throughput = completed_tasks / total_time if total_time > 0 else 0
        return self.throughput

    def calculate_resource_utilization(self, vm_resources, vm_used_resources):
        """
        Calculates the resource utilization for each VM.

        Args:
            vm_resources (list): List of total resources available for each VM.
            vm_used_resources (list): List of currently used resources for each VM.

        Returns:
            list: Resource utilization percentages for each VM.
        """
        self.resource_utilizations = [
            (used / total) * 100 if total > 0 else 0
            for used, total in zip(vm_used_resources, vm_resources)
        ]
        return self.resource_utilizations

    def calculate_overhead(self, task_count):
        """
        Calculates the overhead introduced by the load balancing algorithm.

        Args:
            task_count (int): Number of tasks in the system.

        Returns:
            float: Overhead per task.
        """
        self.overhead = (
            (self.final_resource_usage - self.initial_resource_usage) / task_count
            if task_count > 0
            else 0
        )
        return self.overhead

    def reset_metrics(self):
        """
        Resets all metrics to their default values.
        """
        self.makespan = 0
        self.response_times = []
        self.resource_utilizations = []
        self.throughput = 0
        self.sla_violations = 0
        self.overhead = 0
        self.task_start_times.clear()
        self.task_end_times.clear()
        self.initial_resource_usage = 0
        self.final_resource_usage = 0

    def report_metrics(self):
        """
        Reports all collected metrics.

        Returns:
            dict: Dictionary containing all metrics.
        """
        return {
            "makespan": self.makespan,
            "average_response_time": sum(self.response_times) / len(self.response_times)
            if self.response_times
            else 0,
            "resource_utilizations": self.resource_utilizations,
            "throughput": self.throughput,
            "sla_violations": self.sla_violations,
            "overhead": self.overhead,
        }
