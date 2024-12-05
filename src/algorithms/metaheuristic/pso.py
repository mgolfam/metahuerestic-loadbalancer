import numpy as np
from src.algorithms.metaheuristic.metaheuristic_abstract import Metaheuristic

class ParticleSwarmOptimization(Metaheuristic):
    """
    Particle Swarm Optimization (PSO) Algorithm for task-to-VM allocation optimization.
    """

    def __init__(self, config):
        super().__init__(config)
        self.num_particles = config.get("num_particles", 30)
        self.max_iterations = config.get("iterations", 50)
        self.inertia_weight = config.get("inertia_weight", 0.5)
        self.cognitive_weight = config.get("cognitive_weight", 1.5)
        self.social_weight = config.get("social_weight", 1.5)
        self.velocity_clamp = config.get("velocity_clamp", [-1, 1])
        self.convergence_threshold = config.get("convergence_threshold", 1e-6)

    def initialize_population(self, tasks, vms):
        positions = np.random.randint(0, len(vms), size=(self.num_particles, len(tasks)))
        velocities = np.random.uniform(
            self.velocity_clamp[0], self.velocity_clamp[1], size=(self.num_particles, len(tasks))
        )
        return positions, velocities

    def evaluate_fitness(self, population, tasks, vms):
        fitness_scores = []
        for allocation in population:
            vm_utilization = [0] * len(vms)
            for task_idx, vm_idx in enumerate(allocation):
                task_cpu = tasks[task_idx] if isinstance(tasks[task_idx], (int, float)) else tasks[task_idx].cpu
                vm_utilization[vm_idx] += task_cpu

            ideal_load = sum(vm_utilization) / len(vms)
            fitness = sum((util - ideal_load) ** 2 for util in vm_utilization)
            fitness_scores.append(fitness)
        return np.array(fitness_scores)

    def update_population(self, positions, velocities, personal_best_positions, global_best_position):
        for i in range(self.num_particles):
            r1, r2 = np.random.random(), np.random.random()
            velocities[i] = (
                self.inertia_weight * velocities[i]
                + self.cognitive_weight * r1 * (personal_best_positions[i] - positions[i])
                + self.social_weight * r2 * (global_best_position - positions[i])
            )
            velocities[i] = np.clip(velocities[i], *self.velocity_clamp)

            # Update positions with explicit casting to int
            positions[i] = np.clip(positions[i] + velocities[i], 0, len(positions[0]) - 1).astype(int)

        return positions, velocities

    def optimize(self, tasks, vms):
        positions, velocities = self.initialize_population(tasks, vms)
        personal_best_positions = np.copy(positions)
        personal_best_scores = self.evaluate_fitness(positions, tasks, vms)
        global_best_position = personal_best_positions[np.argmin(personal_best_scores)]
        global_best_score = min(personal_best_scores)

        for iteration in range(self.max_iterations):
            positions, velocities = self.update_population(
                positions, velocities, personal_best_positions, global_best_position
            )
            fitness_scores = self.evaluate_fitness(positions, tasks, vms)

            for i in range(self.num_particles):
                if fitness_scores[i] < personal_best_scores[i]:
                    personal_best_scores[i] = fitness_scores[i]
                    personal_best_positions[i] = positions[i]

            if min(fitness_scores) < global_best_score:
                global_best_score = min(fitness_scores)
                global_best_position = positions[np.argmin(fitness_scores)]

            if global_best_score < self.convergence_threshold:
                break

        return global_best_position
