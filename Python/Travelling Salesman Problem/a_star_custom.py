from graph import Graph, Node
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import List, Any


@dataclass(order=True)
class PrioritizedItem:
    priority: float
    item: Any = field(compare=False)


class AStarCustom:

    DEFAULT_HEURISTIC = 0

    def __init__(self, graph: Graph):
        self.graph = graph
        self.heuristic_choice = AStarCustom.DEFAULT_HEURISTIC
        self.num_of_heuristics = 6

    def heuristic(self, path: List[Node]) -> float:
        """
            Returns cost of the path.
                cost for heuristic0: path length + minimum distance from the last node in path to any node not visited
                cost for heuristic1: minimum distance from the last node in path to any node not visited
                cost for heuristic2: minimum distance from the last node in path to starting node
                cost for heuristic3:
                    minimum value of:
                        distance from the last node in path to any node not visited + distance from node not visited to
                        starting node
                cost for heuristic4: path length / number of nodes left to finish full cycle
                cost for heuristic5: path length + minimum distance from the last node in path to starting node
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
            return self.heuristic4(path)
        elif self.heuristic_choice == 5:
            return self.heuristic5(path)

    def heuristic0(self, path: List[Node]) -> float:
        path_length = Graph.calculate_path_length(path)
        if len(path) >= self.graph.num_of_nodes:
            return path_length + Graph.distance(path[0], path[-1])
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

    def heuristic4(self, path: List[Node]) -> float:
        path_length = Graph.calculate_path_length(path)
        return path_length / (self.graph.num_of_nodes + 1 - len(path))

    def heuristic5(self, path: List[Node]) -> float:
        path_length = Graph.calculate_path_length(path)
        return path_length + Graph.distance(path[0], path[-1])

    def a_star(self, start_node: Node) -> List[Node]:
        queue = PriorityQueue()
        queue.put(PrioritizedItem(self.heuristic([start_node]), [start_node]))

        while True:
            # print(queue.qsize())
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
