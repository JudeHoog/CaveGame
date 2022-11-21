"""
TODO
Use https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.pdf for zip code to lat long for weather API
Build Map generation / story generation
User input for location

Optional
Color terminal
ASCII art anamations
music
"""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import requests
 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (105,105,105)
 
print("""
   (                     (                           
   )\      )   )      (  )\ )       )     )      (   
 (((_)  ( /(  /((    ))\(()/(    ( /(    (      ))\  
 )\___  )(_))(_))\  /((_)/(_))_  )(_))   )\  ' /((_) 
((/ __|((_)_ _)((_)(_)) (_)) __|((_)_  _((_)) (_))   
 | (__ / _` |\ V / / -_)  | (_ |/ _` || '  \  / -_)  
  \___|\__,_| \_/  \___|   \___|\__,_||_|_|_| \___|  
""")

print("Welcome to CaveGame!")
custLoac = input("Do you want to use the custom weather feature? (y or n)")
if custLoac == "y":
    return
elif == "n":
    weather(1)

def getLoac():
    pass

def weather(defult):

        if defult == 1:
            lat = 40.6892
            lon = 40.6892

        #dont steal my api key
        response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat=43.033138&lon=-85.460312&appid=5362b9830508ec079bd2d89531909011&units=imperialkey 5362b9830508ec079bd2d89531909011")

        print(response.json())

weather()

def game():

    pygame.init()
     
    size = (700, 500)
    screen = pygame.display.set_mode(size)
     
    pygame.display.set_caption("CaveGame")

    done = False
     
    clock = pygame.time.Clock()

    screen.fill(GREY)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        pygame.draw.rect(screen, WHITE, pygame.Rect(30, 30, 60, 60))
    
        pygame.display.flip()
    
        clock.tick(60)
     
    pygame.quit()

game()
