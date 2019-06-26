from Rocket import*
from Asteroid import*
import sys, pygame, random, pandas as pd
from pygame.locals import *
import matplotlib.pyplot as plt
import matplotlib
millsec = 0
min = 0

pygame.init()
screen_info = pygame.display.Info()
deaths = -1
size = (width, height) = (int(screen_info.current_w * 1), int(screen_info.current_h * 1))

screen = pygame.display.set_mode(size)
color = (0,0,0)

screen.fill(color)

df = pd.read_csv('game_info.csv')

asteroids = pygame.sprite.Group()
numLevel = df['LevelNum'].max()
level = df['LevelNum'].min()
levelData = df.iloc[level] #level is 0, and the 'first' number in LevelNum is equal to this
asteroidCount = levelData['AsteroidCount'] #the one next to 0 in asteroid count

player = Ship((levelData['PlayerX'], levelData['PlayerY']))

clock = pygame.time.Clock()

sec = 0

times = []

def init():
    global asteroidCount, asteroids, levelData
    levelData = df.iloc[level]
    player.reset((levelData['PlayerX'], levelData['PlayerY']))
    asteroids.empty()
    asteroidCount = levelData['AsteroidCount']
    for i in range(asteroidCount):
        asteroids.add(Asteroid((random.randint(50, width-50), #X-Axis
                                random.randint(50, height-50)), #Y-Axis
                                random.randint(15, 60))) #Size

def win():
    global sec, min, millsec, numLevel
    font = pygame.font.SysFont(None, 70)
    text = font.render("You have Escaped", True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (width/2, height/2)
    pygame.mixer.music.stop()
    pygame.mixer.music.load('Win.mp3')
    pygame.mixer.music.play(0)
    print(millsec)
    print(times)
    plt.ylabel('Time')
    plt.xlabel('Round')

    plt.plot(times)

    plt.show()
    while True:
        screen.fill(color)
        screen.blit(text, text_rect)
        pygame.display.flip()


def main():
    global level, player, asteroids, numLevels, clock, millsec, event, times, sec, min
    while level <= numLevel:
        millsec += clock.tick_busy_loop(60)
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.speed[0] = 10
                if event.key == pygame.K_LEFT:
                    player.speed[0] = -10
                if event.key == pygame.K_UP:
                    player.speed[1] = -10
                if event.key == pygame.K_DOWN:
                    player.speed[1] = 10
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player.speed[0] = 0
                if event.key == pygame.K_LEFT:
                    player.speed[0] = 0
                if event.key == pygame.K_UP:
                    player.speed[1] = 0
                if event.key == pygame.K_DOWN:
                    player.speed[1] = 0

        screen.fill(color)
        player.update() #DOES NOT WORK
        asteroids.update() #WORKS
        gets_hit = pygame.sprite.spritecollide(player, asteroids, False)
        asteroids.draw(screen)
        screen.blit(player.image, player.rect)
        pygame.display.flip()

        if player.checkReset(width):
            if level == numLevel:
                break
            else:
                while millsec >= 1000:
                    if millsec >= 1000:
                        sec += 1
                        millsec -= 1000
                        '''
                while sec >= 60:
                    if sec > 60:
                        min += 1
                        sec -= 60'''

                times.append(str(sec) + "." + str(millsec))
                #times.append(str(min)+"."+str(sec)+"."+str(millsec))

                millsec = 0
                level += 1
                init()
        elif gets_hit:
            global deaths
            deaths += 1
            '''
            pygame.mixer.music.load("Failed.mp3")
            pygame.mixer.music.play()
            #MUSIC CODE
            '''
            player.reset((levelData['PlayerX'], levelData['PlayerY']))
    win()

clock = pygame.time.Clock()
pygame.mixer.music.load('Music.mp3')
pygame.mixer.music.play(0)
if __name__ == '__main__':
    main()
