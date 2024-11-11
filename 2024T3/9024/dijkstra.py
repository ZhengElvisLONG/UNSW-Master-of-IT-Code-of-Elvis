import heapq

def dijkstra(graph, start, target):
    # Number of nodes in the graph
    n = len(graph)
    
    # Initialize distances with infinity and set the distance of the start node to 0
    distances = [float('inf')] * n
    distances[start] = 0

    # Priority queue to store the nodes to visit, initialized with the start node
    priority_queue = [(0, start)]  # (distance, node)
    
    while priority_queue:
        # Get the node with the smallest distance
        current_distance, current_node = heapq.heappop(priority_queue)

        # If we reached the target node, return the distance
        if current_node == target:
            return current_distance

        # If a shorter path to current_node has been found, skip this node
        if current_distance > distances[current_node]:
            continue

        # Explore neighbors
        for neighbor in range(n):
            weight = graph[current_node][neighbor]
            if weight > 0:  # There's an edge
                distance = current_distance + weight
                # Only consider this new path if it's better
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
    
    # If the target node is unreachable, return infinity
    return float('inf')

# Define the adjacency matrix as provided in the input
graph = [
    [0, 3, 3, 0, 5, 0, 0, 0],
    [0, 0, 0, 4, 0, 4, 0, 0],
    [0, 3, 0, 0, 0, 3, 0, 0],
    [4, 0, 0, 0, 6, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 5, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

# Calculate the shortest distance from Node 3 to Node 7 (index 2 to 6)
shortest_distance = dijkstra(graph, 3, 7)
print (shortest_distance)
