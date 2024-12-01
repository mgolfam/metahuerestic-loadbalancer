from src.cloud.datacenter import Datacenter

def main():
    dc = Datacenter(5, 20, 2.8*1024, 64, 5)
    Datacenter.visualize_datacenter(dc)
    
    # # Create tasks
    # task1 = Task(cpu_demand=2, memory_demand=4, arrival_time=0, deadline=10)
    # task2 = Task(cpu_demand=1, memory_demand=2, arrival_time=1, deadline=5)

    # # Create VMs
    # vm1 = VM(vm_id=1, cpu_capacity=8, memory_capacity=16)
    # vm2 = VM(vm_id=2, cpu_capacity=4, memory_capacity=8)

    # # Create a PM and assign VMs to it
    # pm1 = PM(pm_id=1, cpu_capacity=16, memory_capacity=32)
    # pm1.add_vm(vm1)
    # pm1.add_vm(vm2)

    # # Allocate tasks to VMs
    # vm1.allocate_task(task1)
    # vm2.allocate_task(task2)

    # # Monitor resources
    # total_cpu, total_memory = pm1.monitor_resources()
    # print(f"PM1 Total CPU Usage: {total_cpu}, Total Memory Usage: {total_memory}")

if __name__ == "__main__":
    main()
