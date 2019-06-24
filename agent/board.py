import numpy as np

class Board:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.animal_mat = []
        for i in range(self.height):
            tmp = []
            for j in range(self.width):
                tmp.append(0)
            self.animal_mat.append(tmp)
        self.spe_mat = []
        for i in range(self.height):
            tmp = []
            for j in range(self.width):
                tmp.append(0)
            self.spe_mat.append(tmp)

        self.score = 0
        self.action_space = []
        self.animal_num = [0]*7
        self.last_act_space = []
        self.same_cnt = 0

    def show(self):
        for i in range(self.height):
            print(self.animal_mat[i])

    def get_mat(self, mat):
        for i in range(self.height):
            for j in range(self.width):
                self.animal_mat[i][j] = mat[i][j]

    @staticmethod
    def pos_can_exchange(p1, p2):
        dy = abs(p1[0] - p2[0])
        dx = abs(p1[1] - p2[1])
        if dy + dx != 1:
            return False
        else:
            return True

    def item_can_exchange(self, p1, p2):
        if self.animal_mat[p1[0]][p1[1]] == 0:
            return False
        if self.animal_mat[p2[0]][p2[1]] == 0:
            return False
        return True

    def can_exchange(self, p1, p2):
        if self.pos_can_exchange(p1,p2) and self.item_can_exchange(p1,p2):
            return True
        else:
            return False

    def have_cancle_env(self):
        # 给环境用的判断更新完是否能继续消除，因此不含两个特殊交换，凤凰交换
        # 普通三及以上消
        for i in range(self.height):
            for j in range(2, self.width):
                if self.animal_mat[i][j - 2] == self.animal_mat[i][j - 1] == self.animal_mat[i][j] and \
                        self.animal_mat[i][j] != 0:
                    return True
        for i in range(self.width):
            for j in range(2, self.height):
                if self.animal_mat[j-2][i] == self.animal_mat[j-1][i] == self.animal_mat[j][i] and \
                 self.animal_mat[j][i] != 0:
                    return True


    def have_cancle(self):
        # 看行
        # 普通三及以上消
        for i in range(self.height):
            for j in range(2,self.width):
                if self.animal_mat[i][j-2] == self.animal_mat[i][j-1] == self.animal_mat[i][j] and \
                 self.animal_mat[i][j] != 0:
                    return True
        # 两个挨着的特效
        for i in range(self.height):
            for j in range(1,self.width):
                if self.spe_mat[i][j-1] != 0 and self.spe_mat[i][j] != 0 and \
                 self.spe_mat[i][j-1] != 4 and self.spe_mat[i][j] != 4:
                    return True

        # 看列
        # 普通三消及以上
        for i in range(self.width):
            for j in range(2, self.height):
                if self.animal_mat[j-2][i] == self.animal_mat[j-1][i] == self.animal_mat[j][i] and \
                 self.animal_mat[j][i] != 0:
                    return True
        # 两个挨着的特效
        for i in range(self.width):
            for j in range(self.height):
                if self.spe_mat[j-1][i] != 0 and self.spe_mat[j][i] != 0 and \
                 self.spe_mat[j-1][i] != 4 and self.spe_mat[j][i] != 4:
                    return True

        #凤凰
        for i in range(self.height):
            for j in range(self.width):
                if self.animal_mat[i][j] == 7:
                    return True

    def find_empty(self):
        empty_list = []
        for i in range(self.height-1,-1,-1):
            for j in range(self.width-1,-1,-1):
                if self.animal_mat[i][j] == -1:
                    empty_list.append((i,j))
        return empty_list

    def find_first_up_ani(self,i,j):
        for m in range(i-1,-1,-1):
            if self.animal_mat[m][j] in range(1,8):
                return m,j
        return -1,-1


    def drop(self):
        # 已经消除的块，有空隙，上方下落，随机生成新的动物。
        empty_list = self.find_empty()
        for empty_block in empty_list:
            fua = self.find_first_up_ani(empty_block[0],empty_block[1])
            if fua[0] == -1:
                self.animal_mat[empty_block[0]][empty_block[1]] = np.random.randint(1,6)
                self.spe_mat[empty_block[0]][empty_block[1]] = 0
            else:
                self.animal_mat[empty_block[0]][empty_block[1]] = self.animal_mat[fua[0]][fua[1]]
                self.spe_mat[empty_block[0]][empty_block[1]] = self.spe_mat[fua[0]][fua[1]]
                self.animal_mat[fua[0]][fua[1]] = -1
                self.spe_mat[fua[0]][fua[1]] = 0
                empty_list.append(fua)


    def get_boom_range(self,h,w):
        down_limit = 2
        up_limit_height = self.height - 2
        up_limit_width = self.width - 2
        if h < down_limit and w < down_limit:
            return range(0,h+3), range(0,w+3)
        if h < down_limit and down_limit <= w <= up_limit_width:
            return range(0,h+3), range(w-2,w+3)
        if h < down_limit and w > up_limit_width:
            return range(0,h+3), range(w-2,self.width)
        if down_limit<=h<=up_limit_height and w < down_limit:
            return range(h-2,h+3), range(0,w+3)
        if down_limit<=h<=up_limit_height and down_limit<=w<=up_limit_width:
            return range(h-2,h+3), range(w-2,w+3)
        if down_limit<=h<=up_limit_height and w > up_limit_width:
            return range(h-2,h+3), range(w-2,self.width)
        if h > up_limit_height and w < down_limit:
            return range(h-2,self.height), range(0, w+3)
        if h > up_limit_height and down_limit<=w<=up_limit_width:
            return range(h-2,self.height), range(w-2,w+3)
        if h > up_limit_height and w > up_limit_width:
            return range(h-2,self.height), range(w-2, self.width)

    def patten_T_up(self,h,w):
        if self.animal_mat[h-2][w] == self.animal_mat[h-1][w] == self.animal_mat[h][w]:
            if self.animal_mat[h][w-1] == self.animal_mat[h][w] == self.animal_mat[h][w+1]:
                return True
        return False

    def patten_T_down(self,h,w):
        if self.animal_mat[h][w] == self.animal_mat[h+1][w] == self.animal_mat[h+2][w]:
            if self.animal_mat[h][w-1] == self.animal_mat[h][w] == self.animal_mat[h][w+1]:
                return True
        return False

    def patten_T_left(self,h,w):
        if self.animal_mat[h][w-2] == self.animal_mat[h][w-1] == self.animal_mat[h][w]:
            if self.animal_mat[h-1][w] == self.animal_mat[h][w] == self.animal_mat[h+1][w]:
                return True
        return False

    def patten_T_right(self,h,w):
        if self.animal_mat[h][w] == self.animal_mat[h][w+1] == self.animal_mat[h][w+2]:
            if self.animal_mat[h-1][w] == self.animal_mat[h][w] == self.animal_mat[h+1][w]:
                return True
        return False

    def patten_L_ul(self,h,w):
        if self.animal_mat[h-1][w-1] == self.animal_mat[h-1][w] == self.animal_mat[h-1][w+1]:
            if self.animal_mat[h-1][w-1] == self.animal_mat[h][w-1] == self.animal_mat[h+1][w-1]:
                return True
        return False

    def patten_L_ur(self,h,w):
        if self.animal_mat[h-1][w-1] == self.animal_mat[h-1][w] == self.animal_mat[h-1][w+1]:
            if self.animal_mat[h-1][w+1] == self.animal_mat[h][w+1] == self.animal_mat[h+1][w+1]:
                return True
        return False

    def patten_L_bl(self,h,w):
        if self.animal_mat[h+1][w-1] == self.animal_mat[h][w-1] == self.animal_mat[h-1][w-1]:
            if self.animal_mat[h+1][w-1] == self.animal_mat[h+1][w] == self.animal_mat[h+1][w+1]:
                return True
        return False

    def patten_L_br(self,h,w):
        if self.animal_mat[h+1][w+1] == self.animal_mat[h+1][w] == self.animal_mat[h+1][w-1]:
            if self.animal_mat[h+1][w+1] == self.animal_mat[h][w+1] == self.animal_mat[h-1][w+1]:
                return True
        return False

    def update(self):
        # 更新两个矩阵，获得reward.若新的还能消，则继续更新，直到新的没有能消的。

        #横5
        for i in range(self.height):
            j = 4
            while j < self.width:

                if self.animal_mat[i][j-4] == self.animal_mat[i][j-3] == self.animal_mat[i][j-2] == self.animal_mat[i][j-1] == self.animal_mat[i][j]:
                    # 5个普通的
                    if self.spe_mat[i][j-4] == self.spe_mat[i][j-3] == self.spe_mat[i][j-2] == self.spe_mat[i][j-1] == self.spe_mat[i][j] == 0:
                        phoenix = np.random.randint(0,5)+j-4
                        self.animal_mat[i][phoenix] = 7
                        for k in range(j-4,j+1):
                            if k != phoenix:
                                self.animal_mat[i][k] = -1
                        self.score += 5 * 3
                        break
                    # 里面有横消特效
                    for k in range(j-4,j+1):
                        if self.spe_mat[i][k] == 1:
                            phoenix = np.random.randint(0, 5) + j - 4
                            self.animal_mat[i][phoenix] = 7
                            row_ani_cnt = 0
                            for m in range(0, self.width):
                                if m != phoenix and self.animal_mat[i][m] != 0: # 清空一行，考虑生成的凤凰和本来没动物的死块
                                    self.animal_mat[i][m] = -1
                                    row_ani_cnt += 1
                            self.score += row_ani_cnt * 2
                            break
                    # 里面有纵消特效
                    for k in range(j-4,j+1):
                        if self.spe_mat[i][k] == 2:
                            self.animal_mat[i][k] = -1
                            phoenix = np.random.randint(0, 5) + j - 4
                            self.animal_mat[i][phoenix] = 7
                            col_ani_cnt = 0
                            for m in range(0,self.height):
                                if self.animal_mat[m][k] != 0 and m != k:
                                    self.animal_mat[m][k] = -1
                                    col_ani_cnt += 1
                            self.score += (5 + col_ani_cnt) * 2
                            break
                    # 里面有爆炸特效
                    for k in range(j-4,j+1):
                        if self.spe_mat[i][k] == 3:
                            self.animal_mat[i][k] = -1
                            phoenix = np.random.randint(0, 5) + j - 4
                            self.animal_mat[i][phoenix] = 7
                            boom_ani_cnt = 0
                            boom_range = self.get_boom_range(i,k)
                            for m in boom_range[0]:
                                for n in boom_range[1]:
                                    self.animal_mat[m][n] = -1
                                    boom_ani_cnt += 1
                            self.score += (5 + boom_ani_cnt) * 2.5
                            break
                j += 1

        #横4
        for i in range(self.height):
            j = 3
            while j < self.width:

                if self.animal_mat[i][j-3] == self.animal_mat[i][j-2] == self.animal_mat[i][j-1] == self.animal_mat[i][j]:
                    # 4个普通的
                    if self.spe_mat[i][j-3] == self.spe_mat[i][j-2] == self.spe_mat[i][j-1] == self.spe_mat[i][j] == 0:
                        spe = np.random.randint(0,4)+j-3
                        self.spe_mat[i][spe] = 1
                        self.animal_mat[i][spe] = self.animal_mat[i][j]
                        for k in range(j-3,j+1):
                            if k != spe:
                                self.animal_mat[i][k] = -1
                        self.score += 4 * 3
                        break
                    # 里面有横消特效
                    for k in range(j-3,j+1):
                        if self.spe_mat[i][k] == 1:
                            spe = np.random.randint(0, 4) + j - 3
                            self.animal_mat[i][spe] = self.animal_mat[i][j]
                            self.spe_mat[i][spe] = 1
                            row_ani_cnt = 0
                            for m in range(0, self.width):
                                if m != spe and self.animal_mat[i][m] != 0: # 清空一行，考虑生成的横消特效和本来没动物的死块
                                    self.animal_mat[i][m] = -1
                                    row_ani_cnt += 1
                            self.score += row_ani_cnt * 2
                            break
                    # 里面有纵消特效
                    for k in range(j-3,j+1):
                        if self.spe_mat[i][k] == 2:
                            self.animal_mat[i][k] = -1
                            spe = np.random.randint(0, 4) + j - 3
                            self.animal_mat[i][spe] = self.animal_mat[i][k]
                            self.spe_mat[i][spe] = 1
                            col_ani_cnt = 0
                            for m in range(0,self.height):
                                if self.animal_mat[m][k] != 0 and m != k:
                                    self.animal_mat[m][k] = -1
                                    col_ani_cnt += 1
                            self.score += (4 + col_ani_cnt) * 2
                            break
                    # 里面有爆炸特效
                    for k in range(j-3,j+1):
                        if self.spe_mat[i][k] == 3:
                            self.animal_mat[i][k] = -1
                            spe = np.random.randint(0, 4) + j - 3
                            self.animal_mat[i][spe] = self.animal_mat[i][k]
                            self.spe_mat[i][spe] = 1
                            boom_ani_cnt = 0
                            boom_range = self.get_boom_range(i,k)
                            for m in boom_range[0]:
                                for n in boom_range[1]:
                                    self.animal_mat[m][n] = -1
                                    boom_ani_cnt += 1
                            self.score += (4 + boom_ani_cnt) * 2.5
                            break
                j += 1
        #横3
        for i in range(self.height):
            j = 2
            while j < self.width:

                if self.animal_mat[i][j-2] == self.animal_mat[i][j-1] == self.animal_mat[i][j]:
                    # 3个普通的
                    if self.spe_mat[i][j-2] == self.spe_mat[i][j-1] == self.spe_mat[i][j] == 0:
                        for k in range(j-2,j+1):
                            self.animal_mat[i][k] = -1
                        self.score += 3
                        break
                    # 里面有横消特效
                    for k in range(j-2,j+1):
                        if self.spe_mat[i][k] == 1:
                            row_ani_cnt = 0
                            for m in range(0, self.width):
                                if self.animal_mat[i][m] != 0: # 清空一行，考虑生成的横消特效和本来没动物的死块
                                    self.animal_mat[i][m] = -1
                                    row_ani_cnt += 1
                            self.score += row_ani_cnt * 2
                            break
                    # 里面有纵消特效
                    for k in range(j-2,j+1):
                        if self.spe_mat[i][k] == 2:
                            self.animal_mat[i][k] = -1
                            col_ani_cnt = 0
                            for m in range(0,self.height):
                                if self.animal_mat[m][k] != 0 and m != k:
                                    self.animal_mat[m][k] = -1
                                    col_ani_cnt += 1
                            self.score += (3 + col_ani_cnt) * 2
                            break
                    # 里面有爆炸特效
                    for k in range(j-2,j+1):
                        if self.spe_mat[i][k] == 3:
                            self.animal_mat[i][k] = -1
                            boom_ani_cnt = 0
                            boom_range = self.get_boom_range(i,k)
                            for m in boom_range[0]:
                                for n in boom_range[1]:
                                    self.animal_mat[m][n] = -1
                                    boom_ani_cnt += 1
                            self.score += boom_ani_cnt * 2.5
                            break
                j += 1
        #纵五
        for i in range(self.width):
            j = 4
            while j < self.height:

                if self.animal_mat[j-4][i] == self.animal_mat[j-3][i] == self.animal_mat[j-2][i] == self.animal_mat[j-1][i] == self.animal_mat[j][i]:
                    # 5个普通的
                    if self.spe_mat[j-4][i] == self.spe_mat[j-3][i] == self.spe_mat[j-2][i] == self.spe_mat[j-1][i] == self.spe_mat[j][i] == 0:
                        phoenix = np.random.randint(0,5)+j-4
                        self.animal_mat[phoenix][i] = 7
                        for k in range(j-4,j+1):
                            if k != phoenix:
                                self.animal_mat[k][i] = -1
                        self.score += 5 * 3
                        break
                    # 里面有横消特效
                    for k in range(j-4,j+1):
                        if self.spe_mat[k][i] == 1:
                            phoenix = np.random.randint(0, 5) + j - 4
                            self.animal_mat[phoenix][i] = 7
                            row_ani_cnt = 0
                            for m in range(0, self.width):
                                if k!=phoenix and self.animal_mat[k][m] != 0: # 清空一行，考虑生成的凤凰和本来没动物的死块
                                    self.animal_mat[k][m] = -1
                                    row_ani_cnt += 1
                            self.score += row_ani_cnt * 2
                            break
                    # 里面有纵消特效
                    for k in range(j-4,j+1):
                        if self.spe_mat[k][i] == 2:
                            self.animal_mat[k][i] = -1
                            phoenix = np.random.randint(0, 5) + j - 4
                            self.animal_mat[phoenix][i] = 7
                            col_ani_cnt = 0
                            for m in range(0,self.height):
                                if self.animal_mat[m][i] != 0 and m != phoenix:
                                    self.animal_mat[m][i] = -1
                                    col_ani_cnt += 1
                            self.score += (5 + col_ani_cnt) * 2
                            break
                    # 里面有爆炸特效
                    for k in range(j-4,j+1):
                        if self.spe_mat[k][i] == 3:
                            self.animal_mat[k][i] = -1
                            phoenix = np.random.randint(0, 5) + j - 4
                            self.animal_mat[phoenix][i] = 7
                            boom_ani_cnt = 0
                            boom_range = self.get_boom_range(k,i)
                            for m in boom_range[0]:
                                for n in boom_range[1]:
                                    self.animal_mat[m][n] = -1
                                    boom_ani_cnt += 1
                            self.score += (5 + boom_ani_cnt) * 2.5
                            break
                j += 1
        #纵四
        for i in range(self.width):
            j = 3
            while j < self.height:

                if self.animal_mat[j-3][i] == self.animal_mat[j-2][i] == self.animal_mat[j-1][i] == self.animal_mat[j][i]:
                    # 4个普通的
                    if self.spe_mat[j-3][i] == self.spe_mat[j-2][i] == self.spe_mat[j-1][i] == self.spe_mat[j][i] == 0:
                        spe = np.random.randint(0,4)+j-3
                        self.animal_mat[spe][i] = self.animal_mat[j][i]
                        self.spe_mat[spe][i] = 2
                        for k in range(j-3,j+1):
                            if k != spe:
                                self.animal_mat[k][i] = -1
                        self.score += 4 * 3
                        break
                    # 里面有横消特效
                    for k in range(j-3,j+1):
                        if self.spe_mat[k][i] == 1:
                            spe = np.random.randint(0, 4) + j - 3
                            self.animal_mat[spe][i] = self.animal_mat[j][i]
                            self.spe_mat[spe][i] = 2
                            row_ani_cnt = 0
                            for m in range(0, self.width):
                                if k!=spe and self.animal_mat[k][m] != 0: # 清空一行，考虑生成的特殊和本来没动物的死块
                                    self.animal_mat[k][m] = -1
                                    row_ani_cnt += 1
                            self.score += row_ani_cnt * 2
                            break
                    # 里面有纵消特效
                    for k in range(j-3,j+1):
                        if self.spe_mat[k][i] == 2:
                            self.animal_mat[k][i] = -1
                            spe = np.random.randint(0, 4) + j - 3
                            self.animal_mat[spe][i] = self.animal_mat[j][i]
                            self.spe_mat[spe][i] = 2
                            col_ani_cnt = 0
                            for m in range(0,self.height):
                                if self.animal_mat[m][i] != 0 and m != spe:
                                    self.animal_mat[m][i] = -1
                                    col_ani_cnt += 1
                            self.score += (4 + col_ani_cnt) * 2
                            break
                    # 里面有爆炸特效
                    for k in range(j-3,j+1):
                        if self.spe_mat[k][i] == 3:
                            self.animal_mat[k][i] = -1
                            spe = np.random.randint(0, 4) + j - 3
                            self.animal_mat[spe][i] = self.animal_mat[j][i]
                            self.spe_mat[spe][i] = 2
                            boom_ani_cnt = 0
                            boom_range = self.get_boom_range(k,i)
                            for m in boom_range[0]:
                                for n in boom_range[1]:
                                    self.animal_mat[m][n] = -1
                                    boom_ani_cnt += 1
                            self.score += boom_ani_cnt * 2.5
                            break
                j += 1
        #纵三
        for i in range(self.width):
            j = 2
            while j < self.height:

                if self.animal_mat[j-2][i] == self.animal_mat[j-1][i] == self.animal_mat[j][i]:
                    # 3个普通的
                    if self.spe_mat[j-2][i] == self.spe_mat[j-1][i] == self.spe_mat[j][i] == 0:
                        for k in range(j-2,j+1):
                            self.animal_mat[k][i] = -1
                        self.score += 3
                        break
                    # 里面有横消特效
                    for k in range(j-2,j+1):
                        if self.spe_mat[k][i] == 1:
                            row_ani_cnt = 0
                            for m in range(0, self.width):
                                if self.animal_mat[k][m] != 0: # 清空一行，考虑生成的特殊和本来没动物的死块
                                    self.animal_mat[k][m] = -1
                                    row_ani_cnt += 1
                            self.score += row_ani_cnt * 2
                            break
                    # 里面有纵消特效
                    for k in range(j-2,j+1):
                        if self.spe_mat[k][i] == 2:
                            col_ani_cnt = 0
                            for m in range(0,self.height):
                                if self.animal_mat[m][i] != 0 :
                                    self.animal_mat[m][i] = -1
                                    col_ani_cnt += 1
                            self.score += (3 + col_ani_cnt) * 2
                            break
                    # 里面有爆炸特效
                    for k in range(j-3,j+1):
                        if self.spe_mat[k][i] == 3:
                            boom_ani_cnt = 0
                            boom_range = self.get_boom_range(k,i)
                            for m in boom_range[0]:
                                for n in boom_range[1]:
                                    self.animal_mat[m][n] = -1
                                    boom_ani_cnt += 1
                            self.score += boom_ani_cnt * 2.5
                            break
                j += 1
        #丁字（上下左右）
        #上丁
        for i in range(2,self.height):
            for j in range(1,self.width-1):
                if self.patten_T_up(i,j):
                    # 消掉上丁里的元素，并且在i,j处生成一个爆炸特效。
                    for m in range(i-2,i+1):
                        if m != i:
                            self.animal_mat[m][j] = -1
                    for n in range(j-1,j+2):
                        if n!=j:
                            self.animal_mat[i][n] = -1
                    self.spe_mat[i][j] = 3
                    self.score += 2.5 * 5
        #下丁
        for i in range(self.height-2):
            for j in range(1,self.width-1):
                if self.patten_T_down(i,j):
                    for m in range(i+1,i+3):
                        self.animal_mat[m][j] = -1
                    for n in range(j-1,j+2):
                        if n != j:
                            self.animal_mat[i][n] = -1
                    self.spe_mat[i][j] = 3
                    self.score += 2.5*5
        #左丁
        for i in range(1,self.height-1):
            for j in range(2,self.width):
                if self.patten_T_left(i,j):
                    for m in range(i-1,i+2):
                        if m!=i:
                            self.animal_mat[m][j] = -1
                    for n in range(j-2,j):
                        self.animal_mat[i][n] = -1
                    self.spe_mat[i][j] = 3
                    self.score += 2.5*5
        #右丁
        for i in range(1,self.height-1):
            for j in range(self.width-2):
                if self.patten_T_right(i,j):
                    for m in range(i-1,i+2):
                        if m!=i:
                            self.animal_mat[m][j] = -1
                    for n in range(j+1,j+3):
                        self.animal_mat[i][n] = -1
                    self.spe_mat[i][j] = 3
                    self.score += 2.5*5

        #勾（左上，右上，左下，右下）

        for i in range(1,self.height-1):
            for j in range(1,self.width-1):
                if self.patten_L_ul(i,j):
                    rem = self.animal_mat[i-1][j-1]
                    for m in range(i-1,i+2):
                        self.animal_mat[m][j-1] = -1
                    for n in range(j-1,j+2):
                        self.animal_mat[i-1][n] = -1
                    self.animal_mat[i-1][j-1] = rem
                    self.spe_mat[i-1][j-1] = 3
                    self.score += 5*2.5

                if self.patten_L_ur(i,j):
                    rem = self.animal_mat[i-1][j+1]
                    for m in range(i-1,i+2):
                        self.animal_mat[m][j+1] = -1
                    for n in range(j-1,j+2):
                        self.animal_mat[i-1][n] = -1
                    self.animal_mat[i-1][j+1] = rem
                    self.spe_mat[i-1][j+1] = 3
                    self.score += 5*2.5

                if self.patten_L_bl(i,j):
                    rem = self.animal_mat[i+1][j-1]
                    for m in range(i-1,i+2):
                        self.animal_mat[m][j-1] = -1
                    for n in range(j-1,j+2):
                        self.animal_mat[i+1][n] = -1
                    self.animal_mat[i+1][j-1] = rem
                    self.spe_mat[i+1][j-1] = 3
                    self.score += 2.5*5

                if self.patten_L_br(i,j):
                    rem = self.animal_mat[i+1][j+1]
                    for m in range(i-1,i+2):
                        self.animal_mat[m][j+1] = -1
                    for n in range(j-1,j+2):
                        self.animal_mat[i+1][n] = -1
                    self.animal_mat[i+1][j+1] = rem
                    self.spe_mat[i+1][j+1] = 3
                    self.score += 2.5*5

        self.drop()

        if self.have_cancle_env():
            self.update()



    def exchange(self, p1, p2):
        if not self.can_exchange(p1, p2):
            print("can not exchange")
            return
        self.animal_mat[p1[0]][p1[1]], self.animal_mat[p2[0]][p2[1]] = self.animal_mat[p2[0]][p2[1]], self.animal_mat[p1[0]][p1[1]]
        self.update()

    def get_action_space(self):
        action_space = []
        for i in range(self.height):
            for j in range(self.width):
                if self.animal_mat[i][j] != 0:
                    if j+1 < self.width and self.animal_mat[i][j] == self.animal_mat[i][j+1]:
                        if i-1 >= 0 and j-1 >= 0 and i+1<self.height:
                            if self.animal_mat[i][j] in [self.animal_mat[i-1][j-1], self.animal_mat[i+1][j-1]] \
                                and self.animal_mat[i][j-1] != 0:
                                action_space.append(((i - 1, j - 1), (i, j - 1)) if self.animal_mat[i][j] == self.animal_mat[i-1][j-1] else ((i+1,j-1),(i,j-1)))
                                break
                        if i-1>=0 and i+1<self.height and j+2<self.width:
                            if self.animal_mat[i][j] in [self.animal_mat[i-1][j+2], self.animal_mat[i+1][j+2]] \
                                and self.animal_mat[i][j+2] != 0:
                                # a     b
                                #   a a
                                # c     d
                                action_space.append(((i,j+2),(i-1,j+2)) if self.animal_mat[i][j] == self.animal_mat[i-1][j+2] else ((i,j+2),(i+1,j+2)))
                                break

                    elif i+1<self.height and j+1<self.width and self.animal_mat[i][j] == self.animal_mat[i+1][j]:
                        if i-1 >= 0 and j-1 >= 0:
                            if self.animal_mat[i][j] in [self.animal_mat[i-1][j-1],self.animal_mat[i-1][j+1]] \
                                and self.animal_mat[i-1][j] != 0:
                                action_space.append(
                                    ((i-1, j -1), (i -1, j)) if self.animal_mat[i][j] == self.animal_mat[i - 1][
                                        j -1] else ((i-1, j), (i-1, j + 1)))
                                break
                        if i+2<self.height and j-1 >= 0:
                            if self.animal_mat[i][j] in [self.animal_mat[i+2][j-1],self.animal_mat[i+2][j+1]] \
                                and self.animal_mat[i+2][j] != 0:
                                action_space.append(
                                    ((i+2, j-1), (i+2, j)) if self.animal_mat[i][j] == self.animal_mat[i+2][
                                        j -1] else ((i+2, j), (i+2, j + 1)))
                                break
                            # a b
                            #  a
                            #  a
                            # c d

                    else:
                        if i-1>=0 and j-1>=0 and i+1<self.height and j+1<self.width:
                            if self.animal_mat[i - 1][j - 1] == self.animal_mat[i][j]:
                                if self.animal_mat[i][j] == self.animal_mat[i - 1][j + 1] and self.animal_mat[i - 1][j] != 0:
                                    action_space.append(((i,j), (i-1,j)))
                                    break
                                if self.animal_mat[i][j] == self.animal_mat[i + 1][j - 1] and self.animal_mat[i][j - 1] != 0:
                                    action_space.append(((i,j-1), (i,j)))
                                    break
                            # a   a      a   b
                            #
                            #   a          a
                            #
                            # c          a


                    if i+1<self.height and j+1<self.width and self.animal_mat[i][j] == self.animal_mat[i + 1][j + 1]:
                        if self.animal_mat[i][j] == self.animal_mat[i - 1][j + 1] and self.animal_mat[i][j + 1] != 0:
                            action_space.append(((i,j), (i,j+1)))
                            break
                        if self.animal_mat[i][j] == self.animal_mat[i + 1][j - 1] and self.animal_mat[i + 1][j] != 0:
                            action_space.append(((i,j), (i+1,j)))
                            break
                           #     a          b
                           #
                           #   a          a
                           #
                           # b   a      a   a

                if self.animal_mat[i][j] == 7:
                    if i-1 > 0 and self.animal_mat[i-1][j] != 0:
                        action_space.append(((i,j),(i-1,j)))
                    if i+1<self.height and self.animal_mat[i+1][j] != 0:
                        action_space.append(((i,j),(i+1,j)))
                    if j-1>0 and self.animal_mat[i][j-1] != 0:
                        action_space.append(((i,j),(i,j-1)))
                    if j+1<self.width and self.animal_mat[i][j+1] != 0:
                        action_space.append(((i,j),(i,j+1)))
                    # 凤凰

                if self.spe_mat[i][j] != 0 and self.spe_mat[i][j]!=4:
                    if i-1>0 and self.spe_mat[i-1][j] != 0 and self.spe_mat[i-1][j] != 4:
                        action_space.append(((i, j), (i - 1, j)))
                    if i+1<self.height and self.spe_mat[i+1][j] != 0 and self.spe_mat[i+1][j] != 4:
                        action_space.append(((i, j), (i + 1, j)))
                    if j-1>0 and self.spe_mat[i][j-1] != 0 and self.spe_mat[i][j-1] != 4:
                        action_space.append(((i,j),(i,j-1)))
                    if j+1<self.width and self.spe_mat[i][j+1] != 0 and self.spe_mat[i][j+1] != 4:
                        action_space.append(((i,j),(i,j+1)))
                    # 挨着的特效

        self.action_space = action_space
        if len(action_space)==0:
            self.reshuffle()
            self.action_space = self.get_action_space()

        return self.action_space

    def generate_rd_pos(self):
        swap1_h = np.random.randint(0, self.height)
        swap1_w = np.random.randint(0, self.width)

        swap2_h = np.random.randint(0, self.height)
        swap2_w = np.random.randint(0, self.width)

        return (swap1_h,swap1_w), (swap2_h,swap2_w)

    def reshuffle(self):
        if len(self.action_space) > 0:
            return

        p1, p2 = self.generate_rd_pos()
        if self.animal_mat[p1[0]][p1[1]] != 0 and self.animal_mat[p2[0]][p2[1]] != 0:
            self.animal_mat[p1[0]][p1[1]],self.animal_mat[p2[0]][p2[1]] = self.animal_mat[p2[0]][p2[1]],self.animal_mat[p1[0]][p1[1]]
            self.spe_mat[p1[0]][p1[1]], self.spe_mat[p2[0]][p2[1]] = self.spe_mat[p2[0]][p2[1]], self.spe_mat[p1[0]][p1[1]]
        else:
            self.reshuffle()

    def Conv2(self, img, kernel):
        # img：输入图片；W,H：图片的宽和高；kernel：卷积核。
        # return：和输入图像尺寸大小相同的feature map；
        # 卷积大小固定为3*3卷积，这里因为固定了卷积大小，所以写代码前可以直接确定：卷积步长为1，四周个填充一排0
        H,W = img.shape[0],img.shape[1]
        col = np.zeros(H)
        raw = np.zeros(W + 2)
        img = np.insert(img, W, values=col, axis=1)
        img = np.insert(img, 0, values=col, axis=1)
        img = np.insert(img, H, values=raw, axis=0)
        img = np.insert(img, 0, values=raw, axis=0)
        res = np.zeros([H, W])  ##直接新建一个全零数组，省去了后边逐步填充数组的麻烦
        for i in range(H):
            for j in range(W):
                temp = img[i:i + 3, j:j + 3]
                temp = np.multiply(temp, kernel)
                res[i][j] = temp.sum()

        return res



    def get_state(self):

        state_mat = np.array(self.animal_mat)
        der = [[0,-1,0],[-1,4,-1],[0,-1,0]]
        ker = [[0.0947416,0.118318,0.0947416],[0.118318,0.147761,0.118318],[0.0947416,0.118318,0.0947416]]
        dern = np.array(der)
        kern = np.array(ker)
        state = self.Conv2(state_mat,dern)
        state = self.Conv2(state,kern)
        state = self.Conv2(state,dern)
        state = self.Conv2(state,kern)
        state = np.reshape(state,(1,self.height*self.width))

        return state[0]

    def step(self,action):
        old_score = self.score
        act_space = self.get_action_space()
        if action >= len(act_space):
            a = len(act_space)-1
        elif action < 0:
            a = 0
        else:
            a = action
        act = act_space[a]
        if self.last_act_space == act_space:
            self.same_cnt += 1
        else:
            self.same_cnt = 0
        self.last_act_space = act_space

        self.exchange(act[0],act[1])
        if self.same_cnt > 5:
            return self.get_state(), self.score-old_score,True

        return self.get_state(), self.score-old_score,False

    def reset(self):
        new_mat = np.random.randint(-1,7,(7,7))
        new_mat = new_mat.tolist()
        self.get_mat(new_mat)
        return self.get_state()

# if __name__ == "__main__":
#     bd = Board(5,5)
#     # mat_test = np.random.randint(-1,5,(7,7))
#     # mat_test = mat_test.tolist()
#     mat_test = [[1,2,3,4,5],[2,3,1,4,5],[2,3,1,5,4],[2,2,4,5,1],[4,3,4,2,1]]
#
#     bd.get_mat(mat_test)
#     bd.show()
#     print(bd.spe_mat)
#     print()
#     bd.exchange((0,0),(0,1))
#     bd.show()
#     print()
#     bd.exchange((0,1),(0,2))
#     bd.show()
#     print(bd.score)
#     print(bd.spe_mat)
#     print(bd.get_action_space())
#     print(bd.get_state())
