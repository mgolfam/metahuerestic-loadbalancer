from src.cloud.pm import PM

import matplotlib.pyplot as plt

class Datacenter:
    dc_count = 0
    # because of pms are identical we use the same resource for all of theme.
    def __init__(self, pm_count, cpu_core, cpu_speed, memory, vm_count=0, vm_cpu=0, vm_memory=0):
        Datacenter.dc_count += 1
        self.cpu_speed = cpu_speed
        self.datacenter_id = Datacenter.dc_count
        self.pms = []
        
        if pm_count > 0:
            self.generate_pms(pm_count=pm_count, cpu_core=cpu_core, memory=memory, vm_count=vm_count, vm_cpu=vm_cpu, vm_memory=vm_memory)

    def pm_count(self):
        return len(self.pms)

    def generate_pms(self, pm_count, cpu_core, memory, vm_count=0, vm_cpu=0, vm_memory=0):
        """
        Generates PMs for the datacenter.

        Args:
            pm_count (int): Number of PMs to create.
            cpu_core (int): CPU cores for each PM.
            cpu_speed (int): CPU speed for each PM.
            memory (int): Memory for each PM.

        Returns:
            list: List of PM objects.
        """
        self.pms = [PM(cpu_core=cpu_core, cpu_speed=self.cpu_speed, memory=memory, vm_count=vm_count, vm_cpu=vm_cpu, vm_memory=vm_memory) for _ in range(pm_count)]
        return self.pms

    def calculate_makespan(self):
        max_end_time = 0
        for pm in self.pms:
            max_end_time = max(max_end_time, pm.calculate_makespan())
        return max_end_time
    
    @staticmethod
    def visualize_datacenter(datacenter):
        """
        Visualizes the information of the data center, including PMs, VMs, and resources.

        Args:
            datacenter (list): List of PMs in the data center.
        """
        pm_ids = [pm.pm_id for pm in datacenter.pms]
        free_cpu_cores = [pm.free_cpu_core for pm in datacenter.pms]
        free_memory = [pm.free_memory for pm in datacenter.pms]
        vm_counts = [pm.vm_count() for pm in datacenter.pms]

        # Plot free CPU cores
        plt.figure(figsize=(10, 6))
        plt.bar(pm_ids, free_cpu_cores, color='blue', alpha=0.7, label='Free CPU Cores')
        plt.xlabel("PM ID")
        plt.ylabel("Free CPU Cores")
        plt.title("Free CPU Cores per Physical Machine")
        plt.legend()
        plt.show()

        # Plot free memory
        plt.figure(figsize=(10, 6))
        plt.bar(pm_ids, free_memory, color='green', alpha=0.7, label='Free Memory (GB)')
        plt.xlabel("PM ID")
        plt.ylabel("Free Memory (GB)")
        plt.title("Free Memory per Physical Machine")
        plt.legend()
        plt.show()

        # Plot VM count
        plt.figure(figsize=(10, 6))
        plt.bar(pm_ids, vm_counts, color='orange', alpha=0.7, label='Number of VMs')
        plt.xlabel("PM ID")
        plt.ylabel("Number of VMs")
        plt.title("Number of VMs per Physical Machine")
        plt.legend()
        plt.show()
