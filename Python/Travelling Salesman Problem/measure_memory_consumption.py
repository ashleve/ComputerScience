from graph import Graph
from dfs import DFS
from bfs import BFS
from greedy import Greedy
from a_star_custom import AStarCustom
import seaborn as sns
import pandas as pd
from memory_profiler import memory_usage
import matplotlib.pyplot as plt


NUM_OF_SAMPLES = 1
NUM_OF_NODES = 12
START_COUNTING_FROM_NODE = 4


def measure_dfs_recurrent():
    dfs = DFS(Graph(0))
    avg_memory_consumption = []

    for i in range(START_COUNTING_FROM_NODE, NUM_OF_NODES):
        print(f"Measuring DFS Recurrent for {i} nodes.")

        graph = Graph(i)
        dfs.graph = graph
        starting_node = next(iter(graph.graph))

        mem_usage = memory_usage((dfs.depth_first_search, (), {'start_node': starting_node}))
        avg_memory_consumption.append(mem_usage[-1])

    return avg_memory_consumption


def measure_bfs():
    bfs = BFS(Graph(0))
    avg_memory_consumption = []

    for i in range(START_COUNTING_FROM_NODE, NUM_OF_NODES):
        print(f"Measuring BFS for {i} nodes.")

        graph = Graph(i)
        bfs.graph = graph
        starting_node = next(iter(graph.graph))

        mem_usage = memory_usage((bfs.breadth_first_search, (), {'start_node': starting_node}))
        avg_memory_consumption.append(mem_usage[-1])

    return avg_memory_consumption


def measure_greedy():
    greedy = Greedy(Graph(0))
    avg_memory_consumption = []

    for i in range(START_COUNTING_FROM_NODE, NUM_OF_NODES):
        mem_usage_data = []

        print(f"Measuring Greedy for {i} nodes.")

        for j in range(NUM_OF_SAMPLES):
            graph = Graph(i)
            greedy.graph = graph
            starting_node = next(iter(graph.graph))

            mem_usage = memory_usage((greedy.greedy_approach, (), {'start_node': starting_node}))
            mem_usage_data.append(mem_usage[-1])
        
        avg_memory_consumption.append(sum(mem_usage_data) / NUM_OF_SAMPLES)

    return avg_memory_consumption


def measure_a_star_heuristic(heuristic_choice):
    my_a_star = AStarCustom(Graph(0))
    my_a_star.heuristic_choice = heuristic_choice
    avg_memory_consumption = []

    for i in range(START_COUNTING_FROM_NODE, NUM_OF_NODES):
        mem_usage_data = []

        print(f"Measuring A* heuristic {heuristic_choice} for {i} nodes.")

        for j in range(NUM_OF_SAMPLES):
            graph = Graph(i)
            my_a_star.graph = graph
            starting_node = next(iter(graph.graph))

            mem_usage = memory_usage((my_a_star.a_star, (), {'start_node': starting_node}))
            mem_usage_data.append(mem_usage[-1])

        avg_memory_consumption.append(sum(mem_usage_data) / NUM_OF_SAMPLES)

    return avg_memory_consumption


def main():
    data = {
        "Number of nodes": [i for i in range(START_COUNTING_FROM_NODE, NUM_OF_NODES)],
        "DFS Recurrent": measure_dfs_recurrent(),
        "BFS": measure_bfs(),
        "Greedy": measure_greedy(),
        "A* heuristic 0": measure_a_star_heuristic(0),
        "A* heuristic 1": measure_a_star_heuristic(1),
        "A* heuristic 2": measure_a_star_heuristic(2),
        "A* heuristic 3": measure_a_star_heuristic(3),
        "A* heuristic 4": measure_a_star_heuristic(4),
        "A* heuristic 5": measure_a_star_heuristic(5),
    }

    plot(data)

    print("Done.")


def plot(data):
    """
        Plot memory consumption in respect to number of graph nodes.
    """

    df = pd.DataFrame(data)

    # plotting strip plot with seaborn
    sns.set(style="darkgrid")
    plt.figure(figsize=(9, 10))
    for column in df.drop('Number of nodes', axis=1):
        plt.plot(df['Number of nodes'], df[column], linewidth=1, alpha=0.9, label=column)

    # show legend
    plt.legend(loc=2, ncol=2)

    # giving title to the plot
    plt.title(
        "Comparing memory consumption for TSP problem",
        loc='left', fontsize=16,
        fontweight=0,
        color='orange'
    )

    # giving labels to x-axis and y-axis
    plt.xlabel("Number of nodes", fontsize=14)
    plt.ylabel("Memory consumption (MB)", fontsize=14)

    plt.show()


if __name__ == '__main__':
    main()
