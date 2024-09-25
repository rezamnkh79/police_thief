import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, directed=False):
        """Initialize the graph. By default, it creates an undirected graph."""
        self.directed = directed
        if directed:
            self.graph = nx.DiGraph()
        else:
            self.graph = nx.Graph()

    def add_node(self, node):
        """Add a single node to the graph."""
        self.graph.add_node(node)

    def add_nodes(self, nodes):
        """Add multiple nodes to the graph."""
        self.graph.add_nodes_from(nodes)

    def add_edge(self, u, v):
        """Add an edge between two nodes u and v."""
        self.graph.add_edge(u, v)

    def add_edges(self, edges):
        """Add multiple edges to the graph."""
        self.graph.add_edges_from(edges)

    def remove_node(self, node):
        """Remove a node from the graph."""
        self.graph.remove_node(node)

    def remove_edge(self, u, v):
        """Remove an edge between two nodes u and v."""
        self.graph.remove_edge(u, v)

    def get_nodes(self):
        """Return a list of nodes in the graph."""
        return list(self.graph.nodes)

    def get_edges(self):
        """Return a list of edges in the graph."""
        return list(self.graph.edges)

    def node_degrees(self):
        """Return a dictionary of nodes and their degrees."""
        return dict(self.graph.degree)

    def get_neighbors(self, node):
        return list(self.graph.neighbors(node))

    def display_graph(self, color_map = None):
        """Display the graph using matplotlib."""
        pos = nx.spring_layout(self.graph)
        if color_map is None:
            nx.draw(self.graph, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='gray', font_size=10)
        else:
            nx.draw(self.graph, pos, with_labels=True, node_color=color_map, node_size=1500, edge_color='gray', font_size=10)
        plt.show()

# Example Usage
if __name__ == "__main__":
    g = Graph()
    g.add_nodes([1, 2, 3, 4])
    color_map = ["blue", "blue", "red", "blue"]
    g.add_edges([[1, 2], [1, 3], [2, 4]])
    print("Nodes:", g.get_nodes())
    print("Edges:", g.get_edges())
    print("Node degrees:", g.node_degrees())
    g.display_graph(color_map)