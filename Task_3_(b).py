import pandas as pd
import matplotlib.pyplot as plt
from dijkstra import dijkstra
from adjacency_list_graph import AdjacencyListGraph

# Step 1: Import London Underground Network Data
data = pd.read_excel("London Underground Data.xlsx", header=None)
data.columns = ["Line", "Station1", "Station2", "Duration"]

# Ensure valid station names and remove NaN rows
data = data.dropna(subset=["Station1", "Station2", "Duration"])
data['Station1'] = data['Station1'].astype(str).str.strip()
data['Station2'] = data['Station2'].astype(str).str.strip()

# Extract unique stations and map them to indices
stations = sorted(set(data['Station1']).union(set(data['Station2'])))
station_to_index = {station: idx for idx, station in enumerate(stations)}
n = len(stations)

# Step 2: Initialize the graph for stops
graph_stops = AdjacencyListGraph(n, directed=False, weighted=True)
added_edges = set()

for _, row in data.iterrows():
    source = station_to_index[row['Station1']]
    target = station_to_index[row['Station2']]

    # Ensure the edge is added only once and weight is set to 1 for stops
    if (source, target) not in added_edges and (target, source) not in added_edges:
        graph_stops.insert_edge(source, target, 1)
        added_edges.add((source, target))

# Step 3: Calculate journey durations in terms of stops
durations_stops = []  # To store all journey durations (in stops)
paths_stops = {}  # To store paths for later identification of the longest path

for source in range(n):  # For each station
    distances, predecessors = dijkstra(graph_stops, source)  # Run Dijkstra’s algorithm
    for target in range(source + 1, n):  # Only consider unique pairs (A->B, not B->A)
        if distances[target] != float('inf'):  # Exclude unreachable pairs
            durations_stops.append(distances[target])  # Store the journey duration
            paths_stops[(source, target)] = (distances[target], predecessors)

# Step 4: Plot histogram of journey durations (stops)
plt.figure(figsize=(10, 6))
plt.hist(durations_stops, bins=range(1, max(durations_stops) + 2), edgecolor='black')
plt.xlabel("Journey Duration (Number of Stops)")
plt.ylabel("Frequency")
plt.title("Distribution of Journey Durations (Stops)")
plt.show()

# Step 5: Identify the longest journey (stops) and its path
longest_duration_stops = max(durations_stops)
longest_pair_stops = max(paths_stops, key=lambda pair: paths_stops[pair][0])  # Pair with longest duration
longest_path_duration_stops, predecessors_stops = paths_stops[longest_pair_stops]


# Function to reconstruct the path from predecessors
def reconstruct_path(predecessors, start, end):
    path = []
    while end is not None and end != -1:
        path.append(end)
        end = predecessors[end]
    path.reverse()  # Reverse the path to start from the source
    return path


longest_path_indices_stops = reconstruct_path(predecessors_stops, longest_pair_stops[0], longest_pair_stops[1])
longest_path_stations_stops = [stations[i] for i in longest_path_indices_stops]

# Display the longest journey details (stops)
print(f"Longest journey duration (by stops): {longest_duration_stops} stops")
print("Path for the longest journey (in order):")
print(" -> ".join(longest_path_stations_stops))