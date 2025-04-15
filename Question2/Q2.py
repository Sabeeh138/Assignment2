import random

def get_cost_required(task_number, facility_number):
    cost_matrix = [
        [10, 12, 9],
        [15, 14, 16],
        [8, 9, 7],
        [12, 10, 13],
        [14, 13, 12],
        [9, 8, 10],
        [11, 12, 13],
    ]
    return cost_matrix[task_number - 1][facility_number - 1]

def get_task_time(task_number):
    task_times = [5, 8, 4, 7, 6, 3, 9]
    return task_times[task_number - 1]

def get_facility_capacity(facility_number):
    facility_capacities = [24, 30, 28]
    return facility_capacities[facility_number - 1]

def fitness_calculation(chromosome):
    segments = chromosome.split('-')
    total_cost = 0
    penalty = 0
    used_tasks = set()
    for i, segment in enumerate(segments):
        facility = i + 1
        facility_time = 0
        for task_char in segment:
            task = int(task_char)
            if task in used_tasks:
                penalty += 1000
            used_tasks.add(task)
            facility_time += get_task_time(task)
            total_cost += get_cost_required(task, facility)
        if facility_time > get_facility_capacity(facility):
            penalty += (facility_time - get_facility_capacity(facility)) * 100
    if len(used_tasks) < 7:
        penalty += (7 - len(used_tasks)) * 1000
    return total_cost + penalty

def give_random_not_used(used):
    for _ in range(100):
        t = str(random.randint(1, 7))
        if t not in used:
            return t
    return '1'

def initialization(n):
    pop = []
    for _ in range(n):
        used = set()
        chromosome = []
        remaining = 7
        for fac in range(1, 4):
            part = ''
            if fac != 3:
                count = random.randint(1, 3)
            else:
                count = remaining
            for _ in range(count):
                task = give_random_not_used(used)
                used.add(task)
                part += task
                remaining -= 1
            chromosome.append(part)
        pop.append('-'.join(chromosome))
    return pop

def single_point_crossover(parent1, parent2, crossover_rate=0.8):
    if random.random() > crossover_rate:
        return parent1, parent2
    p1_clean = parent1.replace('-', '')
    p2_clean = parent2.replace('-', '')
    lengths = [len(p) for p in parent1.split('-')]
    total = sum(lengths)
    if total <= 1:
        return parent1, parent2
    point = random.randint(1, total - 1)
    child1_flat = p1_clean[:point] + p2_clean[point:]
    child2_flat = p2_clean[:point] + p1_clean[point:]
    def reconstruct(flat, lens):
        result = []
        idx = 0
        for l in lens:
            result.append(flat[idx:idx + l])
            idx += l
        return '-'.join(result)
    return reconstruct(child1_flat, lengths), reconstruct(child2_flat, lengths)

def roulette_selection(population, pop_size):
    fitness_scores = [fitness_calculation(chromo) for chromo in population]
    inverse_fitness = [1 / f if f != 0 else 1e6 for f in fitness_scores]
    total = sum(inverse_fitness)
    probabilities = [f / total for f in inverse_fitness]
    return random.choices(population, weights=probabilities, k=pop_size)

def swap_mutation(chromosome, mutation_rate=0.2):
    if random.random() > mutation_rate:
        return chromosome
    parts = chromosome.split('-')
    task_indices = [(i, j) for i, part in enumerate(parts) for j in range(len(part))]
    if len(task_indices) < 2:
        return chromosome
    (i1, j1), (i2, j2) = random.sample(task_indices, 2)
    parts[i1] = list(parts[i1])
    parts[i2] = list(parts[i2])
    parts[i1][j1], parts[i2][j2] = parts[i2][j2], parts[i1][j1]
    parts[i1] = ''.join(parts[i1])
    parts[i2] = ''.join(parts[i2])
    return '-'.join(parts)

def genetic_Algo():
    population = [
        '147-35-26',    # [1,3,2,1,2,3,1]
        '25-14-36',     # [2,1,3,2,1,3,2]
        '37-26-15',     # [3,2,1,3,2,1,3]
        '147-34-26',    # [1,3,2,2,1,1,3]
        '147-25-36',    # [1,2,3,1,2,3,1]
        '57-36-124'     # [2,3,1,3,1,2,2]
    ]
    population_size = len(population)
    generations = 100
    best_chromosome = None
    best_fitness = float('inf')
    for gen in range(generations):
        fitness_scores = [fitness_calculation(chromo) for chromo in population]
        for i in range(population_size):
            if fitness_scores[i] < best_fitness:
                best_fitness = fitness_scores[i]
                best_chromosome = population[i]
        selected = roulette_selection(population, pop_size=population_size)
        new_population = []
        for i in range(0, population_size, 2):
            p1 = selected[i]
            p2 = selected[i + 1] if i + 1 < population_size else random.choice(selected)
            c1, c2 = single_point_crossover(p1, p2)
            new_population.extend([c1, c2])
        new_population = new_population[:population_size]
        for i in range(len(new_population)):
            new_population[i] = swap_mutation(new_population[i], mutation_rate=0.2)
        population = new_population
    print("Best solution:", best_chromosome)
    print("Fitness:", best_fitness)

genetic_Algo()
