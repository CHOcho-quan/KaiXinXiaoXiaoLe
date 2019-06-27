import numpy as np
import sys
import socket
import time
from agent.board import *
from agent.dqn import DQNAgent
from ImageProcessing.ImageProcessing import *

BUFSIZE = 100
# ip = '192.168.2.104'
ip = '10.162.45.126'
server_ip_port = ('10.162.220.210', 8899)
client_ip_port = (ip, 9000)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(server_ip_port)
print("Bind Success")

# time.sleep(10)
print("Begin")

camera = cv2.VideoCapture(0)
success, ori_img = camera.read()
# img, hsv, (top, bottom, left, right) = getPadLoc(ori_img)
# img, img2, hsv2, biasy, top2, bottom2, biasx, left2, right2 = getXXLLoc(img, hsv)
# animalVertical, animalHorizontal, singleLength = getRowColumnNum(img, img2, right2, left2, bottom2, top2)
#
# env = Board(animalVertical, animalHorizontal)
img1, hsv, (top, bottom, left, right) = getPadLoc(ori_img)
mode = 1
# state_size = animalVertical * animalHorizontal
# action_size = min(animalVertical, animalHorizontal)
# agent = DQNAgent(state_size, action_size)
# agent.load("./agent/save/dqn{0}{1}.h5".format(animalVertical, animalHorizontal))

while True:
    recv =  server.recvfrom(BUFSIZE)[0]
    if len(recv) <= 0:
        continue
    if mode == 1:
        img, img2, hsv2, biasy, top2, bottom2, biasx, left2, right2 = getXXLLoc(img1, hsv)
        animalVertical, animalHorizontal, singleLength = getRowColumnNum(img, img2, right2, left2, bottom2, top2)
        env = Board(animalVertical, animalHorizontal)
        state_size = animalVertical * animalHorizontal
        action_size = min(animalVertical, animalHorizontal)
        agent = DQNAgent(state_size, action_size)
        agent.load("./agent/save/dqn{0}{1}.h5".format(animalVertical, animalHorizontal))
    mode = 0

    # Quan Da's code
    success, ori_img = camera.read()

    if recv[0] == ord('&'):  # 初始化
        # writing your fucking code here

        init_x = left
        init_y = top
        up_x = left
        up_y = top
        down_x = left
        down_y = bottom
        data_lst = [init_x, init_y, up_x, up_y, down_x, down_y]
        s = ""
        for i in range(len(data_lst)):
            s += str(data_lst[i])
            s += '+'
        server.sendto(s.encode('utf-8'), client_ip_port)

        print("Sending init info Success")


    elif recv[0] == ord('^'):  # 处理图像
        img2 = ori_img[(biasy+top+top2):(biasy+top+bottom2), (biasx+left+left2):(biasx+left+right2)]
        mask2 = cv2.inRange(cv2.cvtColor(img2, cv2.COLOR_BGR2HSV), np.array([0, 0, 185]), np.array([180, 55, 255]))
        # cv2.imshow("mask2", mask2)
        # cv2.waitKey(0)
        if np.count_nonzero(mask2) / float(mask2.shape[0]*mask2.shape[1]) > 0.5:
            mode = 1
            print("WIN")
        # img2 = ori_img[top:bottom, left:right]
        # img2 = img2[top2:bottom2, left2:right2]
        # cv2.imshow('img2', img2)
        # cv2.waitKey(0)

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
        print(action_space[action], singleLength)

        x0, y0 = biasx+left+left2 + int((action_space[action][0][1]+0.5)*singleLength), biasy+top+top2 + int((action_space[action][0][0]+0.5)*singleLength)
        x1, y1 = biasx+left+left2 + int((action_space[action][1][1]+0.5)*singleLength), biasy+top+top2 + int((action_space[action][1][0]+0.5)*singleLength)
        cv2.imwrite("./i.png", cv2.circle(ori_img, (x0, y0), 5, (255, 0, 0), thickness=2))
        cv2.imwrite("./i2.png", cv2.circle(ori_img, (x1, y1), 5, (255, 0, 0), thickness=2))
        pixel_lst = [x0, y0, x1, y1, x1, y1]
        if mode==1:
            pixel_lst = [int(left+(right-left)/2), int(top+3/4*(bottom-top)), int(left+(right-left)/2), int(top+7.2/8*(bottom-top)), int(left+(right-left)/2), int(top+5/8*(bottom-top))]
        s = str(mode) + '+'
        for i in range(len(pixel_lst)):
            s += str(pixel_lst[i])
            s += '+'
        print(s)
        server.sendto(s.encode('utf-8'), client_ip_port)

        print("Sending Success")

print('Finished')
server.close()
