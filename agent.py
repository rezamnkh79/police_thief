import random
from graph import Graph

class Agent:
    def __init__(self, agent_id, graph: Graph, start_node=None):
        """
        Initialize the Agent with a graph and a starting node.

        :param graph: A Graph object.
        :param start_node: The node from which the agent starts. If not provided, a random node is chosen.
        """
        self.turn_counter = 0
        self.agent_id = agent_id
        self.agent_type = None
        self.graph = graph  # Use the networkx graph from the Graph class
        if start_node is None:
            # Choose a random start node if not provided
            self.current_node = random.choice(list(self.graph.get_nodes()))
        else:
            self.current_node = start_node

    def move(self, agents_positions=None):
        """
        Move the agent to a random neighbor of the current node.
        If the current node has no neighbors, the agent stays in place.
        """
        neighbors = list(self.graph.get_neighbors(self.current_node))
        if neighbors:
            self.current_node = random.choice(neighbors)
        else:
            print(f"Node {self.current_node} has no neighbors. Staying at the same node.")
        return self.current_node

    def get_position(self):
        """Return the current position of the agent."""
        return self.current_node

# Example Usage
if __name__ == "__main__":
    # Create a graph
    g = Graph()
    g.add_nodes([1, 2, 3, 4, 5])
    g.add_edges([(1, 2), (1, 3), (2, 4), (3, 5)])

    # Create an agent that starts at node 1
    agent = Agent(1, g, start_node=1)

    # Move the agent and print its new position
    for i in range(5):
        new_position = agent.move()
        print(f"Move {i+1}: Agent is now at node {new_position}")
