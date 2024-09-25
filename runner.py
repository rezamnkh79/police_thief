import json
import logging
import random

from graph import Graph
from police import Police
from thief import Thief

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class Runner:
    def __init__(self, config_file_name: str = "config.json"):
        self.config_file_name = config_file_name
        self.num_thieves = None
        self.num_polices = None
        self.number_of_rounds = None
        self.reveal_rounds = None
        self.graph = Graph()
        self.vertices = []
        self.edges = []

        self.polices = []
        self.thieves = []

    def read_config(self):
        with open(self.config_file_name, "r") as f:
            try:
                config_file = json.load(f)
                map_graph = config_file["map"]
                self.vertices = map_graph["vertices"]
                self.edges = map_graph["edges"]
                self.create_graph()

                self.number_of_rounds = config_file["number_of_rounds"]
                self.reveal_rounds = config_file["reveal_rounds"]
                self.num_polices = config_file["polices"]
                self.num_thieves = config_file["thieves"]
            except Exception as e:
                logger.error("Exception in reading config file!", e, exc_info=True)

    def create_graph(self):
        self.graph = Graph()
        self.graph.add_nodes(self.vertices)
        self.graph.add_edges(self.edges)
        self.graph.display_graph()

    def init_game(self):
        if self.num_thieves < 0 or self.num_polices < 0:
            raise ValueError("Number of thieves and polices cannot be negative!")
        if self.num_thieves + self.num_polices >= len(self.vertices):
            raise ValueError("Number of thieves and polices should be less than the number of vertices!")

        police_vertices = []
        for i in range(self.num_polices):
            police_init_position = random.choice(self.vertices)
            police = Police(i, self.graph, police_init_position)
            self.polices.append(police)
            logger.info(f"Police {police.agent_id} initialized at vertex {police_init_position}")
            police_vertices.append(police_init_position)

        thieves_possible_init_positions = [v for v in self.vertices if v not in police_vertices]
        for i in range(self.num_thieves):
            thief_init_position = random.choice(thieves_possible_init_positions)
            thief = Thief(i, self.graph, thief_init_position)
            self.thieves.append(thief)
            logger.info(f"Thief {thief.agent_id} initialized at vertex {thief_init_position}")

    def run(self, draw_map_each_round = False):
        self.init_game()
        if draw_map_each_round:
            self.draw_map()

        for round_number in range(self.number_of_rounds):
            self.run_round(round_number)
            self.check_thieves_and_police_collision()

            if draw_map_each_round:
                self.draw_map()

            if len(self.thieves) == 0:
                logger.info("Counter Terrorists win the game 🥳")
                return

        logger.info("Terrorists win the game 🫢")

    def run_round(self, round_number):
        current_police_positions = {police.agent_id: police.current_node for police in self.polices}
        current_thief_positions = {thief.agent_id: thief.current_node for thief in self.thieves}

        is_reveal_round = round_number in self.reveal_rounds
        for police in self.polices:
            if is_reveal_round:
                police.move(
                    {
                        "polices": list(current_police_positions.values()),
                        "thieves": list(current_thief_positions.values())
                    }
                )
            else:
                police.move(
                    {
                        "polices": list(current_police_positions.values()),
                        "thieves": []
                    }
                )
            logger.info(f"Police {police.agent_id} has made this move: "
                        f"{current_police_positions[police.agent_id]} -> {police.current_node}")

        for thief in self.thieves:
            thief.move(
                {
                    "polices": list(current_police_positions.values()),
                    "thieves": list(current_thief_positions.values())
                }
            )
            logger.info(f"Thief {thief.agent_id} has made this move: "
                        f"{current_thief_positions[thief.agent_id]} -> {thief.current_node}")

    def check_thieves_and_police_collision(self):
        current_police_positions = [police.current_node for police in self.polices]

        for thief in self.thieves:
            if thief.current_node in current_police_positions:
                self.thieves.remove(thief)
                logger.info(f"Thief {thief.agent_id} has caught!")

    def draw_map(self):
        color_map = ["gray" for _ in range(len(self.vertices))]
        for thief in self.thieves:
            color_map[self.vertices.index(thief.current_node)] = "red"
        for police in self.polices:
            color_map[self.vertices.index(police.current_node)] = "green"

        self.graph.display_graph(color_map)

# Example Usage
if __name__ == "__main__":
    runner = Runner()
    runner.read_config()
    runner.run(draw_map_each_round = False)
