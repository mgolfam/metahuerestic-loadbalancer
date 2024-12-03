from src.cloud.vm import VM

class PM:
    pm_counter = 0
    lower_bound = 15
    upper_bound = 90
    
    """
    Represents a Physical Machine (PM) that hosts multiple VMs.
    """
    def __init__(self, cpu_core, cpu_speed, memory, vm_count=0, vm_cpu=0, vm_memory=0):
        PM.pm_counter += 1
        self.pm_id = PM.pm_counter
        self.cpu_core = cpu_core
        self.free_cpu_core = cpu_core
        self.cpu_speed = cpu_speed # CPU speed in MHz
        self.mips = cpu_core * cpu_speed  # Calculate MIPS as cores x speed
        self.memory = memory
        self.free_memory = memory
        self.vms = []
        
        if vm_count > 0:
            self.generate_vms(vm_numbers=vm_count, cpu_core=vm_cpu, memory=vm_memory)
        
    def allocated_resource(self, required_cpu_core, required_memory):
        """
        Allocates the required resources if available.

        Args:
            required_mips (int): Required MIPS for allocation.
            required_cpu_core (int): Required CPU cores for allocation.
            required_memory (int): Required memory for allocation.

        Returns:
            bool: True if resources are allocated, False otherwise.
        """
        required_mips = self.cpu_speed * required_cpu_core
        # print(required_mips, self.cpu_speed, required_cpu_core)
        if (self.free_cpu_core >= required_cpu_core and
                self.free_memory >= required_memory):
            self.free_cpu_core -= required_cpu_core
            self.free_memory -= required_memory
            return True
        else:
            return False
        
    def free_mips(self):
        return self.free_cpu_core * self.cpu_speed

    def add_vm(self, vm):
        """
        Adds a VM to this PM.
        """
        # self.show_free_resources()
        can_add_vm = self.allocated_resource(vm.cpu_core, vm.memory)
        # self.show_free_resources()
        if can_add_vm:
            self.vms.append(vm)
        
        return can_add_vm

    def vm_count(self):
        """
        Returns the number of VMs hosted on this PM.
        """
        return len(self.vms)

    def monitor_resources(self):
        """
        Monitors the resource usage of the PM by aggregating VM usage.
        """
        total_cpu_usage = sum(vm.cpu_usage for vm in self.vms)
        total_memory_usage = sum(vm.memory_usage for vm in self.vms)
        cpu_utilization = (total_cpu_usage / (self.cpu_core * self.cpu_speed)) * 100
        memory_utilization = (total_memory_usage / self.memory) * 100
        status = "Normal"
        if cpu_utilization > self.upper_bound or memory_utilization > self.upper_bound:
            status = "Overloaded"
        elif cpu_utilization < self.lower_bound and memory_utilization < self.lower_bound:
            status = "Underloaded"
        return {
            "total_cpu_usage": total_cpu_usage,
            "total_memory_usage": total_memory_usage,
            "cpu_utilization": cpu_utilization,
            "memory_utilization": memory_utilization,
            "status": status
        }
    
    def generate_vms(self, vm_numbers, cpu_core, memory, disk=10):
        """
        Generates and adds VMs to the PM.

        Args:
            vm_numbers (int): Number of VMs to create.
            cpu_core (int): CPU core allocation for each VM.
            memory (int): Memory allocation for each VM.
            disk (int): Disk storage allocation for each VM (default is 10).

        Returns:
            list: List of created VM objects.
        """
        if cpu_core == 0:
            cpu_core = int(self.free_cpu_core / vm_numbers)
            
        if memory == 0:
            memory = int(self.free_memory / vm_numbers)
            
        for i in range(vm_numbers):
            vm = VM(
                pm_id=self.pm_id,
                cpu_core=cpu_core,
                cpu_speed=self.cpu_speed,
                memory=memory,
            )
            added = self.add_vm(vm)
            if not added :
                print(f"cant add vm on pm:{1} because of resource problems.".format(self.pm_id))
        return self.vms

    def show_free_resources(self):
        """
        Displays the free resources available on the PM.

        Returns:
            dict: Dictionary containing free CPU cores, free memory, and free MIPS.
        """
        print({
            "PM ID": self.pm_id,
            "Free CPU Cores": self.free_cpu_core,
            "Free Memory (GB)": self.free_memory,
            "Free MIPS": self.free_mips
        })
    
    def calculate_makespan(self):
        max_end_time = 0
        for vm in pm.vms:
            max_end_time = max(max_end_time, vm.calculate_makespan())
        return max_end_time
