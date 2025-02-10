import pandas as pd
import matplotlib.pyplot as plt
from dijkstra import dijkstra  # Importing necessary libraries from "Introduction to Algorithms" 4th Edition
from adjacency_list_graph import AdjacencyListGraph # Importing necessary libraries from "Introduction to Algorithms"
# 4th Edition

# Step 1: Import London Underground Network Data
data = pd.read_excel("London Underground Data.xlsx", header=None)
data.columns = ["Line", "Station1", "Station2", "Duration"]  # column name based on the file format

# Make sure that all station names are strings and handle any NaN values
data['Station1'] = data['Station1'].astype(str).fillna('Unknown')
data['Station2'] = data['Station2'].astype(str).fillna('Unknown')

# Select distinctive stations and create a mapping
stations = sorted(set(data['Station1']).union(set(data['Station2'])))
station_to_index = {station: index for index, station in enumerate(stations)}
n = len(stations)

# Step 2: Define the graph with journey times as weights
graph = AdjacencyListGraph(n, directed=False, weighted=True)
added_edges = set()  # Track added edges to avoid duplicates

for _, row in data.iterrows():
    source = station_to_index[row['Station1']]
    target = station_to_index[row['Station2']]
    duration = row['Duration']

    # Only add the edge if it has not been added before
    if (source, target) not in added_edges and (target, source) not in added_edges:
        graph.insert_edge(source, target, duration)
        added_edges.add((source, target))  # Mark this edge as added

# Step 3: Calculate journey durations for all station pairs
durations = []  # To store all unique journey durations
paths = {}  # To store paths for later identification of the longest path

for source in range(n):  # For every station
    distances, predecessors = dijkstra(graph, source)  # Use Dijkstra’s algorithm
    for target in range(source + 1, n):  # Only use unique pairs (A->B, not B->A)
        if distances[target] != float('inf'):  # Exclude unapproachable pairs
            durations.append(distances[target])  # Stock the journey duration
            paths[(source, target)] = (distances[target], predecessors)  # Store path information

# Step 4: Plot histogram of journey durations
plt.figure(figsize=(10, 6))
plt.hist(durations, bins=20, edgecolor='black')
plt.xlabel("Journey Duration (minutes)")
plt.ylabel("Frequency")
plt.title("Distribution of Journey Durations in the London Underground Network")
plt.show()

# Step 5: Find the longest journey duration and its path
longest_duration = max(durations)
longest_pair = max(paths, key=lambda pair: paths[pair][0])  # Get the pair with the longest duration
longest_path_duration, predecessors = paths[longest_pair]


# Function to rebuild the path from predecessors
def reconstruct_path(predecessors, start, end):
    path = []
    while end is not None:
        path.append(end)
        end = predecessors[end]
    path.reverse()  # Reverse the path to start from the source
    return path


# Reconstruct the longest path
longest_path_indices = reconstruct_path(predecessors, longest_pair[0], longest_pair[1])
longest_path_stations = [stations[i] for i in longest_path_indices]

# Display the longest journey details
print(f"Longest journey duration: {longest_duration} minutes")
print("Path for the longest journey (in order):")
print(" -> ".join(longest_path_stations))