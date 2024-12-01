import tkinter as tk
from tkinter import ttk
import random
import time


class TaskMonitor:
    """
    Task monitoring GUI displaying running tasks on each PM-VM and CPU utilization summary.
    """

    def __init__(self, pm_vm_structure, update_interval=1000, tasks_per_update=5):
        """
        Initializes the TaskMonitor GUI.

        Args:
            pm_vm_structure (dict): Dictionary with PM keys and lists of VMs (e.g., {"PM1": ["VM1", "VM2"]}).
            update_interval (int): Update interval in milliseconds for real-time updates.
            tasks_per_update (int): Number of tasks to assign in each update cycle.
        """
        self.pm_vm_structure = pm_vm_structure
        self.update_interval = update_interval
        self.tasks_per_update = tasks_per_update
        self.task_count = 1  # Simulated task ID counter
        self.running_tasks = {f"{pm}-{vm}": [] for pm, vms in pm_vm_structure.items() for vm in vms}
        self.cpu_utilization = {pm: {"total": 0, "vms": {vm: 0 for vm in vms}} for pm, vms in pm_vm_structure.items()}  # PM and VM utilization

        # Tkinter setup
        self.root = tk.Tk()
        self.root.title("Task Monitoring")
        self.root.geometry("1200x700")

        # Treeview setup
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Define columns dynamically
        self.columns = [f"{pm}-{vm}" for pm, vms in pm_vm_structure.items() for vm in vms]
        self.tree["columns"] = self.columns

        # Format columns
        self.tree.heading("#0", text="Task ID")
        self.tree.column("#0", width=100, anchor="center")
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        # Frame for CPU utilization summary
        self.utilization_frame = tk.LabelFrame(self.root, text="CPU Utilization Summary", padx=10, pady=10)
        self.utilization_frame.pack(fill=tk.X)

        # CPU utilization labels
        self.utilization_labels = {}
        for pm in self.pm_vm_structure:
            pm_label = tk.Label(self.utilization_frame, text=f"{pm}: 0%", width=15, anchor="w")
            pm_label.pack(side=tk.LEFT, padx=5)
            self.utilization_labels[pm] = {"pm_label": pm_label, "vms": {}}
            for vm in self.pm_vm_structure[pm]:
                vm_label = tk.Label(self.utilization_frame, text=f"{pm}-{vm}: 0%", width=20, anchor="w")
                vm_label.pack(side=tk.LEFT, padx=5)
                self.utilization_labels[pm]["vms"][vm] = vm_label

        # Start the periodic updates
        self.update_table()

    def assign_tasks(self):
        """
        Simulates assigning multiple tasks to random PM-VMs with random durations, enforcing a 90% threshold.
        """
        for _ in range(self.tasks_per_update):
            pm = random.choice(list(self.pm_vm_structure.keys()))
            if self.cpu_utilization[pm]["total"] >= 90:  # Skip overloaded PMs
                continue

            vm = random.choice(self.pm_vm_structure[pm])
            pm_vm = f"{pm}-{vm}"
            task_id = f"T{self.task_count}"
            self.task_count += 1
            duration = random.randint(5, 15)  # Task duration in seconds
            self.running_tasks[pm_vm].append({"task_id": task_id, "end_time": time.time() + duration})

    def remove_finished_tasks(self):
        """
        Removes tasks that have finished running based on their end time.
        """
        current_time = time.time()
        for tasks in self.running_tasks.values():
            tasks[:] = [task for task in tasks if task["end_time"] > current_time]

    def calculate_cpu_utilization(self):
        """
        Calculates and updates the CPU utilization for each PM and its VMs.
        """
        for pm in self.pm_vm_structure:
            pm_total = 0
            for vm in self.pm_vm_structure[pm]:
                pm_vm = f"{pm}-{vm}"
                vm_utilization = len(self.running_tasks[pm_vm]) * 10  # Simulate 10% per task
                self.cpu_utilization[pm]["vms"][vm] = min(vm_utilization, 100)
                pm_total += vm_utilization

            self.cpu_utilization[pm]["total"] = min(pm_total, 100)

        # Update the utilization labels
        for pm, data in self.cpu_utilization.items():
            self.utilization_labels[pm]["pm_label"].config(text=f"{pm}: {data['total']}%")
            for vm, utilization in data["vms"].items():
                self.utilization_labels[pm]["vms"][vm].config(text=f"{pm}-{vm}: {utilization}%")

    def update_table(self):
        """
        Periodically updates the table with running tasks and CPU utilization.
        """
        # Simulate task assignments
        self.assign_tasks()

        # Remove finished tasks
        self.remove_finished_tasks()

        # Calculate and update CPU utilization
        self.calculate_cpu_utilization()

        # Clear the current table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Add running tasks to the table
        max_rows = max(len(tasks) for tasks in self.running_tasks.values())
        for i in range(max_rows):
            row_values = []
            for col in self.columns:
                if i < len(self.running_tasks[col]):
                    row_values.append(self.running_tasks[col][i]["task_id"])
                else:
                    row_values.append("")
            self.tree.insert("", "end", text=f"Row {i+1}", values=row_values)

        # Schedule the next update
        self.root.after(self.update_interval, self.update_table)

    def run(self):
        """
        Runs the Tkinter main loop.
        """
        self.root.mainloop()


# Example usage
if __name__ == "__main__":
    # Define PM-VM structure for the table
    pm_vm_structure = {
        "PM1": ["VM1", "VM2", "VM3"],
        "PM2": ["VM1", "VM2", "VM3", "VM4"],
        "PM3": ["VM1", "VM2"],
    }

    # Initialize and run the Task Monitor
    monitor = TaskMonitor(pm_vm_structure=pm_vm_structure, update_interval=1000, tasks_per_update=10)
    monitor.run()
