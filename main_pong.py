import pygame
from paddle import Paddle
from ball import Ball
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

#Loop while true
gameOn = True

#clock controls how fast screen updates
clock = pygame.time.Clock()

#Main
while gameOn:

    #terminate if user quits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOn = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                gameOn = False
    
    #game logic
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.moveUp(5)
    if keys[pygame.K_s]:
        paddleA.moveDown(5)
    if keys[pygame.K_UP]:
        paddleB.moveUp(5)
    if keys[pygame.K_DOWN]:
        paddleB.moveDown(5)
    
    all_sprite_list.update()

    #hit the wall
    if ball.rect.x >= 690:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x <= 0:
        ball.velocity[0] = -ball.velocity[0]
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

    #update screen with whats been drawn
    pygame.display.flip()

    #limit to 60 fps
    clock.tick(60)

pygame.quit()
    