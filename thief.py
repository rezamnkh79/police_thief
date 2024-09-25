from agent import Agent
from agent_type import AgentType

class Thief(Agent):
    def __init__(self, agent_id, graph, start_node=None):
        super().__init__(agent_id, graph, start_node)
        self.agent_type = AgentType.THIEF

    def alpha_beta_move(self, depth, alpha, beta, agents_positions):
        current_position = self.get_position()
        neighbors = self.graph.get_neighbors(current_position)

        police_positions = agents_positions.get("polices", [])
        available_moves = [node for node in neighbors if node not in police_positions]

        if not available_moves or depth == 0:
            return current_position

        best_move = None

        for move in available_moves:
            self.set_position(move)

            new_agents_positions = agents_positions.copy()
            new_agents_positions["thieves"] = [self.get_position()]

            evaluation = self.simulate_policeman_move(new_agents_positions, depth - 1, alpha, beta)

            self.set_position(current_position)

            if evaluation > alpha:
                alpha = evaluation
                best_move = move

            if beta <= alpha:
                break

        return best_move if best_move is not None else current_position

    def simulate_policeman_move(self, agents_positions, depth, alpha, beta):
        police_positions = agents_positions.get("polices", [])
        current_position = self.get_position()

        score = -sum(1 for police in police_positions if police in self.graph.get_neighbors(current_position))

        if depth == 0:
            return score

        for police in police_positions:
            police_neighbors = self.graph.get_neighbors(police)
            for new_pos in police_neighbors:
                temp_agents_positions = agents_positions.copy()
                temp_agents_positions["polices"] = [new_pos]

                score = max(score, self.simulate_policeman_move(temp_agents_positions, depth - 1, alpha, beta))

                beta = min(beta, score)
                if beta <= alpha:
                    break

        return score

    def move(self, agents_positions=None):
        best_move = self.alpha_beta_move(depth=3, alpha=float('-inf'), beta=float('inf'), agents_positions=agents_positions)

        self.set_position(best_move)
        return best_move

    def set_position(self, new_position):
        self.current_node = new_position