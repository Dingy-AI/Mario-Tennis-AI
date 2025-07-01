
from environment import SuperMarioPyBoyEnvironment
import time
def create_env():
    
    env = SuperMarioPyBoyEnvironment("smbd.gbc")

    return env

def main():
    print("Hello world")
    env = create_env()

    for i in range(0,1000):

        print(env.step(4))
    print("temp")



if __name__ == "__main__":
    main()