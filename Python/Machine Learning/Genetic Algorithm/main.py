import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class GeneticAlgorithm:
    # f(x) = 2(x^2 + 1), x e <1…127>

    X_RANGE = (0, 127)
    NUM_OF_GENES_IN_CHROMOSOME = 7
    MAXIMUM = 2*(X_RANGE[1]**2 + 1)

    def __init__(self, num_of_individuals=100, num_of_iterations=100, mutation_prob=0.01, crossover_prob=0.1,
                 nonlinear_selection=False):
        self.population = []
        self.num_of_individuals = num_of_individuals
        self.num_of_iterations = num_of_iterations
        self.mutation_prob = mutation_prob
        self.crossover_prob = crossover_prob
        self.nonlinear_selection = nonlinear_selection

    @staticmethod
    def calculate_equation(x):
        return 2*(x**2 + 1)

    def solve(self):
        data = []
        self.initialize_population(self.num_of_individuals)
        for i in range(self.num_of_iterations):
            if self.nonlinear_selection:
                self.natural_selection_nonlinear()
            else:
                self.natural_selection()
            self.crossover()
            self.mutate()
            highest_fitness_score, avg_fitness_score, lowest_loss, avg_loss = self.get_data_for_plots()
            data.append(avg_loss)
        return data

    def initialize_population(self, num_of_individuals):
        self.population.clear()
        for i in range(num_of_individuals):
            self.population.append(self.get_random_chromosome())

    @staticmethod
    def get_random_chromosome():
        return [random.randint(0, 1) for i in range(GeneticAlgorithm.NUM_OF_GENES_IN_CHROMOSOME)]
        # return [0 for i in range(GeneticAlgorithm.NUM_OF_GENES_IN_CHROMOSOME)]

    def select_parent(self, fitness_scores):
        running_sum = 0
        rand = random.uniform(0, sum(fitness_scores))
        for i in zip(self.population, fitness_scores):
            running_sum += i[1]
            if running_sum >= rand:
                return i[0]

    def select_parent_nonlinear(self, probs):
        running_sum = 0
        rand = random.uniform(0, sum(probs))
        for i in zip(self.population, probs):
            running_sum += i[1]
            if running_sum >= rand**2:
                return i[0]

    def natural_selection(self):
        fitness_scores = self.calculate_fitness()
        survivors = []
        for i in range(self.num_of_individuals):
            survivors.append(self.select_parent(fitness_scores))
        self.population = survivors

    def natural_selection_nonlinear(self):
        probs = self.calculate_probabilities()
        survivors = []
        for i in range(self.num_of_individuals):
            survivors.append(self.select_parent_nonlinear(probs))
        self.population = survivors

    def mutate(self):
        mutated = []
        for i in self.population:
            new_bits = i.copy()
            rand = random.uniform(0, 1)
            if rand < self.mutation_prob:
                index = random.randint(0, GeneticAlgorithm.NUM_OF_GENES_IN_CHROMOSOME - 1)
                new_bits[index] = random.randint(0, 1)
            mutated.append(new_bits)
        self.population = mutated

    def crossover(self):
        new_population = self.population.copy()
        for i in range(len(new_population)):
            if random.uniform(0, 1) < self.crossover_prob:
                parent1 = self.population[random.randint(0, self.num_of_individuals - 1)]
                parent2 = self.population[random.randint(0, self.num_of_individuals - 1)]
                cross_point = random.randint(0, GeneticAlgorithm.NUM_OF_GENES_IN_CHROMOSOME - 1)
                new_individual = parent1[:cross_point] + parent2[cross_point:]
                new_population[i] = new_individual
        self.population = new_population

    @staticmethod
    def get_integer_from_bits(bits):
        return int("".join(str(b) for b in bits), 2)

    def calculate_fitness(self):
        integers = [self.get_integer_from_bits(bits) for bits in self.population]
        return [self.calculate_equation(x) for x in integers]

    def get_data_for_plots(self):
        fitness_scores = self.calculate_fitness()
        highest_fitness_score = max(fitness_scores)
        avg_fitness_score = sum(fitness_scores) / len(fitness_scores)
        loss = [GeneticAlgorithm.MAXIMUM - y for y in fitness_scores]
        lowest_loss = min(loss)
        avg_loss = sum(loss) / len(loss)
        return highest_fitness_score, avg_fitness_score, lowest_loss, avg_loss

    def calculate_probabilities(self):
        fitness_scores = self.calculate_fitness()
        probabilities = [score / sum(fitness_scores) for score in fitness_scores]
        return probabilities


def main():
    num_of_iterations = 400
    population_size = 100

    MUTATION_PROBS = [0.0001, 0.001, 0.01, 0.1]
    CROSSOVER_PROBS = [0.001, 0.01, 0.1, 0.5]

    GA = GeneticAlgorithm(
        num_of_iterations=num_of_iterations,
        num_of_individuals=population_size,
        nonlinear_selection=False
    )

    data_mutation = {
        "iteration": [i for i in range(num_of_iterations)],
    }

    GA.crossover_prob = 0
    for p in MUTATION_PROBS:
        GA.mutation_prob = p
        data_mutation[f"MUTATION PROBABILITY: {GA.mutation_prob}"] = GA.solve()

    plot(data_mutation, population_size)

    data_crossover = {
        "iteration": [i for i in range(num_of_iterations)],
    }

    GA.mutation_prob = 0.01
    for p in CROSSOVER_PROBS:
        GA.crossover_prob = p
        data_crossover[f"CROSSOVER PROBABILITY: {GA.crossover_prob}"] = GA.solve()

    plot(data_crossover, population_size)

    data_nonlinear = {
        "iteration": [i for i in range(num_of_iterations)],
    }
    GA.mutation_prob = 0.01
    GA.crossover_prob = 0.1

    GA.nonlinear_selection = True
    data_nonlinear["NONLINEAR SELECTION"] = GA.solve()

    GA.nonlinear_selection = False
    data_nonlinear["LINEAR SELECTION"] = GA.solve()

    plot(data_nonlinear, population_size)


def plot(data, population_size):
    df = pd.DataFrame(data)

    # plotting strip plot with seaborn
    sns.set(style="darkgrid")
    plt.figure(figsize=(9, 7))
    for column in df.drop('iteration', axis=1):
        plt.plot(df['iteration'], df[column], linewidth=2, alpha=0.9, label=column)

    # show legend
    plt.legend()

    # giving title to the plot
    plt.title(
        f"Analysing genetic algorithm for population_size: {population_size}",
        loc='left', fontsize=16,
        fontweight=0,
        color='orange'
    )

    # giving labels to x-axis and y-axis
    plt.xlabel("Iteration", fontsize=14)
    plt.ylabel("Avg loss", fontsize=14)

    plt.show()


if __name__ == "__main__":
    main()
