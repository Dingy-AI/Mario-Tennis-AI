from abc import ABC, abstractmethod


class RewardFunction(ABC):

    @abstractmethod
    def calculate_reward(self, current_fitness: float, previous_fitness: float, **kwargs):
        
        pass