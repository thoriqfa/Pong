import agents
import pong_env
import pygame
import numpy as np
import matplotlib.pyplot as plt

player_random = agents.RandomAgent(3)
player_dqn = agents.DQNAgent(5, 3)

'''
#player dqn uses saved model
model = "q_model_4_5"
player_dqn.q_from_load_model(model)
print("Model loaded.")
'''

num_play = 100
clock = pygame.time.Clock()
scores = []
epsilons = []

break_learning = False
for i in range(num_play):
    done = False
    exits = False
    score = 0
    game = pong_env.Pong()
    while not done and not exits:
        #terminate if user quits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exits = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    exits = True
                if event.key == pygame.K_b:
                    break_learning = True
                    print("Game will stop after this current episode.")
        
        game.display()

        state = game.get_state()
        dqn_act = player_dqn.choose_action(state)
        random_act = player_random.choose_action()

        #dqn as player A, random as player B
        reward, next_state, done = game.game_on(dqn_act, random_act)

        player_dqn.store_transition(state, dqn_act, reward, next_state, done)
        player_dqn.learn()

        score += reward
        #clock.tick(60)
    
    pygame.quit()
    scores.append(score)
    epsilons.append(player_dqn.epsilon)
    print("Episode: ", i, " Score: ", score, " Epsilon: ", player_dqn.epsilon)
    #stops learning
    if break_learning:
        break

print(player_dqn.q.get_weights())
#save trained model to disk
player_dqn.q.save("q_model_4_7")
print("Q model saved")


plt.plot(scores, color="red", label="Scores")x
plt.plot(epsilons, color="blue", label="Epsilons")
plt.xlabel("Episodes")
plt.legend()
plt.savefig("Pong_training_200_9jun_1.png", dpi=150)
plt.show()
