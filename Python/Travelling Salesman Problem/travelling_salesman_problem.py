import matplotlib.pyplot as plt
from graph import Graph, Node
from dfs import DFS
from bfs import BFS
from greedy import Greedy
from a_star_custom import AStarCustom
import seaborn as sns
import pandas as pd
import time


def test_random():
    """
        Test all approaches for random path.
    """
    num_of_nodes = 7
    graph = Graph(num_of_nodes)

    starting_node = next(iter(graph.graph))

    print("{:-^100}".format(" TESTING RANDOM PATH "))

    dfs = DFS(graph)
    paths_dfs = dfs.depth_first_search(starting_node)
    print("DEPTH FIRST SEARCH")
    print("Number of Hamilton Cycles found:", len(paths_dfs))
    print("Shortest path:", graph.get_shortest_path(paths_dfs), end="\n\n")

    bfs = BFS(graph)
    paths_bfs = bfs.breadth_first_search(starting_node)
    print("BREADTH FIRST SEARCH")
    print("Number of Hamilton Cycles found:", len(paths_bfs))
    print("Shortest path:", graph.get_shortest_path(paths_bfs), end="\n\n")

    greedy = Greedy(graph)
    path_greedy = greedy.greedy_approach(starting_node)
    print("GREEDY APPROACH")
    print("Path length:", (path_greedy, graph.calculate_path_length(path_greedy)), end="\n\n")

    a_star_custom = AStarCustom(graph)
    path_a_star = a_star_custom.a_star(starting_node)
    print("A* APPROACH")
    print("Path length:", (path_a_star, graph.calculate_path_length(path_a_star)), end="\n")

    print("{:-^100}".format(" END OF TEST "), end="\n\n")


def try_a_star(num_of_samples, num_of_nodes, heuristic_choice=AStarCustom.DEFAULT_HEURISTIC):
    a_star_custom = AStarCustom(Graph(0))

    a_star_path_lengths = []
    a_star_execution_times = []

    for j in range(num_of_samples):
        graph = Graph(num_of_nodes)
        starting_node = next(iter(graph.graph))

        start = time.time()
        a_star_custom.graph = graph
        a_star_custom.heuristic_choice = heuristic_choice
        path_a_star = a_star_custom.a_star(starting_node)
        a_star_path_lengths.append(Graph.calculate_path_length(path_a_star))
        execution_time = time.time() - start
        a_star_execution_times.append(execution_time)

    avg_path_length = sum(a_star_path_lengths) / num_of_samples
    avg_execution_time = sum(a_star_execution_times) / num_of_samples
    return avg_path_length, avg_execution_time


def try_different_a_star_heuristics(num_of_samples, num_of_nodes):
    a_star_custom = AStarCustom(Graph(0))
    results = []

    for i in range(a_star_custom.num_of_heuristics):
        avg_path_length, avg_execution_time = try_a_star(num_of_samples, num_of_nodes, heuristic_choice=i)
        label = "A* heuristic " + str(i)
        results.append((avg_path_length, avg_execution_time, label))

    return results


def try_dfs_and_bfs_and_greedy(num_of_samples: int, num_of_nodes: int):
    graph = Graph(0)

    dfs = DFS(graph)
    dfs_path_lengths = []
    dfs_execution_times = []

    bfs = BFS(graph)
    bfs_path_lengths = []
    bfs_execution_times = []

    greedy = Greedy(graph)
    greedy_path_lengths = []
    greedy_execution_times = []

    for j in range(num_of_samples):
        graph = Graph(num_of_nodes)
        starting_node = next(iter(graph.graph))

        start = time.time()
        dfs.graph = graph
        paths_dfs = dfs.depth_first_search(starting_node)
        dfs_path_lengths.append(Graph.get_shortest_path(paths_dfs)[1])
        execution_time = time.time() - start
        dfs_execution_times.append(execution_time)

        start = time.time()
        bfs.graph = graph
        paths_bfs = bfs.breadth_first_search(starting_node)
        bfs_path_lengths.append(Graph.get_shortest_path(paths_bfs)[1])
        execution_time = time.time() - start
        bfs_execution_times.append(execution_time)

        start = time.time()
        greedy.graph = graph
        path_greedy = greedy.greedy_approach(starting_node)
        greedy_path_lengths.append(Graph.calculate_path_length(path_greedy))
        execution_time = time.time() - start
        greedy_execution_times.append(execution_time)

    dfs_avg_results = sum(dfs_path_lengths) / num_of_samples, sum(dfs_execution_times) / num_of_nodes, "DFS Recurrent"
    bfs_avg_results = sum(bfs_path_lengths) / num_of_samples, sum(bfs_execution_times) / num_of_nodes, "BFS"
    greedy_avg_results = sum(greedy_path_lengths) / num_of_samples, sum(greedy_execution_times) / num_of_nodes, "Greedy"

    return dfs_avg_results, bfs_avg_results, greedy_avg_results


def approaches_analysis():
    """
        Analyse all approaches in respect to execution time, number of graph nodes and memory usage.
    """

    dfs_results = []
    bfs_results = []
    greedy_results = []
    a_star_results = []



    # num_of_nodes_to_test = 7
    # for i in range(2, num_of_nodes_to_test + 1):
    #
    #     num_of_nodes = i
    #
    #
    #     dfs_avg_results, bfs_avg_results, greedy_avg_results = try_dfs_and_bfs_and_greedy(num_of_samples, num_of_nodes)
    #     a_star_avg_results = try_a_star(num_of_samples, num_of_nodes)

    num_of_samples = 100
    num_of_nodes = 6

    dfs_avg_results, bfs_avg_results, greedy_avg_results = try_dfs_and_bfs_and_greedy(num_of_samples, num_of_nodes)
    a_star_avg_results = try_different_a_star_heuristics(num_of_samples, num_of_nodes)

    data = [dfs_avg_results, bfs_avg_results, greedy_avg_results]
    for res in a_star_avg_results:
        data.append(res)

    df = pd.DataFrame(data, columns=['path_length', 'execution_time', 'Method'])

    print(df)

    # plotting strip plot with seaborn
    sns.set(style="darkgrid")
    plt.figure(figsize=(9, 10))
    ax = sns.scatterplot(x="path_length", y="execution_time", hue="Method", data=df, s=250)

    # giving labels to x-axis and y-axis
    x_label = 'Avg path length for {} nodes'.format(num_of_nodes)
    y_label = 'Avg execution time for {} nodes'.format(num_of_nodes)
    ax.set(xlabel=x_label, ylabel=y_label)

    # giving title to the plot
    plt.title('Comparing efficiency of different algorithms for TSP')

    plt.plot([dfs_avg_results[0], dfs_avg_results[0]], [dfs_avg_results[1] + 0.05 * dfs_avg_results[1], 0 - 0.05 * dfs_avg_results[1]], linewidth=1)
    plt.annotate("Shortest possible path", [dfs_avg_results[0], dfs_avg_results[1]/2])

    # show plot
    plt.show()


def main():
    # test_random()
    approaches_analysis()


if __name__ == "__main__":
    main()
