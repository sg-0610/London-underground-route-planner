# Importing necessary modules and functions from the desired library "Introduction to Algorithms" (4th edition)
from dijkstra import dijkstra  # Import the dijkstra function from dijkstra.py
from adjacency_list_graph import AdjacencyListGraph

# Step 1: The first step is to create the graph (tube network) using AdjencyListGraph class
vertices = ['A', 'B', 'C', 'D', 'E']  # Available stations
edges = [
    ('A', 'B', 8),  # A to B- 8 minutes
    ('A', 'D', 7),  # A to D- 7 minutes
    ('B', 'C', 3),  # B to C- 3 minutes
    ('C', 'E', 5),  # C to E- 5 minutes
    ('D', 'E', 1)   # D to E-1 minute
]

# Set the graph with 5 vertices, directed=False, weighted=True
graph = AdjacencyListGraph(len(vertices), directed=False, weighted=True)

# Put the edges into the graph
for edge in edges:
    graph.insert_edge(vertices.index(edge[0]), vertices.index(edge[1]), edge[2])

# Step 3: Get the user input for source and destination stations
source_station = input(f"Enter the source station (Choose from {vertices}): ").upper()
destination_station = input(f"Enter the destination station (Choose from {vertices}): ").upper()

# Guarantee rational input
if source_station not in vertices or destination_station not in vertices:
    print("Invalid station name(s). Please enter valid stations from the list.")
else:
    # Step 4: Determine the shortest route from source to destination
    source_vertex = vertices.index(source_station)  # Obtain the index of the source station
    d, pi = dijkstra(graph, source_vertex)  # Call the imported Dijkstra function

    # Step 5: Rebuild the shortest path
    target_vertex = vertices.index(destination_station)  # Get the index of the destination station
    path = []
    current_vertex = target_vertex

    while current_vertex is not None:
        path.insert(0, vertices[current_vertex])  # Insert each station at the beginning of the path list
        current_vertex = pi[current_vertex]  # Go to the predecessor

    # Step 6: Show the shortest route and journey duration
    print(f"Shortest path from {source_station} to {destination_station}: {' -> '.join(path)}")
    print(f"Journey duration: {d[target_vertex]} minutes")