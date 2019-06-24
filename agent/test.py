from board import *
from dqn import DQNAgent

if __name__ == "__main__":
    env = Board(7, 7)
    state_size = 49
    action_size = 7
    agent = DQNAgent(state_size, action_size)
    agent.load("./save/dqn.h5")
    mat_test = [[1, 2, 3, 4, 5, 3, 2], [2, 3, 1, 4, 5, 1, 4], [2, 3, 1, 5, 4, 4, 1], [2, 2, 4, 5, 1, 1, 2], [4, 3, 4, 2, 1, 3, 5], [1, 3, 4, 5, 1, 2, 3],[4, 5, 1, 2, 3, 4, 5]]
    env.get_mat(mat_test)
    state = env.get_state()
    action = agent.act(state)
    action_space = env.get_action_space()
    print(state)
    print(action_space)
    action = action if action < len(action_space)-1 else len(action_space)-1
    print(action_space[action])
