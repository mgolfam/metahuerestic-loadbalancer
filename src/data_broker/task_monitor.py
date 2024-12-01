import tkinter as tk
from tkinter import ttk
import time
from src.cloud.vm import VM  # Assuming you have a VM class

class TaskMonitor:
    """
    Task monitoring GUI displaying running tasks on each PM-VM and CPU utilization summary.
    This class does not allocate, remove or schedule tasks, it simply monitors them.
    """

    def __init__(self, vms, update_interval=300):
        """
        Initializes the TaskMonitor GUI with real VM data.

        Args:
            vms (list): List of VM objects.
            update_interval (int): Update interval in milliseconds for real-time updates.
        """
        self.vms = vms  # List of actual VM objects
        self.update_interval = update_interval
        self.running_tasks = {f"{vm.pm_id}-{vm.vm_id}": [] for vm in self.vms}  # Track tasks for each VM
        self.cpu_utilization = {vm.vm_id: 0 for vm in self.vms}  # Initialize VM CPU utilization

        # Tkinter setup
        self.root = tk.Tk()
        self.root.title("Task Monitoring")
        self.root.geometry("1200x700")

        # Treeview setup
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Define columns dynamically for each VM
        self.columns = [f"{vm.vm_id}" for vm in self.vms]
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
        for vm in self.vms:
            label = tk.Label(self.utilization_frame, text=f"{vm.vm_id}: 0%", width=20, anchor="w")
            label.pack(side=tk.LEFT, padx=5)
            self.utilization_labels[vm.vm_id] = label

        # Start the periodic updates
        self.update_table()

    def remove_finished_tasks(self):
        """
        Removes tasks that have finished running based on their end time.
        """
        current_time = time.time()
        for tasks in self.running_tasks.values():
            tasks[:] = [task for task in tasks if task["end_time"] > current_time]

    def update_table(self):
        """
        Periodically updates the table with running tasks and CPU utilization.
        """
        # Remove finished tasks
        self.remove_finished_tasks()

        # Clear the current table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Add running tasks to the table
        max_rows = max(len(tasks) for tasks in self.running_tasks.values()) if self.running_tasks else 0
        for i in range(max_rows):
            row_values = []
            for col in self.columns:
                try:
                    # Find the VM object corresponding to the column (col)
                    vm = next(vm for vm in self.vms if vm.vm_id == col)
                    if i < len(self.running_tasks[f"{vm.pm_id}-{vm.vm_id}"]):
                        row_values.append(self.running_tasks[f"{vm.pm_id}-{vm.vm_id}"][i]["task_id"])
                    else:
                        row_values.append("")
                except StopIteration:
                    # If no matching VM is found, append an empty value
                    row_values.append("")

            self.tree.insert("", "end", text=f"Row {i+1}", values=row_values)

        # Update CPU utilization for each VM
        self.calculate_cpu_utilization()

        # Schedule the next update
        self.root.after(self.update_interval, self.update_table)

    def calculate_cpu_utilization(self):
        """
        Calculates and updates the CPU utilization for each VM.
        """
        for vm in self.vms:
            # Calculate CPU utilization based on the number of running tasks
            total_cpu_usage = sum(task["task"].cpu_demand for task in self.running_tasks[f"{vm.pm_id}-{vm.vm_id}"])
            self.cpu_utilization[vm.vm_id] = min(total_cpu_usage * 100, 100)  # Max CPU usage of 100%

        # Update the utilization labels
        for vm, utilization in self.cpu_utilization.items():
            self.utilization_labels[vm].config(text=f"{vm}: {utilization}%")

    def run(self):
        """
        Runs the Tkinter main loop.
        """
        self.root.mainloop()


# Example usage
if __name__ == "__main__":
    # Assuming you have a list of VM objects initialized somewhere in your code
    vms = [
        VM(vm_id="VM1", pm_id="PM1", cpu_core=4, memory=8192), 
        VM(vm_id="VM2", pm_id="PM1", cpu_core=4, memory=8192),
        VM(vm_id="VM3", pm_id="PM2", cpu_core=8, memory=16384),
        VM(vm_id="VM4", pm_id="PM2", cpu_core=8, memory=16384)
    ]

    # Initialize and run the Task Monitor
    monitor = TaskMonitor(vms=vms, update_interval=1000)
    monitor.run()
