# Adopted from https://github.com/NicoleFaye/PyBoy/blob/rl-test/PokemonPinballEnv.py
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from pyboy import PyBoy


actions = ['','a', 'b', 'left', 'right', 'up', 'down']
true_actions = ['','a', 'b', 'left', 'right', 'up', 'down', 'start', 'select']



matrix_shape = (16, 20)
game_area_observation_space = spaces.Box(low=0, high=255, shape=matrix_shape, dtype=np.uint8)

from .reward_calculator import BasicReward

class SuperMarioPyBoyEnvironment(gym.Env):

    def __init__(self, rom_path, debug=False):
        super().__init__()
        self.pyboy = PyBoy(rom_path)
        self._reward=0
        self._previous_reward=0
        self.debug = debug

        if not self.debug:
            self.pyboy.set_emulation_speed(0)

        self.action_space = spaces.Discrete(len(actions))
        self.observation_space = game_area_observation_space

        self.pyboy.game_wrapper.start_game()
        
        self.menu_navigation()
        self.set_initial_reward_position()
        # while self.pyboy.tick():
        #     print(self.pyboy.memory[0xC1C1])

        #     pass

        # self.pyboy.stop()

    def menu_navigation(self):
        for _ in range(60):
            self.pyboy.button(actions[1])
            self.pyboy.tick(10)
    
    def set_initial_reward_position(self):
        self._previous_position =  self.pyboy.memory[0xC1CA]

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))

        # Move the agent
        if action == 0:
            pass
        else:
            self.pyboy.button(actions[action])

        # Consider disabling renderer when not needed to improve speed:
        # self.pyboy.tick(1, False)
        self.pyboy.tick(1)


        # do a reset of the game if mario dies :O
        done = self.is_mario_dead()

        observation=self.pyboy.game_area()

        reward = self.calculate_reward()
        info = {}
        truncated = False

        # print("reward checker", reward, self.pyboy.memory[0xC1CA], self._previous_position, self.pyboy.memory[0xC1C1], self.pyboy.memory[0xFF99], self.pyboy.memory[0xFFA9], self.pyboy.memory[0xDE61])
        return observation, reward, done, truncated, info

    def is_mario_dead(self):
        if self.pyboy.memory[0xC1C1] == 3:
            return True
        return False

    # Basic reward function to prevent dying 
    def calculate_reward(self):
        # print("Current Menu Selection", self.pyboy.memory[0xC1A8])
        # print("Player State", self.pyboy.memory[0xC1C1])

        # print("Player X Position", self.pyboy.memory[0xC1CA])
        # print("Sprite Slot", self.pyboy.memory[0xD00F])

        # the main way to calculate score is to go to the right

        # we want to avoid enemies #if we hit an enemy or die we get a negative score

        # self._previous_position=self._current_position

        # NOTE: Only some game wrappers will provide a score
        # If not, you'll have to investigate how to score the game yourself

        # come back to this tomorrow - modify reward function to 
         
        if self.is_mario_dead(): # Player is dead
            self._reward = -10
            # input()
            return self._reward
        self._reward = self.pyboy.memory[0xC1CA] - self._previous_position

        self._previous_position = self.pyboy.memory[0xC1CA]

        # some weird thing happens when he hits the gomba. it resets his x and y position.
        # this might not be necessary but we will leave in for now. might just take it out later.
        if self._reward < -100: 
            self._reward = -10

        return self._reward

    def reset(self, **kwargs):
        self.pyboy.game_wrapper.reset_game()
        self._reward=0
        self._previous_reward=0

        observation=self.pyboy.game_area()
        self.menu_navigation()
        info = {}
        return observation, info

    def render(self, mode='human'):
        pass

    def close(self):
        self.pyboy.stop()