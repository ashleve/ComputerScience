from graph import Graph, Node
from typing import List


class BFS:

    def __init__(self, graph: Graph):
        self.graph = graph

    def breadth_first_search(self, start_node: Node) -> List[List[Node]]:
        all_paths = [[start_node]]
        for i in range(self.graph.num_of_nodes):
            new_paths = []
            for path in all_paths:
                for node in self.graph[path[-1]]:
                    if node not in path or (node == path[0] and len(path) >= self.graph.num_of_nodes):
                        new_paths.append(path + [node])
            all_paths = new_paths

        return all_paths

