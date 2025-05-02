import heapq

class CityGraph:
    def __init__(self):
        self.graph = {}
    
    def add_edge(self, city1, city2, distance):
        if city1 not in self.graph:
            self.graph[city1] = {}
        if city2 not in self.graph:
            self.graph[city2] = {}
        self.graph[city1][city2] = distance
        self.graph[city2][city1] = distance

class CityState:
    def __init__(self, city, parent=None, cost=0):
        self.city = city
        self.parent = parent
        self.cost = cost

    def __eq__(self, other):
        return self.city == other.city

    def __lt__(self, other):
        return self.heuristic() < other.heuristic()

    def __hash__(self):
        return hash(self.city)

    def heuristic(self, goal_city, straight_line_distances):
        # Use straight-line distance as heuristic (must be admissible)
        return straight_line_distances.get(self.city, {}).get(goal_city, 0)

def best_first_search_cities(graph, start, goal, straight_line_distances):
    open_list = []
    closed_set = set()
    start_state = CityState(start)
    heapq.heappush(open_list, (start_state.heuristic(goal, straight_line_distances), start_state))
    
    while open_list:
        _, current = heapq.heappop(open_list)
        
        if current.city == goal:
            path = []
            total_distance = current.cost
            while current.parent:
                path.append(current.city)
                current = current.parent
            path.append(start)
            return path[::-1], total_distance
        
        closed_set.add(current.city)
        
        for neighbor, distance in graph.graph[current.city].items():
            if neighbor not in closed_set:
                new_cost = current.cost + distance
                new_state = CityState(neighbor, current, new_cost)
                heapq.heappush(open_list, 
                             (new_state.heuristic(goal, straight_line_distances), new_state))
    
    return None, None  # No path found

# Example usage
city_graph = CityGraph()
city_graph.add_edge('A', 'B', 4)
city_graph.add_edge('A', 'C', 2)
city_graph.add_edge('B', 'C', 1)
city_graph.add_edge('B', 'D', 5)
city_graph.add_edge('C', 'D', 8)
city_graph.add_edge('C', 'E', 10)
city_graph.add_edge('D', 'E', 2)

# Straight-line distances (heuristic) - must be <= actual distance
straight_line_dist = {
    'A': {'E': 10},
    'B': {'E': 8},
    'C': {'E': 7},
    'D': {'E': 2},
    'E': {'E': 0}
}

start_city = 'A'
goal_city = 'E'
path, distance = best_first_search_cities(city_graph, start_city, goal_city, straight_line_dist)
print("Cities Path Solution:", path)
print("Total Distance:", distance)
