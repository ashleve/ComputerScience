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


def try_all_approaches(num_of_samples: int, num_of_nodes: int):
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

    a_star_custom = AStarCustom(graph)
    a_star_path_lengths = []
    a_star_execution_times = []
    for i in range(a_star_custom.num_of_heuristics):
        a_star_path_lengths.append([])
        a_star_execution_times.append([])

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

        for i in range(a_star_custom.num_of_heuristics):
            start = time.time()
            a_star_custom.graph = graph
            a_star_custom.heuristic_choice = i
            path_a_star = a_star_custom.a_star(starting_node)
            execution_time = time.time() - start
            a_star_path_lengths[i].append(Graph.calculate_path_length(path_a_star))
            a_star_execution_times[i].append(execution_time)

    dfs_avg_results = sum(dfs_path_lengths) / num_of_samples, sum(dfs_execution_times) / num_of_nodes, "DFS Recurrent"
    bfs_avg_results = sum(bfs_path_lengths) / num_of_samples, sum(bfs_execution_times) / num_of_nodes, "BFS"
    greedy_avg_results = sum(greedy_path_lengths) / num_of_samples, sum(greedy_execution_times) / num_of_nodes, "Greedy"
    a_star_avg_results = []
    for i in range(a_star_custom.num_of_heuristics):
        label = "A* heuristic " + str(i)
        a_star_avg_results.append(
            (sum(a_star_path_lengths[i]) / num_of_samples,
             sum(a_star_execution_times[i]) / num_of_samples,
             label)
        )

    data = [dfs_avg_results, bfs_avg_results, greedy_avg_results]
    data.extend(a_star_avg_results)

    return data


def approaches_analysis():
    """
        Analyse all approaches in respect to execution time, number of graph nodes and memory usage.
    """

    num_of_samples = 100
    num_of_nodes = 8

    data = try_all_approaches(num_of_samples, num_of_nodes)
    plot_path_lengths_and_execution_times(data, num_of_nodes, num_of_samples)

    results = []
    num_of_nodes_to_test = 9
    for i in range(2, num_of_nodes_to_test + 1):
        data = try_all_approaches(num_of_samples, i)
        results.append(data)
    plot_execution_times_and_number_of_nodes(results, num_of_samples)


def plot_memory_usage_and_number_of_nodes():
    pass


def plot_execution_times_and_number_of_nodes(results, num_of_samples):
    data = {"Number of nodes": []}
    for i in range(len(results)):
        for j in range(len(results[i])):
            if results[i][j][2] not in data:
                data[results[i][j][2]] = []
            data[results[i][j][2]].append(results[i][j][1])
        data["Number of nodes"].append(i + 2)
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
        'Comparing efficiency of different algorithms for TSP for {} samples'.format(num_of_samples),
        loc='left', fontsize=16,
        fontweight=0,
        color='orange'
    )

    # giving labels to x-axis and y-axis
    plt.xlabel("Number of nodes", fontsize=14)
    plt.ylabel("Execution time", fontsize=14)

    plt.show()


def plot_path_lengths_and_execution_times(data, num_of_nodes, num_of_samples):
    dfs_avg_results = data[0]
    df = pd.DataFrame(data, columns=['Path_length', 'Execution_time', 'Method'])

    # plotting strip plot with seaborn
    sns.set(style="darkgrid")
    plt.figure(figsize=(9, 10))
    sns.scatterplot(x="Path_length", y="Execution_time", hue="Method", data=df, s=250)

    # giving labels to x-axis and y-axis
    plt.xlabel('Avg path length for {} nodes'.format(num_of_nodes), fontsize=14)
    plt.ylabel('Avg execution time for {} nodes'.format(num_of_nodes), fontsize=14)

    # giving title to the plot
    plt.title(
        'Comparing efficiency of different algorithms for TSP for {} samples'.format(num_of_samples),
        loc='left',
        fontsize=16,
        fontweight=0,
        color='orange'
    )

    # plot shortest path line
    plt.plot(
        [dfs_avg_results[0], dfs_avg_results[0]],
        [dfs_avg_results[1] + 0.05 * dfs_avg_results[1], 0 - 0.05 * dfs_avg_results[1]],
        linewidth=1
    )
    plt.annotate("Shortest possible avg path", [dfs_avg_results[0], dfs_avg_results[1] / 2])

    # show plot
    plt.show()


def main():
    # test_random()
    approaches_analysis()


if __name__ == "__main__":
    main()
