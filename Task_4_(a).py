
import pandas as pd
from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal  # Using the Kruskal's MST algorithm from the library ("Introduction to Algorithms" 4th edition)


# Step 1: Load the data from the Excel file
def load_data(file_path):
    """Load journey data and prepare it for the graph."""
    data = pd.read_excel(file_path, header=None)
    data.columns = ['Line', 'Start_Station', 'End_Station', 'Duration']
    data.dropna(subset=['Start_Station', 'End_Station', 'Duration'], inplace=True)
    return data


# Step 2: Create the graph with all unique stations
def create_graph(data):
    """Initialize the graph with vertices and edges based on the data."""
    # Get unique stations from both Start_Station and End_Station columns
    unique_stations = pd.concat([data['Start_Station'], data['End_Station']]).unique()
    graph = AdjacencyListGraph(len(unique_stations), directed=False, weighted=True)

    # Map each station to a unique index
    station_to_index = {station: idx for idx, station in enumerate(unique_stations)}

    # Add edges to the graph
    for _, row in data.iterrows():
        u = station_to_index[row['Start_Station']]
        v = station_to_index[row['End_Station']]
        weight = row['Duration']
        if not graph.has_edge(u, v):  # Avoid duplicate edges
            graph.insert_edge(u, v, weight)

    return graph, station_to_index, unique_stations


# Step 3: Find redundant edges using Kruskal's MST algorithm
def find_redundant_edges(graph):
    """Identify edges that are not part of the MST."""
    mst_graph = kruskal(graph)  # Call the Kruskal's algorithm from the imported module
    original_edges = set(graph.get_edge_list())
    mst_edges = set(mst_graph.get_edge_list())
    redundant_edges = original_edges - mst_edges
    return redundant_edges


# Step 4: Convert the redundant edges back to station names for output
def list_closed_sections(redundant_edges, station_to_index, vertices):
    closed_sections = []
    for u, v in redundant_edges:
        start_station = vertices[u]
        end_station = vertices[v]
        closed_sections.append(f"{start_station} -- {end_station}")
    return closed_sections


# Main code execution
file_path = 'London Underground Data.xlsx'
data = load_data(file_path)
graph, station_to_index, vertices = create_graph(data)
redundant_edges = find_redundant_edges(graph)

# Output the list of closed sections
closed_sections = list_closed_sections(redundant_edges, station_to_index, vertices)
print("Closed line sections:")
for section in closed_sections:
    print(section)
