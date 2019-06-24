# 消消乐DQN

用法在test.py里面。

7*7的网格

每次获取到动物矩阵后，调用env.get_mat() 将看到的矩阵送进去

env.get_state() 获取当前的state 向量，这是通过卷积网络得到的结果

agent.act()得到当前网络认为的最优move

env.get_action_space() 可以获得当前能走的所有位置

由于训练不充分，导致得到的有些action 超过了action space 的index，因此要截断一下

最后获得的最优走法是 action_space[action]