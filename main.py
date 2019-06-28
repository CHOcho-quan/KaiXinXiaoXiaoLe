from agent.board import *
from agent.dqn import DQNAgent
from ImageProcessing.ImageProcessing import *

if __name__=='__main__':
    camera = cv2.VideoCapture(0)
    success, ori_img = camera.read()
    print(ori_img.shape)
    img, hsv, (top, bottom, left, right) = getPadLoc(ori_img)
    img, img2, hsv2, biasy, top2, bottom2, biasx, left2, right2 = getXXLLoc(img, hsv)
    animalVertical, animalHorizontal, singleLength = getRowColumnNum(img, img2, right2, left2, bottom2, top2)
    print(int(left+(right-left)/2), int(top+3/4*(bottom-top)))
    # cv2.imshow("hello", cv2.circle(img=ori_img, center=(int(left+(right-left)/2), int(top+3/4*(bottom-top))), radius=5, color=(0, 0, 255)))
    # cv2.waitKey(0)

    env = Board(animalVertical, animalHorizontal)
    env.show()
    state_size = 32
    action_size = 4
    agent = DQNAgent(state_size, action_size)
    agent.load("./agent/save/dqn84.h5")

    while (success):
        img2 = ori_img[(biasy+top+top2):(biasy+top+bottom2), (biasx+left+left2):(biasx+left+right2)]
        mask2 = cv2.inRange(cv2.cvtColor(img2, cv2.COLOR_BGR2HSV), np.array([0, 0, 185]), np.array([180, 55, 255]))
        # cv2.imshow("mask2", mask2)
        # cv2.waitKey(0)
        if np.count_nonzero(mask2) / float(mask2.shape[0]*mask2.shape[1]) > 0.5:
            print("WIN")
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

        x0, y0 = biasx+left+left2 + int((action_space[action][0][1]+0.5)*singleLength), biasy+top+top2 + int((action_space[action][0][0]+0.5)*singleLength)
        x1, y1 = biasx+left+left2 + int((action_space[action][1][1]+0.5)*singleLength), biasy+top+top2 + int((action_space[action][1][0]+0.5)*singleLength)
        cv2.imwrite("./i.png", cv2.circle(ori_img, (x0, y0), 5, (255, 0, 0), thickness=2))
        cv2.imwrite("./i2.png", cv2.circle(ori_img, (x1, y1), 5, (255, 0, 0), thickness=2))

        success, ori_img = camera.read()
