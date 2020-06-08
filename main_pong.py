import pygame
from agents import RandomAgent, HumanAgent
from pong_objects import Paddle, Ball
pygame.init()

#Defining base color
BLACK = (0,0,0)
WHITE = (255,255,255)

#Make game window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")

paddleA = Paddle(WHITE, 10, 100)
paddleA.rect.x = 20
paddleA.rect.y = 200

paddleB = Paddle(WHITE, 10, 100)
paddleB.rect.x = 670
paddleB.rect.y = 200

ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195

all_sprite_list = pygame.sprite.Group()
all_sprite_list.add(paddleA)
all_sprite_list.add(paddleB)
all_sprite_list.add(ball)

#player agents
player_random = RandomAgent(3)
player_human = HumanAgent()

#Loop while true
gameOn = True

#clock controls how fast screen updates
clock = pygame.time.Clock()

#player score
scoreA = 0
scoreB = 0

#Main
while gameOn:

    #terminate if user quits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                gameOn = False
    
    ##game logic
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.moveUp(5)
    if keys[pygame.K_s]:
        paddleA.moveDown(5)
    if keys[pygame.K_UP]:
        paddleB.moveUp(5)
    if keys[pygame.K_DOWN]:
        paddleB.moveDown(5)
    
    '''
    #random player move
    random_action = player_random.choose_action()
    if random_action == 1:
        paddleA.moveUp(5)
    elif random_action == 2:
        paddleA.moveDown(5)
    else:
        pass

    human_action = player_human.choose_action()
    if human_action == 1:
        paddleB.moveUp(5)
    elif human_action == 2:
        paddleB.moveDown(5)
    else:
        pass
    '''

    all_sprite_list.update()

    #hit the wall
    if ball.rect.x >= 690:
        ball.velocity[0] = -ball.velocity[0]
        scoreA += 1
    if ball.rect.x <= 0:
        ball.velocity[0] = -ball.velocity[0]
        scoreB += 1
    if ball.rect.y > 490:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y < 0:
        ball.velocity[1] = -ball.velocity[1]

    #bounce to paddle
    if pygame.sprite.collide_rect(ball, paddleA) or pygame.sprite.collide_rect(ball, paddleB):
        ball.bounce()

    
    #draw things
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, [349, 0], [349, 500], 5)
    all_sprite_list.draw(screen)

    #display scores
    font = pygame.font.Font(None, 74)
    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (250,10))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (420,10))

    #update screen with whats been drawn
    pygame.display.flip()
    
    #print("Score A: ", scoreA, " Score B: ", scoreB)
    
    #limit to 60 fps
    clock.tick(60)

pygame.quit() 