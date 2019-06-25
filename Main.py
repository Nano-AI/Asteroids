from Rocket import*
from Asteroid import*
import sys, pygame, random, pandas as pd
from pygame.locals import *

pygame.init()
screen_info = pygame.display.Info()

size = (width, height) = (int(screen_info.current_w * 0.5), int(screen_info.current_h * 0.5))

screen = pygame.display.set_model(size)
clock = pygame.time.Clock()
color = (0,0,0)

screen.fill(color)

df = pd.read_csv('game_info.csv')

asteroids = pygame.sprite.Group()
numLevel = df['LevelNum'].max()
level = df['LevelNum'].min()
levelData = df.iloc[level] #level is 0, and the 'first' number in LevelNum is equal to this
asteroidCount = levelData['AsteroidCount'] #the one next to 0 in asteroid count

player = ((levelData['PlayerX'], levelData['PlayerY']))

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
    while True:
        screen.fill(color)
        screen.blit(text, text_rect)
        pygame.display.flip()