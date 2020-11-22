import random
import numpy as np
from tqdm import tqdm




def Game(Neuron, Snake_game, SIZE, length_of_hinder, hinder_nos, STEPS_PER_GAME, EPISODES, min_len4train, epsilon, epsilon_mul_value, TO_SHOW_GAME, UPDATE_SECONDARY_WEIGHTS_NUM):
    m=0
    score = []
    for epi in tqdm(range(1, EPISODES + 1), ascii=True, unit='Episodes'):
        Game = Snake_game(SIZE, length_of_hinder, hinder_nos)
        Game.end = False
        count = 0
        while True:
            count += 1
            prev_mov = Game.to_get_init_move()
            if epi<min_len4train:
                m2=random.randint(0,3)
            elif np.random.random() < epsilon:

                m2 = random.randint(0,3)
            else:
                m2 = np.argmax(Neuron.nn_predicting(prev_mov))

            while (m2-2==m or m2+2==m):
                m2 = random.randint(0,3)
            m=m2

            Game.play(m)
            mem4training = Game.to_get_array(prev_mov, m)

            if epi%TO_SHOW_GAME == 0:
                Game.display()

            Neuron.updating_mem4train(mem4training)
            if epi>=min_len4train:
                Neuron.nn_training()

            if Game.end or count>=STEPS_PER_GAME:
                if epi%UPDATE_SECONDARY_WEIGHTS_NUM == 0:
                    UPDATE_SECONDARY_WEIGHTS = True
                break

        epsilon *= epsilon_mul_value


    ##    print('Total:',Game.snake_len)
        score.append(Game.snake_len)

