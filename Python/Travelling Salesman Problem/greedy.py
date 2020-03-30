from graph import Graph, Node
from typing import List


class Greedy:

    def __init__(self, graph: Graph):
        self.graph = graph

    def greedy_approach(self, start_node: Node) -> List[Node]:
        path = [start_node]
        while True:
            distances = [(node, Graph.distance(node, path[-1])) for node in self.graph[path[-1]] - set(path)]
            if not distances or len(path) == self.graph.num_of_nodes:
                return path + [start_node]
            path.append(min(distances, key=lambda t: t[1])[0])
