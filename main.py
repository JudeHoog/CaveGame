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
import requests
import json
import pygame

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

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
custLoac = input("Do you want to use the custom weather feature? (y or n): ")

def weather(defult):

        lat = "40.6892"
        lon = "-74.0445"

        #dont steal my api key
        response = requests.get("https://api.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+lon+"&appid=5362b9830508ec079bd2d89531909011&units=imperial")

        responseParsed = json.loads(response)

        print(responseParsed)

def getLoac(adress, state, zipCode):
    AddrStr = ""
    response = requests.get("https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address=9001+Conservtion+Ct+Ne%2C+Michigan%2C+49301&benchmark=2020&format=json")
    
    #print(response.json())
    weather(0)

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

#game()

if custLoac == "y":
    adress = str(input("Enter address(eg. 1 Hacker Way): "))
    state = str(input("Enter State (eg. California): "))
    zipCode = str(input("Enter ZipCode: "))
    getLoac(adress, state, zipCode)
elif custLoac == "n":
    weather(1)

