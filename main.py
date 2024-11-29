import pygame as pg
from random import randrange
from queue import Queue
import random

q = Queue()

pg.init()

# Constants
WINDOW = 700
FPS = 60
TITLE_SIZE = 50 # Cell size
RANGE = (TITLE_SIZE // 2, WINDOW - TITLE_SIZE // 2, TITLE_SIZE)
playlist = ['music/dymok.mp3', 'music/Gorod_Sochi.mp3', 'music/Imperatrica.mp3',\
            'music/Mardzhandzha.mp3', 'music/Mladshijj_lejjtenant.mp3',\
            'music/Samogonchik.mp3', 'music/SHarik.mp3', 'music/Ugonshhica.mp3',\
            'music/Vladimirskijj_central.mp3', 'music/Zapakhlo_vesnojj.mp3',\
            'music/Ljokha.mp3']
default_music = True

## Music
new_highscore_sound = pg.mixer.Sound('music/game-won.mp3')
gameover_sound = pg.mixer.Sound('music/gameover_1.mp3')

## Menu
score_font = pg.font.SysFont('arial', 36)
menu_font = pg.font.SysFont('arial', 46)
pomer_font = pg.font.SysFont('arial', 54, True)
title_font = pg.font.SysFont('arial', 50, True)

# Object initialization
gameScreen = pg.display.set_mode([WINDOW] * 2)
pg.display.set_caption('Змейка для смешариков')
clock = pg.time.Clock()

# Func to define random position coordinats (X:Y) on game board
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]



def print_score(score):
    val = score_font.render("Счет: " + str(score), True, (255, 255, 255))
    gameScreen.blit(val, [0, 0])

def make_highscore_file(cur_score, highscore):
    if cur_score > highscore:
        file = open("highscore.txt", "w")
        file.write(str(cur_score))
        res = cur_score
        file.close()
        new_highscore_sound.play()
    else:
        res = highscore
        gameover_sound.play()


    return str(res)

def gameLoop():
    # Snake parameters
    snake = pg.rect.Rect([0, 0, TITLE_SIZE - 2, TITLE_SIZE - 2])
    snake.center = get_random_position()
    length = 1
    segments = [snake.copy()]
    directions = [(0, -TITLE_SIZE), (0, TITLE_SIZE),\
                  (TITLE_SIZE, 0), (-TITLE_SIZE, 0)]
    ## snake_dir = random.choice(directions)
    snake_dir = (0, 0)

    # Time parameters
    time = 0
    time_step = 160 # 110

    # Food
    food = snake.copy()
    food.center = get_random_position()

    # Read high score
    file = open("highscore.txt", "r")
    highscore = file.read()
    file.close()

    if highscore == "":
        highscore = 0
    else:
        highscore = int(highscore)

    # Main cycle
    game_over = False

    for i in range(len(playlist)):
        q.put(playlist[i])

    pg.mixer.music.load(q.get())
    if default_music:
        pg.mixer.music.play()
    else:
        pg.mixer.music.play(-1)
    
    while not game_over:
        # Refresh rate
        clock.tick(FPS)

        if default_music:
            if not pg.mixer.music.get_busy():
                pg.mixer.music.unload()
                pg.mixer.music.load(q.get())
                pg.mixer.music.play()

        # Event loop
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over = True
                return False
                
                
            # Processing WASD click
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    if not snake_dir == (0, TITLE_SIZE):
                        snake_dir = (0, -TITLE_SIZE)
                if event.key == pg.K_s:
                    if not snake_dir == (0, -TITLE_SIZE):
                        snake_dir = (0, TITLE_SIZE)
                if event.key == pg.K_a:
                    if not snake_dir == (TITLE_SIZE, 0):
                        snake_dir = (-TITLE_SIZE, 0)
                if event.key == pg.K_d:
                    if not snake_dir == (-TITLE_SIZE, 0):
                        snake_dir = (TITLE_SIZE, 0)

                ##snake_dir = last_key

        gameScreen.fill((0, 0, 0))
    

        # Collisions
        snake_collision = pg.Rect.collidelist(snake, segments[:-1]) != -1
        if snake.left < 0 or snake.right > WINDOW or \
        snake.top < 0 or snake.bottom > WINDOW or snake_collision:
##            snake.center, food.center = get_random_position(), get_random_position()
##            length, snake_dir = 1, (0, 0)
##            segments = [snake.copy()]
            pg.mixer.music.stop()
            
            
            gameover_window_render(length - 1, highscore)
            game_over = True
            break
  
        
        # Eat
        if snake.center == food.center:
            food.center = get_random_position()
            length += 1
            if length % 10 == 0:
                time_step -= 5
            
        # Draw food
        pg.draw.rect(gameScreen, (255, 0, 0), food)
                
        # Draw snake
        [pg.draw.rect(gameScreen, (155, 188, 15), segment) \
        for segment in segments]


        # Control
        time_now = pg.time.get_ticks()
        if time_now - time > time_step:
            time = time_now
            snake.move_ip(snake_dir)
            segments.append(snake.copy())
            segments = segments[-length:]
            

        print_score(length - 1)
        string = "Рекорд: " + str(highscore)
        text = score_font.render(string, True, (255, 255, 255))
        t_width, t_hight = score_font.size(string)
        gameScreen.blit(text, [WINDOW - t_width, 0])
        pg.display.update()

    return True
    

def start_menu_render():
    gameScreen.fill((0, 0, 0))
    str = "Funny snake"
    text = title_font.render(str, True, (155, 188, 15))
    t_width, t_hight = menu_font.size(str)
    gameScreen.blit(text, [WINDOW // 2 - t_width // 2,\
                           WINDOW // 2 - t_hight // 2 - 2*t_hight])

    str = "1 - Изменить размер интерфейса"
    text = menu_font.render(str, True, (255, 255, 255))
    t_width, t_hight = menu_font.size(str)
    gameScreen.blit(text, [WINDOW // 2 - t_width // 2,\
                           WINDOW // 2 - t_hight // 2])

    str = "2 - Выбрать режим"
    text = menu_font.render(str, True, (255, 255, 255))
    t_width, t_hight = menu_font.size(str)
    gameScreen.blit(text, [WINDOW // 2 - t_width // 2,\
                           WINDOW // 2 + t_hight // 2])

    str = "SPACE - Старт"
    text = menu_font.render(str, True, (255, 255, 255))
    t_width, t_hight = menu_font.size(str)
    gameScreen.blit(text, [WINDOW // 2 - t_width // 2,\
                           WINDOW // 2 + t_hight // 2 + 2*t_hight])

    pg.display.update()


##    gameScreen.fill((0, 0, 0))
##    str = "Press SPACE to Start"
##    text = menu_font.render(str, True, (255, 255, 255))
##    t_width, t_hight = menu_font.size(str)
##    gameScreen.blit(text, [WINDOW // 2 - t_width // 2,\
##                                     WINDOW // 2 - t_hight // 2])
##    pg.display.update()

def gameover_window_render(cur_score, highscore):
    gameScreen.fill((0, 0, 0))
    str = "Помер"
    text = pomer_font.render(str, True, (255, 0, 0))
    t_width, t_hight = pomer_font.size(str)
    x = WINDOW // 2 - t_width // 2
    y = WINDOW // 2 - t_hight
    gameScreen.blit(text, [x,y])

    if cur_score > highscore:
        str = "Новый рекорд - " + make_highscore_file(cur_score, highscore) + "!"
    else:
        str = "Рекорд - " + make_highscore_file(cur_score, highscore)
    text = menu_font.render(str, True, (255, 255, 255))
    t_width, t_hight = menu_font.size(str)
    x = WINDOW // 2 - t_width // 2
    y = WINDOW // 2 + t_hight
    gameScreen.blit(text, [x,y])
    pg.display.update()

def choose_size():
    gameScreen.fill((0, 0, 0))
    
    str = "Выбор размера интерфейса"
    text = title_font.render(str, True, (255, 255, 255))
    t_width, t_hight = menu_font.size(str)
    gameScreen.blit(text, [WINDOW // 2 - t_width // 2,\
                           WINDOW // 2 - t_hight // 2 - 2*t_hight])

    str = "1 - Стандартный"
    text = menu_font.render(str, True, (255, 255, 255))
    t_width, t_hight = menu_font.size(str)
    gameScreen.blit(text, [WINDOW // 2 - t_width // 2,\
                           WINDOW // 2 - t_hight // 2])

    str = "2 - Мелкий"
    text = menu_font.render(str, True, (255, 255, 255))
    t_width, t_hight = menu_font.size(str)
    gameScreen.blit(text, [WINDOW // 2 - t_width // 2,\
                           WINDOW // 2 + t_hight // 2])
    
    pg.display.update()

    end = False
    while not end:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    end = True
                if event.key == pg.K_2:
                    global TITLE_SIZE
                    TITLE_SIZE = TITLE_SIZE // 2 # Cell size
                    global RANGE
                    RANGE = (TITLE_SIZE // 2, WINDOW - TITLE_SIZE // 2,\
                                TITLE_SIZE)
                    end = True
                if event.key == pg.K_q or event.key == pg.K_ESCAPE:
                    end = True
                

def choose_mode():
    gameScreen.fill((0, 0, 0))
    
    str = "Выбор режима"
    text = title_font.render(str, True, (255, 255, 255))
    t_width, t_hight = menu_font.size(str)
    gameScreen.blit(text, [WINDOW // 2 - t_width // 2,\
                           WINDOW // 2 - t_hight // 2 - 2*t_hight])

    str = "1 - Стандартный"
    text = menu_font.render(str, True, (255, 255, 255))
    t_width, t_hight = menu_font.size(str)
    gameScreen.blit(text, [WINDOW // 2 - t_width // 2,\
                           WINDOW // 2 - t_hight // 2])

    str = "2 - ГОООООООООЛ"
    text = menu_font.render(str, True, (255, 255, 255))
    t_width, t_hight = menu_font.size(str)
    gameScreen.blit(text, [WINDOW // 2 - t_width // 2,\
                           WINDOW // 2 + t_hight // 2])
    
    pg.display.update()

    end = False
    while not end:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    end = True
                if event.key == pg.K_2:
                    global playlist
                    playlist = ['wide_putin.mp3']
                    global default_music
                    default_music = False
                    end = True
                if event.key == pg.K_q or event.key == pg.K_ESCAPE:
                    end = True

def main():
    start_menu_render()
        
    close = False
    while not close:
        
        
        # Event loop
        for event in pg.event.get():
            if event.type == pg.QUIT:
                close = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q or event.key == pg.K_ESCAPE:
                    close = True
                if event.key == pg.K_1:
                    choose_size()
                    start_menu_render()
                if event.key == pg.K_2:
                    choose_mode()
                    start_menu_render()
                if event.key == pg.K_SPACE:
                    res = gameLoop()
                    random.shuffle(playlist)
                    if not res:
                        close = True


    pg.quit()


main()
