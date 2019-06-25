from agent.board import *
from agent.dqn import DQNAgent
from ImageProcessing.ImageProcessing import *

if __name__=='__main__':
    camera = cv2.VideoCapture(0)
    success, ori_img = camera.read()
    img, hsv, (top, bottom, left, right) = getPadLoc(ori_img)
    img, img2, hsv2, biasy, top2, bottom2, biasx, left2, right2 = getXXLLoc(img, hsv)
    animalVertical, animalHorizontal, singleLength = getRowColumnNum(img, img2, right2, left2, bottom2, top2)

    env = Board(animalVertical, animalHorizontal)
    state_size = 49
    action_size = 7
    agent = DQNAgent(state_size, action_size)
    agent.load("./agent/save/dqn.h5")

    while (success):
        img2 = ori_img[(biasy+top+top2):(biasy+top+bottom2), (biasx+left+left2):(biasx+left+right2)]
        # img2 = ori_img[top:bottom, left:right]
        # img2 = img2[top2:bottom2, left2:right2]
        cv2.imshow('img2', img2)
        cv2.waitKey(0)

        # Now we construct the total animal matrix up to single animals
        animals = getAnimalMatrix(singleLength, animalVertical, animalHorizontal, img2)

        """
        0 : Blank, 1 : Fox, 2 : Chicken, 3 : Frog, 4 : Bear, 5 : Blueshit, 6 : Hawk, 7 : Phinex

        """
        print(animals)

        env.get_mat(animals)
        state = env.get_state()
        action = agent.act(state)
        action_space = env.get_action_space()
        print(state)
        print(action_space)
        action = action if action < len(action_space)-1 else len(action_space)-1
        print(action_space[action])

        success, ori_img = camera.read()
