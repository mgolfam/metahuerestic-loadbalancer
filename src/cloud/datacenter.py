from src.cloud.pm import PM
from src.cloud.vm import VM

class Datacenter:
    dc_count = 0

    def __init__(self, config):
        """
        Initializes the datacenter with configurations.

        Args:
            config (dict): Configuration dictionary containing PM and VM settings.
        """
        Datacenter.dc_count += 1
        self.datacenter_id = Datacenter.dc_count
        self.pms = []
        self.config = config

        # Generate PMs based on config
        self.generate_pms()

    def pm_count(self):
        """Returns the number of PMs in the datacenter."""
        return len(self.pms)

    def generate_pms(self):
        """
        Generates PMs based on the provided configuration. Supports both heterogeneous and homogeneous setups.
        """
        if "pm_configurations" in self.config:
            # Generate heterogeneous PMs
            for pm_config in self.config["pm_configurations"]:
                pm = PM(
                    cpu_core=pm_config["cpu_core"],
                    cpu_speed=pm_config["cpu_speed"],
                    memory=pm_config["memory"]
                )
                for vm_config in pm_config["vms"]:
                    vm = VM(
                        pm_id=pm.pm_id,
                        cpu_core=vm_config["cpu_core"],
                        cpu_speed=pm_config["cpu_speed"],
                        memory=vm_config["memory"]
                    )
                    pm.add_vm(vm)
                self.pms.append(pm)
        elif "default_pm_config" in self.config:
            # Generate homogeneous PMs
            default_config = self.config["default_pm_config"]
            for _ in range(default_config["pm_count"]):
                pm = PM(
                    cpu_core=default_config["cpu_core"],
                    cpu_speed=default_config["cpu_speed"],
                    memory=default_config["memory"]
                )
                for vm_config in default_config["vms"]:
                    vm = VM(
                        pm_id=pm.pm_id,
                        cpu_core=vm_config["cpu_core"],
                        cpu_speed=default_config["cpu_speed"],
                        memory=vm_config["memory"]
                    )
                    pm.add_vm(vm)
                self.pms.append(pm)

    def calculate_makespan(self):
        """
        Calculates the makespan for the datacenter.

        Returns:
            float: The makespan (maximum end time across all PMs).
        """
        max_end_time = 0
        for pm in self.pms:
            max_end_time = max(max_end_time, pm.calculate_makespan())
        return max_end_time

    @staticmethod
    def visualize_datacenter(datacenter):
        """
        Visualizes the information of the datacenter, including PMs, VMs, and resources.

        Args:
            datacenter (Datacenter): Datacenter instance to visualize.
        """
        import matplotlib.pyplot as plt

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
