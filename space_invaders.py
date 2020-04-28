


import pygame
from time import perf_counter, sleep
import gamebox
import random
camera = gamebox.Camera(800, 600)
master_timer = 0


def draw_ship():
    global ship
    global pics
    global ships
    if len(ships) > 0:
        for i in ships:
            ships.remove(i)
    if len(ships) == 0:
        ship = gamebox.from_image(400, 300,pics[1])
        ship.scale_by(.06)
        ships.append(ship)

def draw_heart():
    global all_hearts
    all_hearts = []
    heart = gamebox.from_image(50,50,'heart.png')
    heart.scale_by(.05)
    heart2 = gamebox.from_image(100,50,'heart.png')
    heart2.scale_by(.05)
    all_hearts.append(heart)
    all_hearts.append(heart2)
            

def all_sprites_draw():
    global all_sprites
    global asteroids
    global all_bullets
    global ammo
    global enemies_onscreen
    camera.clear(color='black')
    for l in backgrounds:
        camera.draw(l)
    for i in all_sprites:
        camera.draw(i)
    for b in asteroids:
        if b.right < 800 and b.bottom < 600:
            b.move_speed()
            camera.draw(b)
        else:
            asteroids.remove(b)
            enemies_onscreen -= 1
    for e in all_hearts:
        camera.draw(e)
    for f in ships:
        camera.draw(f)
    for r in texts:
        camera.draw(r)
    camera.display()

def check_highscore():
    global timer
    global master_timer
    file = open('best_times.txt', 'a')
    file.write(str("   new score   "+str(timer+master_timer)))
    file.close()
    master_timer = 0

    end_game()

def end_game():
    global ships
    global game_over
    for b in ships:
        ships.remove(b)
    camera.clear(color='black')
    background = gamebox.from_image(0,0,'space.png')
    background.scale_by(2.50)
    text = gamebox.from_text(400, 105, 'GAME OVER \n Press Enter To Restart',fontname='font', fontsize=36, color="red")
    camera.draw(text)
    camera.display()
    sleep(10)
    begin_game()
    
        
    
    
def new_game():
    global game_over
    print('new')
    text = gamebox.from_text(400, 105, 'ASTEROIDS',fontname='font', fontsize=36, color="red")
    text2 = gamebox.from_text(450, 105, 'game controls:left,right,up,down',fontname='font', fontsize=36, color="red")
    camera.draw(text)
    camera.draw(text2)
    camera.diplay()


def draw_background():
    global backgrounds
    background = gamebox.from_image(0,0,'space.png')
    background.scale_by(2.5)
    backgrounds.append(background)

def draw_text():
    global texts
    global timer
    text = gamebox.from_text(400, 105, str(timer),fontname='font', fontsize=36, color="red")
    texts.append(text)
    
    
def begin_game():
    global game_over
    global all_sprites
    global all_hearts
    global ships
    global t1_start
    global lives
    global hearts
    global timer
    global ship_moving
    global pics
    global pic_counter
    global backgrounds
    global texts
    global asteroids
    global enemies_onscreen
    global enemy_count
    global enemy_vert
    global traveling_vert
    global timer_counter
    global level_up
    level_up = False
    timer_counter = True
    traveling_vert = False
    enemy_vert = True
    enemy_count = 7
    enemies_onscreen = 0
    asteroids = []
    texts = []
    backgrounds = []
    game_over = False   
    all_sprites = []
    all_hearts = []
    ships = []
    t1_start = perf_counter()
    lives = 2
    hearts = 0
    timer = 0
    ship_moving = False
    pics = ['spaceship_moving.png','Spaceship_all.png']
    pic_counter = 0

    draw_background()
    draw_text()
    draw_ship()
    draw_heart()
    
begin_game()

def tick(keys):
    global ship_moving
    global traveling_vert
    global asteroids
    global enemies_onscreen
    global ammo
    global lives
    global game_over
    if lives > -1:
        add_enemies()
        populate_enemy_list()
    if len(asteroids) > 0:
        check_collision()
    if pygame.K_RIGHT in keys:
        if ship.right < 800:
            ship_moving = True
            ship.move(5,0)
    if pygame.K_LEFT in keys:
        if ship.left > 0:
            ship_moving = True
            ship.move(-5,0)
    if pygame.K_UP in keys:
        if ship.top > 0:
            ship_moving = True
            ship.move(0,-5)
    if pygame.K_DOWN in keys:
        if ship.bottom < 600:
            ship_moving = True
            ship.move(0,5)
    
    if ship_moving == True:
        ship.image = pics[0]
        ship_moving = False
    else:
        ship.image = pics[1]
        
        
    if camera.mouseclick: #true if some mouse button is being pressed
        ship.center = camera.mouse # the current mouse position

    all_sprites_draw()
       
def populate_enemy_list():
    global asteroids
    global enemies_onscreen 
    global enemy_count 
    global enemy_vert
    create = enemy_count - enemies_onscreen
    for i in range(create):
        print('for')
        size = random.randint(8,35)
        x = random.randint(50,750)
        y = random.randint(50,550)
        a_speed = random.randint(4,10)
        if enemy_vert == True:
            enemy_vert = False
            enemies_onscreen += 1
            asteroid = gamebox.from_color(y, 0, "brown", size, size)
            asteroid.speedy = a_speed
            asteroids.append(asteroid)
        else :
            enemy_vert = True
            enemies_onscreen += 1
            asteroid = gamebox.from_color(0, x, "brown", size, size) 
            asteroid.speedx = a_speed
            asteroids.append(asteroid)

def add_enemies():
    global timer
    global t1_start
    global enemy_count
    global text
    global texts
    global timer_counter
    global level_up
    new_time = perf_counter()
    timer = int(new_time-t1_start)
    for text in texts:
        texts.remove(text)
    text = gamebox.from_text(400, 105, str(timer),fontname='font', fontsize=36, color="red") 
    texts.append(text)
    camera.draw(text)
    if timer == 15 and timer_counter== True:
        timer_counter = False
        enemy_count += 2 
    if timer == 30and timer_counter == False:
        timer_counter = True
        enemy_count += 2
    if timer == 45 and timer_counter == True:
        timer_counter = False
        enemy_count += 2
    if timer == 50 and timer_counter == False:
        timer_counter = True
        level_up = True
        enemy_count += 4
    if timer == 60 and level_up == True:
        next_level()
        
def next_level():
   global t1_start
   global timer
   global master_timer
   global level_up
   level_up = False
   text = gamebox.from_text(400, 105, "next level",fontname='font', fontsize=36, color="red") 
   camera.draw(text)
   camera.display()
   sleep(10)
   t1_start = perf_counter()
   timer = 0
   master_timer += 120

def check_collision():
    global ship
    global asteroids
    global t1_start
    global lives
    global enemies_onscreen
    global game_over
    for i in asteroids:
        for g in ships:
            if i.touches(g):
                if len(asteroids) > 0:
                    asteroids.remove(i)
                ships.remove(g)
                ship = gamebox.from_image(ship.x, ship.y,'explosion.png')
                ships.append(ship)
                camera.draw(ship)
                asteroids = []
                enemies_onscreen = 0
                for d in all_hearts:
                    all_hearts.remove(d)
                    break
                camera.display()
                sleep(2)
                t1_start += 3
                if lives > 0:
                    lives -= 1
                    draw_ship()
                else:
                    print('hit')
                    lives -= 1
                    game_over = True
                    check_highscore()


running = True



while running:

    #game loop, ass long as your game is running

    #this loop will cycle through with every frame

    

    

    for event in pygame.event.get():

        ###this is for all your keypress handling,checked per loop###

        if event.type == pygame.QUIT:

            running = False

            pygame.quit()

            exit()



    #screen.fill(0,0,0)



    #screen.blit

    #all sprite.draw



    #pygame.display.update()

    #pygame.display.flip()
    gamebox.timer_loop(30, tick)




pygame.quit()
