import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import signal
import sys


class ResourceMonitorGUI:
    """
    GUI for monitoring CPU utilization in real-time.
    """

    def __init__(self, pm_list, update_interval=1000):
        """
        Initializes the Resource Monitor GUI.

        Args:
            pm_list (list): List of PM objects to monitor.
            update_interval (int): Update interval in milliseconds.
        """
        self.pm_list = pm_list
        self.update_interval = update_interval
        self.data = {pm.pm_id: [] for pm in pm_list}  # Store utilization data for each PM
        self.max_time = 20  # Number of time points to display
        self.start_time = time.time()

        # Setup Tkinter GUI
        self.root = tk.Tk()
        self.root.title("Resource Monitoring - CPU Utilization")
        self.root.geometry("800x600")
        
        # Handle CTRL+C
        signal.signal(signal.SIGINT, self.handle_exit)


        # Setup Matplotlib Figure
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Start updating the GUI
        self.update_gui()

    def fetch_cpu_utilization(self):
        """
        Fetches real CPU utilization from PMs.
        """
        for pm in self.pm_list:
            resource_status = pm.monitor_resources()  # Fetch real resource data
            utilization = resource_status.get("cpu_utilization", 0)
            self.data[pm.pm_id].append((time.time() - self.start_time, utilization))
            if len(self.data[pm.pm_id]) > self.max_time:
                self.data[pm.pm_id].pop(0)

    def update_gui(self):
        """
        Updates the GUI with the latest data and refreshes the graph.
        """
        self.fetch_cpu_utilization()
        self.plot_cpu_utilization()
        self.root.after(self.update_interval, self.update_gui)

    def plot_cpu_utilization(self):
        """
        Plots the CPU utilization data on the graph.
        """
        self.ax.clear()
        self.ax.set_title("CPU Utilization Over Time")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("CPU Utilization (%)")
        self.ax.set_ylim(0, 100)

        for pm_id, data_points in self.data.items():
            times, utilizations = zip(*data_points) if data_points else ([], [])
            self.ax.plot(times, utilizations, label=f"PM {pm_id}")

        self.ax.legend()
        self.canvas.draw()

    def run(self):
        """
        Runs the Tkinter main loop.
        """
        self.root.mainloop()
        
    def handle_exit(self, signum, frame):
        """
        Handles CTRL+C for graceful exit.
        """
        print("Exiting...")
        self.root.destroy()
        sys.exit(0)



# Example Usage
if __name__ == "__main__":
    from src.cloud.pm import PM

    # Simulate PMs with real resource monitoring
    pm1 = PM(cpu_core=8, cpu_speed=2000, memory=32)
    pm2 = PM(cpu_core=16, cpu_speed=2500, memory=64)

    # Start the Resource Monitor GUI
    monitor_gui = ResourceMonitorGUI(pm_list=[pm1, pm2], update_interval=1000)
    monitor_gui.run()
