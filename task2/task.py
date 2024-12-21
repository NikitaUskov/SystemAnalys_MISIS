import csv
import io


def main():
    file_path = input("Enter the path to the CSV file containing graph edges: ").strip()
    try:
        with open(file_path, newline='') as csv_file:
            metrics_result = process_graph_metrics(csv_file.read())
        print(metrics_result)
    except FileNotFoundError:
        print(f"File not found: {file_path}")


def parse_graph_edges(raw_csv_data: str):
    csv_reader = csv.reader(raw_csv_data.split('\n'))
    edges = []
    for row in csv_reader:
        if len(row) >= 2:
            edges.append((int(row[0]) - 1, int(row[1]) - 1))

    num_vertices = len(edges) + 1
    adjacency_list = [[] for _ in range(num_vertices)]
    reverse_adjacency_list = [[] for _ in range(num_vertices)]

    for source, destination in edges:
        adjacency_list[source].append(destination)
        reverse_adjacency_list[destination].append(source)

    return adjacency_list, reverse_adjacency_list, num_vertices


def compute_subtree_sizes_and_parents(graph, subtree_sizes, parents, current_vertex, parent_vertex=-1):
    if subtree_sizes[current_vertex] != 0:
        return

    subtree_sizes[current_vertex] = 1
    parents[current_vertex] = parent_vertex

    for neighbor in graph[current_vertex]:
        compute_subtree_sizes_and_parents(graph, subtree_sizes, parents, neighbor, current_vertex)
        subtree_sizes[current_vertex] += subtree_sizes[neighbor]


def compute_depths(graph, depths, current_vertex, current_depth=0):
    depths[current_vertex] = current_depth
    for neighbor in graph[current_vertex]:
        compute_depths(graph, depths, neighbor, current_depth + 1)


def calculate_subtree_sizes_and_parents(graph, num_vertices):
    subtree_sizes = [0] * num_vertices
    parents = [-1] * num_vertices

    for vertex in range(num_vertices):
        compute_subtree_sizes_and_parents(graph, subtree_sizes, parents, vertex)

    return subtree_sizes, parents


def calculate_depths(graph, root_vertex, num_vertices):
    depths = [0] * num_vertices
    compute_depths(graph, depths, root_vertex)
    return depths


def process_graph_metrics(raw_csv_data: str):
    adjacency_list, reverse_adjacency_list, num_vertices = parse_graph_edges(raw_csv_data)

    subtree_sizes, parents = calculate_subtree_sizes_and_parents(adjacency_list, num_vertices)
    root_vertex = parents.index(-1)

    depths = calculate_depths(adjacency_list, root_vertex, num_vertices)

    metrics = []
    for vertex in range(num_vertices):
        direct_children_count = len(adjacency_list[vertex])
        has_parent = 0 if vertex == root_vertex else 1
        indirect_children_count = subtree_sizes[vertex] - direct_children_count - 1
        vertex_depth = max(depths[vertex] - 1, 0)
        siblings_count = 0 if vertex == root_vertex else len(adjacency_list[parents[vertex]]) - 1

        metrics.append([direct_children_count, has_parent, indirect_children_count, vertex_depth, siblings_count])

    output = io.StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerows(metrics)

    return output.getvalue()


if __name__ == '__main__':
    main()
