from Rocket import*
from Asteroid import*
import sys, pygame, random, pandas as pd
from pygame.locals import *

pygame.init()
screen_info = pygame.display.Info()
deaths = -1
size = (width, height) = (int(screen_info.current_w * 0.5), int(screen_info.current_h * 0.5))

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
color = (0,0,0)

screen.fill(color)

df = pd.read_csv('game_info.csv')

asteroids = pygame.sprite.Group()
numLevel = df['LevelNum'].max()
level = df['LevelNum'].min()
levelData = df.iloc[level] #level is 0, and the 'first' number in LevelNum is equal to this
asteroidCount = levelData['AsteroidCount'] #the one next to 0 in asteroid count

player = Ship((levelData['PlayerX'], levelData['PlayerY']))

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
    font = pygame.font.SysFont(None, 70)
    text = font.render("You have Escaped", True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (width/2, height/2)
    pygame.mixer.music.stop()
    pygame.mixer.music.load('Win.mp3')
    pygame.mixer.music.play(0)
    while True:
        screen.fill(color)
        screen.blit(text, text_rect)
        pygame.display.flip()

def main():
    global level, player, asteroids, numLevels
    while level <= numLevel:
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

pygame.mixer.music.load('Music.mp3')
pygame.mixer.music.play(0)
if __name__ == '__main__':
    main()