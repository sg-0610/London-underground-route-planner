import pandas as pd
import matplotlib.pyplot as plt
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra
from mst import kruskal


# Step 1: Load the data from the Excel file
def load_data(file_path):
    data = pd.read_excel(file_path, header=None)
    data.columns = ["Line", "Station1", "Station2", "Duration"]
    data.dropna(subset=["Station1", "Station2", "Duration"], inplace=True)
    data["Station1"] = data["Station1"].astype(str).str.strip()
    data["Station2"] = data["Station2"].astype(str).str.strip()
    return data


# Step 2: Create the graph with all stations and edges
def create_graph(data):
    unique_stations = sorted(set(data["Station1"]).union(set(data["Station2"])))
    station_to_index = {station: idx for idx, station in enumerate(unique_stations)}
    graph = AdjacencyListGraph(len(unique_stations), directed=False, weighted=True)

    for _, row in data.iterrows():
        u, v = station_to_index[row["Station1"]], station_to_index[row["Station2"]]
        weight = row["Duration"]
        if not graph.has_edge(u, v):  # Avoid duplicates
            graph.insert_edge(u, v, weight)

    return graph, station_to_index, unique_stations


# Step 3: Find and close redundant edges using Kruskal's MST
def find_and_close_edges(graph, station_to_index, unique_stations):
    mst_graph = kruskal(graph)  # Compute MST using Kruskal's algorithm
    original_edges = set(graph.get_edge_list())
    mst_edges = set(mst_graph.get_edge_list())
    redundant_edges = original_edges - mst_edges

    # Map redundant edges back to station names
    closed_edges = []
    for u, v in redundant_edges:
        start_station = unique_stations[u]
        end_station = unique_stations[v]
        closed_edges.append((start_station, end_station))

    # Remove redundant edges from the graph
    for u, v in redundant_edges:
        graph.delete_edge(u, v)

    return graph, closed_edges


# Step 4: Analyze the graph (journey durations and longest path)
def analyze_graph(graph, unique_stations):
    n = len(unique_stations)
    durations = []
    paths = {}
    for source in range(n):
        distances, predecessors = dijkstra(graph, source)
        for target in range(source + 1, n):
            if distances[target] != float("inf"):
                durations.append(distances[target])
                paths[(source, target)] = (distances[target], predecessors)
    longest_duration = max(durations)
    longest_pair = max(paths, key=lambda pair: paths[pair][0])
    return durations, longest_duration, longest_pair, paths


# Step 5: Plot histogram
def plot_histogram(durations, title):
    plt.figure(figsize=(10, 6))
    plt.hist(durations, bins=20, edgecolor="black", alpha=0.7)
    plt.xlabel("Journey Duration (minutes)")
    plt.ylabel("Frequency")
    plt.title(title)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()


# Step 6: Reconstruct the longest path
def reconstruct_path(predecessors, start, end):
    path = []
    while end is not None:
        path.append(end)
        end = predecessors[end]
    path.reverse()
    return path


# Main function
if __name__ == "__main__":
    file_path = "London Underground Data.xlsx"  # Path to the dataset
    data = load_data(file_path)

    # Original graph analysis (Task 3a)
    graph_original, station_to_index, unique_stations = create_graph(data)
    durations_original, longest_original, pair_original, paths_original = analyze_graph(graph_original, unique_stations)

    # Reconstruct the longest path in the original graph
    original_longest_path_indices = reconstruct_path(
        paths_original[pair_original][1], pair_original[0], pair_original[1]
    )
    original_longest_path = [unique_stations[i] for i in original_longest_path_indices]

    # Reduced graph analysis (Task 4b)
    reduced_graph, closed_edges = find_and_close_edges(graph_original, station_to_index, unique_stations)
    durations_reduced, longest_reduced, pair_reduced, paths_reduced = analyze_graph(reduced_graph, unique_stations)

    # Reconstruct the longest path in the reduced graph
    reduced_longest_path_indices = reconstruct_path(
        paths_reduced[pair_reduced][1], pair_reduced[0], pair_reduced[1]
    )
    reduced_longest_path = [unique_stations[i] for i in reduced_longest_path_indices]

    # Plot histograms
    plot_histogram(durations_original, "Original Network: Journey Durations")
    plot_histogram(durations_reduced, "Reduced Network: Journey Durations")

    # Display results
    print(f"Original Network: Longest journey duration = {longest_original} minutes")
    print(f"Reduced Network: Longest journey duration = {longest_reduced} minutes")

    print("\nLongest path in Original Network:")
    print(" -> ".join(original_longest_path))

    print("\nLongest path in Reduced Network:")
    print(" -> ".join(reduced_longest_path))

    # Insights
    print("\nInsights:")
    print("- Histogram comparison shows how journey durations are affected by line closures.")
    print(f"- Longest journey duration changed by {longest_reduced - longest_original} minutes.")
    print("- Path comparison highlights how connectivity changes after closures.")
    print("\nClosed Line Sections:")
    for edge in closed_edges:
        print(f"{edge[0]} -- {edge[1]}")