import tkinter as tk
from tkinter import ttk
import time

class TaskMonitor:
    """
    Task monitoring GUI displaying running tasks on each VM and CPU utilization summary.
    This class does not allocate, remove, or schedule tasks, it simply monitors them.
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
        self.utilization_frame = tk.Frame(self.root)  # Use Frame for multi-line CPU utilization
        self.utilization_frame.pack(fill=tk.X, pady=10)  # Add vertical padding here to keep things close

        # CPU utilization labels
        self.utilization_labels = {}
        self.row_count = 0  # Keep track of the rows for the labels

        for vm in self.vms:
            # Create a new label for each VM's CPU usage in a separate row
            if self.row_count % 5 == 0:
                self.utilization_row_frame = tk.Frame(self.utilization_frame)
                self.utilization_row_frame.pack(fill=tk.X)
            
            label = tk.Label(self.utilization_row_frame, text=f"{vm.vm_id}: 0", width=20, anchor="w")
            label.pack(side=tk.LEFT, padx=5)
            self.utilization_labels[vm.vm_id] = label
            self.row_count += 1

        # Start the periodic updates
        self.update_table()

    def update_table(self):
        """
        Periodically updates the table with running tasks and CPU utilization.
        """
        # Clear the current table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Add running tasks to the table
        max_rows = max(len(vm.tasks) for vm in self.vms) if self.vms else 0  # Get max task count across all VMs
        for i in range(max_rows):
            row_values = []
            for vm in self.vms:
                if i < len(vm.tasks):
                    # val = f"{vm.tasks[i].task_id} {vm.tasks[i].cpu_demand}"
                    val = f"%{vm.tasks[i].cpu_demand}"
                    row_values.append(val)  # Add task ID from each VM
                else:
                    row_values.append("")  # No task for this row in this VM

            self.tree.insert("", "end", text=f"Row {i+1}", values=row_values)

        # Update CPU utilization for each VM
        self.calculate_cpu_utilization()

        # Schedule the next update
        self.root.after(self.update_interval, self.update_table)

    def calculate_cpu_utilization(self):
        """
        Calculates and updates the CPU utilization for each VM.
        Here we simply sum the exact CPU demand of the tasks assigned to each VM.
        """
        for vm in self.vms:
            # Calculate CPU utilization by summing CPU demands of all tasks in the VM
            total_cpu_usage = sum(task.cpu_demand for task in vm.tasks)  # Directly use the task's cpu_demand
            
            # Format the utilization to two decimal points
            self.utilization_labels[vm.vm_id].config(text=f"{total_cpu_usage:.2f}")  # Display as floating point with 2 decimals


    def run(self):
        """
        Runs the Tkinter main loop.
        """
        self.root.mainloop()

