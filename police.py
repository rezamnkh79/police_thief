from agent import Agent
from agent_type import AgentType
from collections import deque


class Police(Agent):
    def __init__(self, agent_id, graph, start_node=None):
        super().__init__(agent_id, graph, start_node)
        self.agent_type = AgentType.POLICE

    def alpha_beta_search(self, depth, alpha, beta, maximizing_player, goal_position):
        if depth == 0:
            return self.evaluate_position()

        neighbors = self.graph.get_neighbors(self.current_node)
        if maximizing_player:
            max_eval = float('-inf')
            for neighbor in neighbors:
                self.set_position(neighbor)
                eval = self.alpha_beta_search(depth - 1, alpha, beta, False, goal_position)
                self.set_position(self.current_node)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for neighbor in neighbors:
                self.set_position(neighbor)
                eval = self.alpha_beta_search(depth - 1, alpha, beta, True, goal_position)
                self.set_position(self.current_node)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # هرس
            return min_eval

    def move(self, agents_positions=None):
        thieves_positions = agents_positions["thieves"]
        closest_pacman = self.find_closest_pacman(thieves_positions)

        if closest_pacman:
            best_move = None
            best_value = float('-inf')
            for neighbor in self.graph.get_neighbors(self.current_node):
                self.set_position(neighbor)
                move_value = self.alpha_beta_search(3, float('-inf'), float('inf'), True, closest_pacman)
                self.set_position(self.current_node)

                if move_value > best_value:
                    best_value = move_value
                    best_move = neighbor

            self.set_position(best_move)
            return self.current_node

        return super().move()

    def find_closest_pacman(self, thieves_positions):
        min_distance = float('inf')
        closest_pacman = None
        for pos in thieves_positions:
            distance = self.calculate_distance(self.current_node, pos)
            if distance < min_distance:
                min_distance = distance
                closest_pacman = pos
        return closest_pacman

    def set_position(self, new_position):
        self.current_node = new_position

    def calculate_distance(self, start_node, target_node):
        queue = deque([(start_node, 0)])
        visited = set()
        visited.add(start_node)

        while queue:
            node, dist = queue.popleft()
            if node == target_node:
                return dist

            for neighbor in self.graph.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))

        return float('inf')

    def evaluate_position(self):
        score = 0
        thieves_positions = self.graph.get_neighbors(self.current_node)

        for thief in thieves_positions:
            distance = self.calculate_distance(self.current_node, thief)
            score -= distance

        return score
