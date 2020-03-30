import random
import math


class Node:
    def __init__(self, name: str, x: float, y: float):
        self.name = name
        self.x = x
        self.y = y

    def __repr__(self):
        return self.name


class Graph:

    def __init__(self, num_of_nodes):
        self.graph = None
        self.num_of_nodes = None
        self.reset_graph(num_of_nodes)

    def reset_graph(self, num_of_nodes):
        self.graph = {}
        self.num_of_nodes = num_of_nodes
        self.initialise_randomly(self.num_of_nodes)

    def initialise_randomly(self, num_of_nodes):
        nodes = []
        for i in range(num_of_nodes):
            node = Node(chr(65 + i), x=random.randint(0, 100), y=random.randint(0, 100))
            nodes.append(node)

        for node in nodes:
            self.graph[node] = set(nodes) - {node}

    @staticmethod
    def distance(node1: Node, node2: Node) -> float:
        return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)

    @staticmethod
    def calculate_path_length(path: list) -> float:
        return sum(map(Graph.distance, path, path[1:]))

    @staticmethod
    def get_shortest_path(paths: list) -> tuple:
        shortest_path = min(paths, key=Graph.calculate_path_length)
        return shortest_path, Graph.calculate_path_length(shortest_path)

    @staticmethod
    def print_all_paths(paths: list):
        for p in paths:
            print(p, "length:", Graph.calculate_path_length(p))
        print("Number of Hamilton Cycles found:", len(paths))

    def __getitem__(self, item):
        return self.graph.__getitem__(item)

    def __len__(self):
        return len(self.graph)
