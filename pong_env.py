import pygame
import numpy as np
from pong_objects import Paddle, Ball

BLACK = (0,0,0)
WHITE = (255,255,255)

class Pong:
    def __init__(self):
        pygame.init()
        self.size = (700,500)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Pong")

        #paddle A
        self.paddleA = Paddle(WHITE, 10, 100)
        self.paddleA.rect.x = 20
        self.paddleA.rect.y = 200

        #paddle B
        self.paddleB = Paddle(WHITE, 10, 100)
        self.paddleB.rect.x = 670
        self.paddleB.rect.y = 200

        #ball
        self.ball = Ball(WHITE, 10, 10)
        self.ball.rect.x = 345
        self.ball.rect.y = 195

        self.all_sprite_list = pygame.sprite.Group()
        self.all_sprite_list.add(self.paddleA)
        self.all_sprite_list.add(self.paddleB)
        self.all_sprite_list.add(self.ball)

        #scoring
        self.scoreA = 0
        self.scoreB = 0

    def get_state(self):
        paddleA_ypos = self.paddleA.rect.y/1000
        #paddleB_ypos = self.paddleB.rect.y.copy()
        ball_xpos = self.ball.rect.x/1000
        ball_ypos = self.ball.rect.y/1000
        ball_xspeed = self.ball.velocity[0]/10
        ball_yspeed = self.ball.velocity[1]/10
        state = np.array([paddleA_ypos, ball_xpos, ball_ypos, ball_xspeed, ball_yspeed])
        return state

    def game_on(self, actionA, actionB):
        '''handles game logic'''

        reward = 0
        
        #player doing actions
        if actionA == 1:
            self.paddleA.moveUp(5)
            #reward -= 0.01
        elif actionA == 2:
            self.paddleA.moveDown(5)
            #reward -= 0.01
        else:
            pass

        if actionB == 1:
            self.paddleB.moveUp(5)
        elif actionB == 2:
            self.paddleB.moveDown(5)
        else:
            pass

        #ball bounces when hitting walls
        if self.ball.rect.x >= 690:
            self.ball.velocity[0] = -self.ball.velocity[0]
            self.scoreA += 1
        if self.ball.rect.x <= 0:
            self.ball.velocity[0] = -self.ball.velocity[0]
            self.scoreB += 1
            reward -= 1
        if self.ball.rect.y > 490:
            self.ball.velocity[1] = -self.ball.velocity[1]
        if self.ball.rect.y < 0:
            self.ball.velocity[1] = -self.ball.velocity[1]

        if pygame.sprite.collide_rect(self.ball, self.paddleA) and self.ball.velocity[0] < 0:
            reward += 1

        #ball bounces randomly when hitting paddle
        if pygame.sprite.collide_rect(self.ball, self.paddleA) or pygame.sprite.collide_rect(self.ball, self.paddleB):
            self.ball.bounce()

        #update sprites state
        self.all_sprite_list.update()

        #returning reward, next state, done
        next_state = self.get_state()
        done = False if self.scoreA < 5 else True
        return reward, next_state, done

    def display(self):
        #draw things
        self.screen.fill(BLACK)
        pygame.draw.line(self.screen, WHITE, [349, 0], [349, 500], 5)
        self.all_sprite_list.draw(self.screen)

        #display scores
        font = pygame.font.Font(None, 74)
        text = font.render(str(self.scoreA), 1, WHITE)
        self.screen.blit(text, (250,10))
        text = font.render(str(self.scoreB), 1, WHITE)
        self.screen.blit(text, (420,10))

        #update screen with whats been drawn
        pygame.display.flip()