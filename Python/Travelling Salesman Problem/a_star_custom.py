from graph import Graph, Node
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import List, Any


@dataclass(order=True)
class PrioritizedItem:
    priority: float
    item: Any = field(compare=False)


class AStarCustom:

    DEFAULT_HEURISTIC = 3

    def __init__(self, graph: Graph):
        self.graph = graph
        self.heuristic_choice = AStarCustom.DEFAULT_HEURISTIC
        self.num_of_heuristics = 4

    def heuristic(self, path: List[Node]) -> float:
        """
            Returns cost of path.
                cost:  minimum distance from the last node in path to any node not visited
        """
        if self.heuristic_choice == 0:
            return self.heuristic0(path)
        elif self.heuristic_choice == 1:
            return self.heuristic1(path)
        elif self.heuristic_choice == 2:
            return self.heuristic2(path)
        elif self.heuristic_choice == 3:
            return self.heuristic3(path)
        elif self.heuristic_choice == 4:
            pass

    def heuristic0(self, path: List[Node]) -> float:
        if len(path) >= self.graph.num_of_nodes:
            return Graph.calculate_path_length(path) + Graph.distance(path[0], path[-1])
        path_length = Graph.calculate_path_length(path)
        costs = [path_length + Graph.distance(node, path[-1]) for node in self.graph[path[-1]] - set(path)]
        return min(costs)

    def heuristic1(self, path: List[Node]) -> float:
        if len(path) >= self.graph.num_of_nodes:
            return Graph.distance(path[0], path[-1])
        costs = [Graph.distance(node, path[-1]) for node in self.graph[path[-1]] - set(path)]
        return min(costs)

    def heuristic2(self, path: List[Node]) -> float:
        return Graph.distance(path[0], path[-1])

    def heuristic3(self, path: List[Node]) -> float:
        if len(path) >= self.graph.num_of_nodes:
            return Graph.distance(path[0], path[-1])
        costs = [Graph.distance(node, path[-1]) + Graph.distance(node, path[0]) for node in self.graph[path[-1]] - set(path)]
        return min(costs)

    def a_star(self, start_node: Node) -> List[Node]:
        queue = PriorityQueue()
        queue.put(PrioritizedItem(self.heuristic([start_node]), [start_node]))

        while True:
            current_path = queue.get().item  # deletes first element from queue

            if len(current_path) >= self.graph.num_of_nodes:
                return current_path + [start_node]

            # for each node that can be visited from last node in current path
            for node in self.graph[current_path[-1]] - set(current_path):
                path_extended = current_path + [node]
                cost = self.heuristic(path_extended)
                queue.put(PrioritizedItem(cost, path_extended))
            # print_queue(queue)


def print_queue(some_queue: PriorityQueue):
    queue = some_queue
    print("---------------------------------------------------------------------------")
    elements = []
    while not queue.empty():
        el = queue.get()
        elements.append(el)
        print(el)
    for el in elements:
        queue.put(el)
