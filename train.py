
from environment import SuperMarioPyBoyEnvironment
import time
def create_env():
    
    env = SuperMarioPyBoyEnvironment("smbd.gbc")

    return env

def main():
    print("Hello world")
    env = create_env()

    for i in range(0,1000):

        observation, reward, done, truncated, info = env.step(4)

        if done:
            env.reset()
    print("temp")



if __name__ == "__main__":
    main()