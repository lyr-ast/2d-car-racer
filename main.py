import pygame
from random import choice

pygame.init()
screen = pygame.display.set_mode((700, 730))
pygame.display.set_caption("2D car racer")
clock = pygame.time.Clock()

pygame.mixer.music.load("music/main_menu.mp3")
pygame.mixer.music.play()

font = pygame.font.Font("Assets/mfont.otf",  35)

home = pygame.image.load("Assets/splashscreen.png")
road = pygame.image.load("Assets/road.png")
grass = pygame.image.load("Assets/grass.jpg")
car = pygame.image.load("Assets/car.png")
dead = pygame.image.load("Assets/gameover.png")

o1 = pygame.image.load("Assets/o1.png").convert_alpha()
o2 = pygame.image.load("Assets/o2.png").convert_alpha()
o3 = pygame.image.load("Assets/o3.png").convert_alpha()
o4 = pygame.image.load("Assets/o4.png").convert_alpha()
o5 = pygame.image.load("Assets/o5.png").convert_alpha()

car = pygame.transform.scale(car, (57.5, 128.25)).convert_alpha()   
grass = pygame.transform.scale(grass, (700, 735)).convert()
road = pygame.transform.scale(road, (477, 500)).convert()
dead = pygame.transform.scale(dead, (700, 730)).convert()
home = pygame.transform.scale(home, (700, 730)).convert()

screen.blit(home, (0,0))

scroll = 0

lane_x = (375, 475, 275, 175)

left = False 
right = False

score = 0

car_r = car.get_rect(topleft = (375, 400))

obj_list = []

spawn_obj_event = pygame.USEREVENT                #timer for spawning obstacles
pygame.time.set_timer(spawn_obj_event, 500)  

score_event = pygame.USEREVENT + 1                #timer for score
pygame.time.set_timer(score_event, 2000)

running = True
maingame = False
gameend = False

def obj_movement(obj):                          #spawns, moves and removes obstacles
    if obj:
        for i in obj:
            i[1].y += 8
            obj = [o for o in obj if o[1].y < 700]
            screen.blit(i[0] ,i[1])
        return obj
    else:
        return []

def collisions(car, obj):                       #checks for collision between car and the obstacles
    if not gameend:
        for o in obj:
            if car.colliderect(o):
                return True
    return False

def display_score(x, y, color):                  #displays score    
    score_text = font.render(f"SCORE: {score}", True, color)
    screen.blit(score_text, (x, y))

def spawn_obj():                                  #chooses obstacles to spawn
    ox = choice(lane_x)
    o1_r = o1.get_rect(topleft = (ox, -200))  
    o2_r = o2.get_rect(topleft = (ox, -200))
    o3_r = o3.get_rect(topleft = (ox, -200))
    o4_r = o4.get_rect(topleft = (ox, -200))
    o5_r = o5.get_rect(topleft = (ox, -200))
    ob_choice = choice([(o1, o1_r), (o2, o2_r), (o3, o3_r), (o4, o4_r), (o5, o5_r)])
    obj_list.append(ob_choice)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == spawn_obj_event and maingame:  #spawns obstacles
            spawn_obj()

        if event.type == score_event and maingame:
            score += 1

        if event.type == pygame.KEYDOWN:
                            
            if event.key == pygame.K_ESCAPE:                  #exits the game when esc is pressed
                    running = False
                    
            if event.key == pygame.K_RETURN:
                
                if not maingame and not gameend:
                    maingame = True                             #starts the music and main game from the mainmenu
                    pygame.mixer.music.fadeout(200)
                    pygame.mixer.music.load("music/game.mp3")
                    pygame.mixer.music.play()
                    pygame.mixer.music.set_volume(.6) 
                    
                if gameend:                                         #relaunches the game after it ends and resets the obstacles and car
                    gameend = False
                    maingame = True
                    pygame.mixer.music.play()
                    score = 0
                    
            if event.key == pygame.K_LEFT:
                left = True

            if event.key == pygame.K_RIGHT:
                right = True
    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left = False

            if event.key == pygame.K_RIGHT:
                right = False

    if maingame:
        screen.blit(grass, (0, 0))

        for i in range(-1, 2):                          #scrolls the road
            screen.blit(road, (111.5, 500*i + scroll))
        scroll += 7

        if scroll > 500:  #checks if the road is out of screen 
            scroll = 0

        screen.blit(car, car_r)

        if left:          #moves the car left or right
            car_r.x -= 4
        if right:
            car_r.x +=4
    
        if collisions(car_r, [o[1] for o in obj_list]):          #if the collision function returns True it ends the game
            maingame = False
            gameend = True

        if car_r.collidepoint(577, 450) or car_r.collidepoint(116, 450):      #checks if car goes out of the road
            gameend = True
            maingame = False

        obj_list = obj_movement(obj_list)
        display_score(5, 10, "lightblue")


    if gameend:                     #shows the game over screen, resets cars, displays score
        screen.blit(dead, (0, 0))
        car_r.x = 375
        obj_list = []
        display_score(260, 280, "purple")
        pygame.mixer.music.stop()

    pygame.display.update()
    clock.tick(60)

