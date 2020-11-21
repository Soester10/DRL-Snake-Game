#snake game

import math
from Snake_game import Snake_game
from Snake_DQN import Snake_DQN
from Game import Game


SIZE =10
min_len4train = 500
max_len4train = 50_000
DISCOUNT = 0.90
TO_SHOW_GAME = 100
min_batch = 64
Batch_Size = 32
LENGTH_OF_EACH_GAME = 9
LEARNING_RATE = 0.01
UPDATE_SECONDARY_WEIGHTS = False
UPDATE_SECONDARY_WEIGHTS_NUM = 4
STEPS_PER_GAME = 200

EPISODES = 1500

epsilon = 1
epsilon_mul_value = math.log(0.01, 10)/(EPISODES * 0.8)
epsilon_mul_value = math.pow(10, epsilon_mul_value)

#main

Neuron = Snake_DQN(SIZE, max_len4train, UPDATE_SECONDARY_WEIGHTS, min_batch, min_len4train, DISCOUNT, Batch_Size)
Game(Neuron, Snake_game, SIZE, STEPS_PER_GAME, EPISODES, min_len4train, epsilon, epsilon_mul_value, TO_SHOW_GAME, UPDATE_SECONDARY_WEIGHTS_NUM)

Neuron.model.save_weights("weights")
Neuron.model.save("model.h5")

