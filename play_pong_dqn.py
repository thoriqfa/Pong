import agents
import pong_env
import pygame
import numpy as np
from keras.models import model_from_json
import matplotlib.pyplot as plt

player_random = agents.RandomAgent(3)
player_dqn = agents.DQNAgent(5, 3)

'''
#player dqn uses saved model
json_file = open("q_model.json", "r")
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("q_model.h5")
print("Model loaded.")

player_dqn.q = loaded_model
player_dqn.q_target = loaded_model
'''

num_play = 5
clock = pygame.time.Clock()
scores = []
epsilons = []


for i in range(num_play):
    done = False
    exits = False
    score = 0
    game = pong_env.Pong()
    state = game.get_state()
    while not done or not exits:
        #terminate if user quits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exits = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    exits = True

        #game.display()

        dqn_act = player_dqn.choose_action(state)
        random_act = player_random.choose_action()

        #dqn as player A, random as player B
        reward, next_state, done = game.game_on(dqn_act, random_act)

        player_dqn.store_transition(state, dqn_act, reward, next_state, done)
        player_dqn.learn()

        score += reward
        state = next_state
        #clock.tick(60)
    pygame.quit()
    scores.append(score)
    epsilons.append(player_dqn.epsilon)
    print("Episode: ", i, " Score: ", score, " Epsilon: ", player_dqn.epsilon)

'''
#save trained model to disk
model_json = player_dqn.q.to_json()
with open("q_model.json", "w") as json_file:
    json_file.write(model_json)
player_dqn.q.save_weights("q_model.h5")
print("Q model saved")


plt.plot(scores, color="red", label="Scores")
plt.plot(epsilons, color="blue", label="Epsilons")
plt.xlabel("Episodes")
plt.legend()
plt.savefig("Pong_training_1000_7jun.png", dpi=150)
plt.show()
'''