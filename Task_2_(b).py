import time
import random
import matplotlib.pyplot as plt
from adjacency_list_graph import AdjacencyListGraph  # From "Introduction to Algorithms" (4th edition)
from dijkstra import dijkstra  # From "Introduction to Algorithms" (4th edition)


# Step 1: The First step is to create a random tube network with n stations, where weights represent number of stops
def generate_random_tube_network(n, edge_probability=0.1):
    """
    Generate an artificial tube network with n stations.
    Each edge weight is 1, representing one stop.

    Arguments:
        n -- number of stations (vertices)
        edge_probability -- probability of an edge (journey) existing between two stations

    Returns:
        graph -- the generated tube network as an adjacency list graph
    """
    graph = AdjacencyListGraph(n, directed=False, weighted=True)
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < edge_probability:
                weight = 1  # Weight is set o 1 to show one stop
                graph.insert_edge(u, v, weight)
    return graph


# Step 2: Determine the execution time of Dijkstra's algorithm
def measure_execution_time(graph, source, repetitions=5):
    """
    Measure the execution time for Dijkstra's algorithm on the tube network.

    Arguments:
        graph -- the tube network (AdjacencyListGraph)
        source -- the source station index
        repetitions -- number of times to repeat for averaging

    Returns:
        average_time -- average execution time in milliseconds
    """
    total_time = 0
    for _ in range(repetitions):
        start_time = time.time()
        dijkstra(graph, source)  # Apply Dijkstra's algorithm
        end_time = time.time()
        total_time += (end_time - start_time) * 1000  # Convert to milliseconds
    return total_time / repetitions


# Step 3: Find out the average execution time for various network sizes
network_sizes = [1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]  # As per the specification
execution_times = []

for n in network_sizes:
    graph = generate_random_tube_network(n, edge_probability=0.1)  # Make a network of size n
    source_vertex = 0  # Start from the first station
    avg_time = measure_execution_time(graph, source_vertex)  # Compute average time
    execution_times.append(avg_time)
    print(f"Network size: {n}, Average execution time: {avg_time:.2f} ms")

# Step 4: Lastly, Plot results for empirical time complexity
plt.figure(figsize=(10, 6))
plt.plot(network_sizes, execution_times, marker='o', label='Execution Time')
plt.xlabel('Network Size (Number of Stations)')
plt.ylabel('Average Execution Time (ms)')
plt.title('Average Execution Time vs Network Size (Number of Stops)')
plt.grid(True)
plt.legend()
plt.show()
