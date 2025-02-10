import time
import random
import matplotlib.pyplot as plt
from adjacency_list_graph import AdjacencyListGraph  # Importing from the book "Introduction to Algorithms" (4th
# edition)
from dijkstra import dijkstra  # Importing from the book "Introduction to Algorithms" (4th


# edition)

# Step 1: Create a random tube network with n stations and random journey durations
def generate_random_tube_network(n, edge_probability=0.1, min_weight=1, max_weight=15):
    """
    Generate an artificial tube network with n stations and random journey durations.
    Arguments:
        n -- number of stations (vertices)
        edge_probability -- probability of an edge (journey) existing between two stations
        min_weight -- minimum journey duration in minutes
        max_weight -- maximum journey duration in minutes
    Returns:
        graph -- the generated tube network as an adjacency list graph
    """
    graph = AdjacencyListGraph(n, directed=False, weighted=True)
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < edge_probability:
                weight = random.randint(min_weight, max_weight)
                graph.insert_edge(u, v, weight)
    return graph


# Step 2: Calculate the execution time of Dijkstra's algorithm
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
        dijkstra(graph, source)  # Use Dijkstra's algorithm
        end_time = time.time()
        total_time += (end_time - start_time) * 1000  # Change the time to milliseconds
    return total_time / repetitions


# Step 3: Determine the average execution time for various network sizes
network_sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
execution_times = []

for n in network_sizes:
    graph = generate_random_tube_network(n)  # Create network of size n
    source_vertex = 0  # random starting station
    avg_time = measure_execution_time(graph, source_vertex)  # Average time measurement
    execution_times.append(avg_time)
    print(f"Network size: {n}, Average execution time: {avg_time:.2f} ms")

# Step 4: Plot results for empirical time complexity
plt.figure(figsize=(10, 6))
plt.plot(network_sizes, execution_times, marker='o', label='Execution Time')
plt.xlabel('Network Size (Number of Stations)')
plt.ylabel('Average Execution Time (ms)')
plt.title('Average Execution Time vs Network Size')
plt.grid(True)
plt.legend()
plt.show()
