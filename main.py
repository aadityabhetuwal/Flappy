import pygame
import os

from random import randint

pygame.init()
pygame.font.init()
pygame.mixer.init()

# font
SCORE_FONT = pygame.font.SysFont("bitstreamverasans", 40)

# sounds
DIE_SOUND = pygame.mixer.Sound(os.path.join("audio", "die.ogg"))
HIT_SOUND = pygame.mixer.Sound(os.path.join("audio", "hit.ogg"))
POINT_SOUND = pygame.mixer.Sound(os.path.join("audio", "point.ogg"))
UPFLAP_SOUND = pygame.mixer.Sound(os.path.join("audio", "swoosh.ogg"))
# constants

WHITE = (255, 255, 255)
WIDTH, HEIGHT = 576, 768
FPS = 60
VEL_FLOOR = 2

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy")

# background
BACKGROUND_DAY = pygame.transform.scale(
    pygame.image.load(os.path.join("sprites", "background-day.png")).convert_alpha(), (WIDTH, HEIGHT))

BASE_IMG = pygame.image.load(os.path.join("sprites", "base.png")).convert_alpha()

BASE = pygame.transform.scale(BASE_IMG, (WIDTH, BASE_IMG.get_height() - 2))

BASE_X = 0
BASE_Y = HEIGHT - BASE.get_height()

# bird
BIRD_WID, BIRD_HEI = 35, 25
VEL_BIRD = 9.3
G = .35
THETA = 25

PIPE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("sprites", "pipe-green.png")).convert_alpha())
PIPE_IMG_FILP = pygame.transform.rotate(PIPE_IMG, 180)

MIDFLAP_IMG = pygame.transform.scale(
    pygame.image.load(os.path.join("sprites", "yellowbird-downflap.png")).convert_alpha(), (BIRD_WID, BIRD_HEI))

UPFLAP_IMG = pygame.transform.scale(
    pygame.image.load(os.path.join("sprites", "yellowbird-upflap.png")).convert_alpha(), (BIRD_WID, BIRD_HEI))

DOWNFLAP_IMG = pygame.transform.scale(
    pygame.image.load(os.path.join("sprites", "yellowbird-downflap.png")).convert_alpha(), (BIRD_WID, BIRD_HEI))

GAME_OVER = pygame.transform.scale2x(
    pygame.image.load(os.path.join("sprites", "gameover.png")).convert_alpha())

START_SCREEN = pygame.transform.scale2x(
    pygame.image.load(os.path.join("sprites", "message.png")).convert_alpha())

SCORE_0 = pygame.transform.scale2x(
    pygame.image.load(os.path.join("sprites", "0.png")).convert_alpha())

SCORE_1 = pygame.transform.scale2x(
    pygame.image.load(os.path.join("sprites", "1.png")).convert_alpha())

SCORE_2 = pygame.transform.scale2x(
    pygame.image.load(os.path.join("sprites", "2.png")).convert_alpha())

SCORE_3 = pygame.transform.scale2x(
    pygame.image.load(os.path.join("sprites", "3.png")).convert_alpha())

SCORE_4 = pygame.transform.scale2x(
    pygame.image.load(os.path.join("sprites", "4.png")).convert_alpha())

SCORE_5 = pygame.transform.scale2x(
    pygame.image.load(os.path.join("sprites", "5.png")).convert_alpha())

SCORE_6 = pygame.transform.scale2x(
    pygame.image.load(os.path.join("sprites", "6.png")).convert_alpha())

SCORE_7 = pygame.transform.scale2x(
    pygame.image.load(os.path.join("sprites", "7.png")).convert_alpha())

SCORE_8 = pygame.transform.scale2x(
    pygame.image.load(os.path.join("sprites", "8.png")).convert_alpha())

SCORE_9 = pygame.transform.scale2x(
    pygame.image.load(os.path.join("sprites", "9.png")).convert_alpha())

SCORE_IMG = [SCORE_0, SCORE_1, SCORE_2, SCORE_3, SCORE_4, SCORE_5, SCORE_6, SCORE_7, SCORE_8, SCORE_9]
# User events
BIRD_HIT = pygame.USEREVENT + 1

SPAWNPIPE = pygame.USEREVENT + 2

SCORE = 0
score_ind = []
SCORE_WID, SCORE_HEI = WIDTH // 2 - 70, 20


class Bird(pygame.sprite.Sprite):

    def __init__(self, posx, posy):
        super(Bird, self).__init__()
        self.bird_movement = 0
        self.posx = posx
        self.posy = posy
        self.sprites = []
        self.keypress = False

        self.sprites.append(MIDFLAP_IMG)
        self.sprites.append(pygame.transform.rotate(UPFLAP_IMG, THETA))
        self.sprites.append(pygame.transform.rotate(DOWNFLAP_IMG, -THETA))

        self.current_sprite = 0

        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()

        self.rect.topleft = [self.posx, self.posy]

    def upflap(self):
        self.keypress = True

    def update(self):
        if self.keypress:
            self.bird_movement = 0
            self.bird_movement -= VEL_BIRD
            self.keypress = False

        self.bird_movement += G
        self.rect.y += self.bird_movement

    def draw(self, moving, upflap):

        self.moving = moving
        self.is_upflap = upflap

        if self.is_upflap:
            self.current_sprite = 1
            self.image = self.sprites[int(self.current_sprite)]
            self.moving.draw(WIN)

        else:
            self.current_sprite = 2
            self.image = self.sprites[self.current_sprite]
            self.moving.draw(WIN)

    def get_rectangle(self):
        return self.rect


def create_pipe():
    heights = [HEIGHT // 2, HEIGHT // 3, HEIGHT - BASE_IMG.get_height() - 200, HEIGHT - 400, HEIGHT - 200]
    x = randint(0, len(heights) - 1)
    pipe = PIPE_IMG.get_rect(topleft=(WIDTH + PIPE_IMG.get_width(), heights[x]))
    pipe1 = PIPE_IMG_FILP.get_rect(bottomleft=(WIDTH + PIPE_IMG.get_width(), heights[x] - 200))
    return [pipe, pipe1]


def sprite_collision_check(moving, non_moving, pipes):
    bird_rect = moving.get_rectangle()

    if bird_rect.colliderect(non_moving):
        pygame.event.post(pygame.event.Event(BIRD_HIT))

    for pipe in pipes:
        if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
            pygame.event.post(pygame.event.Event(BIRD_HIT))


def move_pipes(pipes, bird):
    global SCORE

    for pipe in pipes:
        pipe[0].x -= 5
        pipe[1].x -= 5

        if pipe[0].x + PIPE_IMG.get_width() < 0:
            pipes.remove(pipe)
            SCORE += 1
            POINT_SOUND.play()

    return pipes


def start_screen():
    global SCORE

    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = False

                    main()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    run = False
                    main()

        WIN.blit(BACKGROUND_DAY, (0, 0))
        WIN.blit(START_SCREEN, (WIDTH // 6, HEIGHT // 6))
        pygame.display.update()
    pygame.quit()


def death_screen():
    global SCORE, score_ind, SCORE_IMG

    run = True

    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = False
                    SCORE = 0
                    start_screen()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    run = False
                    SCORE = 0
                    start_screen()

        WIN.blit(BACKGROUND_DAY, (0, 0))

        if len(score_ind) == 2:
            WIN.blit(SCORE_IMG[score_ind[0]], (SCORE_WID, SCORE_HEI))
            WIN.blit(SCORE_IMG[score_ind[1]], (SCORE_WID + SCORE_0.get_height() - 20, SCORE_HEI))
        elif len(score_ind) == 3:
            WIN.blit(SCORE_IMG[score_ind[0]], (SCORE_WID, SCORE_HEI))
            WIN.blit(SCORE_IMG[score_ind[1]], (SCORE_WID + SCORE_0.get_height() - 20, SCORE_HEI))
            WIN.blit(SCORE_IMG[score_ind[2]], (SCORE_WID + SCORE_0.get_height() * 2 - 40, SCORE_HEI))
        elif len(score_ind) == 4:
            WIN.blit(SCORE_IMG[score_ind[0]], (SCORE_WID, SCORE_HEI))
            WIN.blit(SCORE_IMG[score_ind[1]], (SCORE_WID + SCORE_0.get_height() - 20, SCORE_HEI))
            WIN.blit(SCORE_IMG[score_ind[2]], (SCORE_WID + SCORE_0.get_height() * 2 - 40, SCORE_HEI))
            WIN.blit(SCORE_IMG[score_ind[3]], (SCORE_WID + SCORE_0.get_height() * 3 - 60, SCORE_HEI))

        WIN.blit(GAME_OVER, (WIDTH // 5 - 25, HEIGHT // 2 - 100))

        pygame.display.update()
    pygame.quit()


def draw_window(moving_sprites, base, pipes, upflap, bird):
    global SCORE, score_ind
    WIN.blit(BACKGROUND_DAY, (0, 0))

    for pipe in pipes:
        WIN.blit(PIPE_IMG, pipe[0])
        WIN.blit(PIPE_IMG_FILP, pipe[1])

    WIN.blit(BASE, base)
    WIN.blit(BASE, (BASE_X, BASE_Y))
    WIN.blit(BASE, (BASE_X + WIDTH, BASE_Y))

    if len(score_ind) == 2:
        WIN.blit(SCORE_IMG[score_ind[0]], (SCORE_WID, SCORE_HEI))
        WIN.blit(SCORE_IMG[score_ind[1]], (SCORE_WID + SCORE_0.get_height() - 20, SCORE_HEI))
    elif len(score_ind) == 3:
        WIN.blit(SCORE_IMG[score_ind[0]], (SCORE_WID, SCORE_HEI))
        WIN.blit(SCORE_IMG[score_ind[1]], (SCORE_WID + SCORE_0.get_height() - 20, SCORE_HEI))
        WIN.blit(SCORE_IMG[score_ind[2]], (SCORE_WID + SCORE_0.get_height() * 2 - 40, SCORE_HEI))
    elif len(score_ind) == 4:
        WIN.blit(SCORE_IMG[score_ind[0]], (SCORE_WID, SCORE_HEI))
        WIN.blit(SCORE_IMG[score_ind[1]], (SCORE_WID + SCORE_0.get_height() - 20, SCORE_HEI))
        WIN.blit(SCORE_IMG[score_ind[2]], (SCORE_WID + SCORE_0.get_height() * 2 - 40, SCORE_HEI))
        WIN.blit(SCORE_IMG[score_ind[3]], (SCORE_WID + SCORE_0.get_height() * 3 - 60, SCORE_HEI))

    bird.draw(moving_sprites, upflap)

    pygame.display.update()


def get_num():
    global score_ind, SCORE
    if SCORE <= 9:
        score_ind = [0, int(SCORE)]
    elif SCORE <= 99:
        st = str(SCORE)
        score_ind = [int(st[0]), int(st[1])]
    elif SCORE <= 999:
        st = str(SCORE)
        score_ind = [int(st[0]), int(st[1]), int(st[2])]
    elif SCORE <= 9999:
        st = str(SCORE)
        score_ind = [int(st[0]), int(st[1]), int(st[2]), int(st[3])]


def main():
    global BASE_X, SCORE, score_ind
    SCORE = 0
    bird = Bird(50, HEIGHT // 2)

    base = pygame.Rect(0, HEIGHT - BASE.get_height(), WIDTH, 10)

    moving_sprites = pygame.sprite.Group()
    moving_sprites.add(bird)

    pipe_list = []

    pygame.time.set_timer(SPAWNPIPE, 1500)

    clock = pygame.time.Clock()
    run = True
    upflap = False

    time_upflap = 0

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.upflap()
                    UPFLAP_SOUND.play()
                    upflap = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    bird.upflap()
                    UPFLAP_SOUND.play()
                    upflap = True

            if event.type == BIRD_HIT:
                run = False
                HIT_SOUND.play()
                pygame.time.delay(400)
                DIE_SOUND.play()
                death_screen()

            if event.type == SPAWNPIPE:
                pipe_list.append(create_pipe())
                print(pipe_list)

        # bird
        bird.update()

        # floor
        BASE_X -= VEL_FLOOR
        if BASE_X <= -WIDTH:
            BASE_X = 0

        # pipes
        pipe_list = move_pipes(pipe_list, bird)

        sprite_collision_check(bird, base, pipe_list)

        get_num()
        if upflap:
            draw_window(moving_sprites, base, pipe_list, upflap, bird)
            time_upflap += 1
        else:
            draw_window(moving_sprites, base, pipe_list, upflap, bird)

        if time_upflap > 30:
            upflap = False
            time_upflap = 0

    pygame.quit()


if __name__ == "__main__":
    start_screen()
