import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Resistance vs The Empire!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 


BORDER = pygame.Rect(0, HEIGHT/2, 100000, 10)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'shoot_wing.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'blast.mp3'))

HEALTH_FONT = pygame.font.SysFont('arial', 40)
WINNER_FONT = pygame.font.SysFont('arial', 65)

FPS = 120
VEL = 5
BULLET_VEL = 7
ALL_BULLETS = 999999999999999999999999999999999999999
SHIP_WIDTH, SHIP_HEIGHT = 100, 75

TIE_HIT = pygame.USEREVENT + 1
WING_HIT = pygame.USEREVENT + 2

TIE_SHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'ship_tie.png')) 
TIE_SHIP = pygame.transform.rotate(pygame.transform.scale(
    TIE_SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 90)
WING_SHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'ship_wing.png'))
WING_SHIP = pygame.transform.rotate(pygame.transform.scale(WING_SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 90)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space_background.png')), (WIDTH, HEIGHT))

def draw_window(wing, tie, wing_bullets, tie_bullets, green_health, red_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER )

    green_health_text = HEALTH_FONT.render(
        "HEALTH: " + str(green_health), 1, WHITE)
    red_health_text = HEALTH_FONT.render(
        "HEALTH: " + str(red_health), 1, WHITE)
    WIN.blit(green_health_text, (WIDTH - green_health_text.get_width() - 10, 10))
    WIN.blit(red_health_text, (10 , 10))
    
    WIN.blit(TIE_SHIP, (tie.x, tie.y))
    WIN.blit(WING_SHIP, (wing.x, wing.y))

    for bullet in wing_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

    for bullet in tie_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()

def tie_handle_movement(keys_pressed, tie):
    if keys_pressed[pygame.K_a] and tie.x - VEL > 0: # LEFT
        tie.x -= VEL
    if keys_pressed[pygame.K_d] and tie.x + VEL + tie.height - 650 < BORDER.y: # RIGHT
        tie.x += VEL
    if keys_pressed[pygame.K_w] and tie.y - VEL > 350: # UP
        tie.y -= VEL
    if keys_pressed[pygame.K_s] and tie.y + VEL + tie.height < HEIGHT: # DOWN
        tie.y += VEL

def wing_handle_movement(keys_pressed, wing):
    if keys_pressed[pygame.K_LEFT] and wing.x - VEL > 0: # LEFT
        wing.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and wing.x + VEL + wing.width < WIDTH: # RIGHT
        wing.x += VEL
    if keys_pressed[pygame.K_UP] and wing.y - VEL > 0: # UP
        wing.y -= VEL
    if keys_pressed[pygame.K_DOWN] and wing.y + VEL + wing.height < 350: # DOWN
        wing.y += VEL

def handle_bullets(tie_bullets, wing_bullets, tie, wing):
    for bullet in tie_bullets:
        bullet.y -= BULLET_VEL
        if wing.colliderect(bullet):
            pygame.event.post(pygame.event.Event(WING_HIT))
            tie_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            tie_bullets.remove(bullet)

    for bullet in wing_bullets:
        bullet.y += BULLET_VEL
        if tie.colliderect(bullet):
            pygame.event.post(pygame.event.Event(TIE_HIT))
            wing_bullets.remove(bullet)
        elif bullet.x < 0:
            wing_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def cool():
    wing = pygame.Rect(425, 100, SHIP_WIDTH, SHIP_HEIGHT)
    tie = pygame.Rect(400, 425, SHIP_WIDTH, SHIP_HEIGHT)

    tie_bullets = []
    wing_bullets = []

    green_health = 15
    red_health = 15

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and len(tie_bullets) < ALL_BULLETS:
                    bullet = pygame.Rect(tie.x + tie.width, tie.y + tie.height//2 - 5, 7 , 5)
                    tie_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(wing_bullets) < ALL_BULLETS:
                    bullet = pygame.Rect(wing.x, wing.y + wing.height//2 - 5, 7 , 5)
                    wing_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == WING_HIT:
                green_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == TIE_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
        winner_text = ""
        if green_health <= 0:
            winner_text = "The Empire Has Won!"

        if red_health <= 0:
            winner_text = "The Rebel Scum Have Won!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        wing_handle_movement(keys_pressed, wing)
        tie_handle_movement(keys_pressed, tie)
        
        handle_bullets(tie_bullets, wing_bullets, tie, wing)
        
        draw_window(wing, tie, wing_bullets, tie_bullets, green_health, red_health)

    cool()


cool()

