import random
import numpy as np
import tensorflow as tf
from collections import deque



class Snake_DQN():
    def __init__(self, SIZE, max_len4train, UPDATE_SECONDARY_WEIGHTS, min_batch, min_len4train, DISCOUNT, Batch_Size):

        self.SIZE = SIZE
        self.model = self.to_initialize_model()
        self.secondary_model = self.to_initialize_model()

##        self.model.load_weights("weights")
        
        self.secondary_model.set_weights(self.model.get_weights())

        self.model.compile(loss="mse", optimizer=tf.keras.optimizers.Adam(lr=0.001), metrics=['accuracy'])
        self.secondary_model.compile(loss="mse", optimizer=tf.keras.optimizers.Adam(lr=0.001), metrics=['accuracy'])

        self.mem4train = deque(maxlen=max_len4train)

        self.UPDATE_SECONDARY_WEIGHTS = UPDATE_SECONDARY_WEIGHTS
        self.min_batch = min_batch
        self.min_len4train = min_len4train
        self.DISCOUNT = DISCOUNT
        self.Batch_Size = Batch_Size


    def to_initialize_model(self):        
        model = tf.keras.models.Sequential([tf.keras.layers.Conv2D(128, (1, 1), input_shape=(self.SIZE,self.SIZE,3)),
                                            tf.keras.layers.Activation('relu'),
                                            tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

                                            tf.keras.layers.Conv2D(128, (1, 1)),
                                            tf.keras.layers.Activation('relu'),
                                            tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

                                            tf.keras.layers.Dropout(0.1),

                                            tf.keras.layers.Flatten(),
                                            tf.keras.layers.Dense(64),
                                            tf.keras.layers.Dense(4, activation='linear')])

        return model

    def updating_mem4train(self,data):
        self.mem4train.append(data)                                  #[current_state, action, reward, new_current_state, done]

    def nn_training(self):
        if len(self.mem4train)<self.min_len4train:
            return
        
        training_data = random.sample(self.mem4train, self.min_batch)

        current_states = np.array([x[0] for x in training_data])
        current_q_list = self.model.predict(current_states)

        new_current_states = np.array([x[3] for x in training_data])
        future_q_list = self.secondary_model.predict(new_current_states)

        X=[]
        Y=[]

        for ind, training_data_iteration in enumerate(training_data):
            if not training_data_iteration[4]:
                max_future_q = np.max(future_q_list[ind])
                new_q = training_data_iteration[2] + self.DISCOUNT * max_future_q
            else:
                new_q = training_data_iteration[2]

            current_q = current_q_list[ind]
            current_q[training_data_iteration[1]] = new_q

            X.append(training_data_iteration[0])
            Y.append(current_q)


##        train_datagen = tf.keras.preprocessing.image.ImageDataGenerator()
##        fiit = self.model.fit_generator(train_datagen.flow(np.array(X),np.array(Y),batch_size=32, shuffle=False),
##                                        verbose=0, steps_per_epoch = len(np.array(X))/32, epochs=5)

        fiit = self.model.fit(np.array(X), np.array(Y), batch_size = self.Batch_Size, verbose=0, steps_per_epoch = len(np.array(X))/self.Batch_Size, shuffle = False, epochs = 4)

        if self.UPDATE_SECONDARY_WEIGHTS == True:
            self.secondary_model.set_weights(self.model.get_weights())
            self.UPDATE_SECONDARY_WEIGHTS = False
            

    def nn_predicting(self,cur_img):
        return self.model.predict(np.array(cur_img).reshape(-1, *cur_img.shape))[0]

