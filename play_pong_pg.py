import agents
import pong_env
import pygame
import matplotlib.pyplot as plt
from datetime import datetime

#get datetime data for file name
now = datetime.now()

player_random = agents.RandomAgent(3)
player_pg = agents.PolicyGradientAgent(5, 3)

'''
#player pg uses saved model
model = "pg_model_1_3"
player_pg.from_load_model(model)
print("Model loaded.")
'''

num_play = 2
clock = pygame.time.Clock()
scores = []

break_learning = False
display = True
for i in range(num_play):
    done = False
    score = 0
    game = pong_env.Pong()
    while not done:
        if display:
            game.display()

        state = game.get_state()
        pg_act, prob = player_pg.choose_action(state)
        random_act = player_random.choose_action()

        #pg as player A, random as player B
        reward, next_state, done = game.game_on(pg_act, random_act)

        player_pg.store_transition(state, pg_act, prob, reward)
        #print(prob)
        score += reward

        #terminate if user quits
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    done = True
                if event.key == pygame.K_b:
                    break_learning = True
                    print("Game will stop after this current episode.")
                if event.key == pygame.K_d:
                    display = not display
                    print("Display: ", display)
        
        #clock.tick(60)
    player_pg.learn()
    pygame.quit()
    scores.append(score)

    print("Episode: ", i, " Score: ", score)
    #stops learning
    if break_learning:
        break

#save trained model to disk
player_pg.model.save("pg_model_1_4")
print("Model saved")


plt.plot(scores, color="red", label="Scores")
plt.xlabel("Episodes")
filename = "Pong_training_pg_"+ str(num_play) +"_"+ str(now.strftime("%Y-%m-%d")) +"_"+ str(now.strftime("%H.%M")) +".png"
plt.savefig(filename, dpi=150)
print("Showing plot.")
plt.show()
