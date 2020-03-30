from graph import Graph, Node
from typing import List


class DFS:

    def __init__(self, graph: Graph):
        self.graph = graph

    def depth_first_search(self, start_node: Node) -> List[List[Node]]:
        return self._depth_first_search_recurrent([start_node])

    def _depth_first_search_recurrent(self, path: List[Node]) -> List[List[Node]]:
        all_paths = []
        for node in self.graph[path[-1]]:
            if node not in path or (node == path[0] and len(path) >= self.graph.num_of_nodes):
                all_paths += self._depth_first_search_recurrent(path + [node])

        if not all_paths and path[0] == path[-1]:
            return [path]

        return all_paths
