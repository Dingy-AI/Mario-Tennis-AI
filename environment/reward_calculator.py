from .interface import RewardFunction

class BasicReward(RewardFunction):

    def __init__(self):

        return None
    
    def calculate_reward(self, current_fitness: float, previous_fitness: float):
        return current_fitness - previous_fitness