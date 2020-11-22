import random
import cv2
from PIL import Image
import numpy as np
import copy
import math


class Snake_game:
    snake = [0,0,255]
    food = [255,0,0]
    def __init__(self, SIZE, length_of_hinder=3, hinder_nos=3):
        self.SIZE = SIZE
        self.hinder = np.array([[255,255,255] for i in range(length_of_hinder)])
        self.snake_pos = [self.SIZE//2,self.SIZE//2,0]
        self.body={}
        self.food_pos =  random.sample(range(self.SIZE),2)
        self.snake_len = 0
        self.velo = 100
        self.refer = self.snake_pos
        self.game = np.zeros((self.SIZE,self.SIZE,3))

        self.hinder_pos = []
        for loo in range(hinder_nos):
            xh = np.random.randint(SIZE-1)
            yh = np.random.randint(SIZE-1)
            while (yh<=SIZE//2 and yh+len(self.hinder)>=SIZE//2) and xh==SIZE//2:
                xh = np.random.randint(SIZE-1)
                yh = np.random.randint(SIZE-1)

            for i in range(len(self.hinder)):
                if yh+i>=SIZE:
                    yh = (-1)*i
                if [xh,yh+i] == self.food_pos:
                    continue
                self.hinder_pos.append([xh,yh+i])
                self.game[xh][yh+i] = self.hinder[i]
        
        self.refer = copy.deepcopy(self.snake_pos)
        self.body[self.snake_len] = self.snake_pos
        self.end = False
        self.point = False

    def play(self,ch):
        self.snake_pos[2] = ch
        self.move()
        
        
    def point_val(self):
        if self.snake_pos[:-1] == self.food_pos:
            self.snake_len += 1
            self.body[self.snake_len] = self.refer
            self.refer = copy.deepcopy(self.body[self.snake_len])
            self.food_pos = random.sample(range(self.SIZE),2)
            ref_lis = self.body.values()
            ref_lis = [i[:-1] for i in ref_lis]
            while self.food_pos in ref_lis:
                self.food_pos = random.sample(range(self.SIZE),2)
            return True
        else:
            return False


    def end_val1(self):
        if (self.snake_pos[0]<=0 and self.snake_pos[2]==0):
            self.snake_pos[0] = self.SIZE
        elif (self.snake_pos[1]>=self.SIZE-1 and self.snake_pos[2]==1):
            self.snake_pos[1]=-1
        elif (self.snake_pos[0]>=self.SIZE-1 and self.snake_pos[2]==2):
            self.snake_pos[0]=-1
        elif (self.snake_pos[1]<=0 and self.snake_pos[2]==3):
            self.snake_pos[1]= self.SIZE


    def end_val2(self):
        ref_dic = {}
        for i in self.body:
            if i==0:
                continue
            ref_dic[i]=self.body[i][:-1]
        if self.snake_pos[:-1] in ref_dic.values():
            return True
        else:
            return False

    def end_val3(self):
        if self.snake_pos[:-1] in self.hinder_pos:
            return True
        else:
            return False


    def move(self):

        self.end_val1()

        if not(self.end):
            self.refer = copy.deepcopy(self.body[self.snake_len])

            if self.snake_pos[2]==0:                 #up
                self.snake_pos[0] = self.snake_pos[0]-1

            elif self.snake_pos[2]==1:              #right
                self.snake_pos[1] = self.snake_pos[1]+1

            elif self.snake_pos[2]==2:                #down
                self.snake_pos[0] = self.snake_pos[0]+1

            elif self.snake_pos[2]==3:                 #left
                self.snake_pos[1] = self.snake_pos[1]-1

            ref_dic = copy.deepcopy(self.body)
            self.body[0] = copy.deepcopy(self.snake_pos)
            for i in self.body:
                if i==0:
                    continue
                self.body[i] = ref_dic[i-1]


            self.point = self.point_val()
            if self.end_val2():
                cv2.destroyWindow('snake')
                # print('game over')
                self.end=True

            if self.end_val3():
                cv2.destroyWindow('snake')
                # print('game over')
                self.end=True

            
    def display(self):
        self.game = np.zeros((self.SIZE,self.SIZE,3), dtype=np.uint8)
        if len(self.body)>1:
            for i in self.body.values():
                self.game[i[0]][i[1]] = self.snake
        else:
            self.game[self.snake_pos[0]][self.snake_pos[1]] = self.snake
        self.game[self.food_pos[0]][self.food_pos[1]] = self.food

        for i in self.hinder_pos:
            self.game[i[0]][i[1]] = [255,255,255]

        img = Image.fromarray(self.game, 'RGB')
        img = img.resize((600,600))
        cv2.imshow('snake',np.array(img))
        cv2.waitKey(30)
        key = cv2.waitKey(20) & 0xFF
        if key==27:
            cv2.destroyWindow('snake')
            self.end=True
        self.velo = 100/math.sqrt((self.snake_len+1))

    def to_get_array(self, prev_mov ,action):
        self.game = np.zeros((self.SIZE,self.SIZE,3), dtype=np.uint8)
        if len(self.body)>1:
            for i in self.body.values():
                self.game[i[0]][i[1]] = self.snake
        else:
            self.game[self.snake_pos[0]][self.snake_pos[1]] = self.snake
        self.game[self.food_pos[0]][self.food_pos[1]] = self.food

        if self.end == True and self.point == False:
            reward = -10
        elif self.point == True:
            reward = 2
            self.point = False
        else:
            reward = -1

        return (prev_mov, action, reward, self.game/255, self.end)

    def to_get_init_move(self):
        self.game = np.zeros((self.SIZE,self.SIZE,3), dtype=np.uint8)
        if len(self.body)>1:
            for i in self.body.values():
                self.game[i[0]][i[1]] = self.snake
        else:
            self.game[self.snake_pos[0]][self.snake_pos[1]] = self.snake
        self.game[self.food_pos[0]][self.food_pos[1]] = self.food

        return self.game/255
