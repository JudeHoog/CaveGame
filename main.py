import os
import requests
import json
import pygame
import random

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

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

#Open Weather map key (optional: when run select n for custom weather)
APIKey = ""

def weatherAPI(defultWeather, userLatatude, userLongitude):

    #Cordinates of Staute of Liberty NY
    weatherLatatude = "40.6892"
    weatherLongitude = "-74.0445"

    if defultWeather == 0:
        weatherLatatude = userLatatude
        weatherLongitude = userLongitude

    try:
        weatherResponse = requests.get("https://api.openweathermap.org/data/2.5/weather?lat="+weatherLatatude+"&lon="+weatherLongitude+"&appid="+APIKey+"&units=imperial")
        
    except: 
        print("Connection Issue: Defalting to use no weather")
        gameMain(1, 0, 0)
        currentTemperature = 0
        weatherDescription = ""

    else:
        weatherResponseJSON = weatherResponse.json()

        y = weatherResponseJSON["main"]
        currentTemperature = y["temp"]
        z = weatherResponseJSON["weather"]

        weatherDescription = z[0]["description"]
        
    gameMain(1, str(currentTemperature), str(weatherDescription))
        

def getLoac(userAdress, userState, userZipCode):    
    
    try:
        response = requests.get("https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address="+userAdress+"%2C+"+userState+"%2C+"+userZipCode+"&benchmark=2020&format=json")
    except:
        
        print("Connection Issue: Defalting to use base address")
        
    else:

        dataAPI = response.json()
       
        dataResult = dataAPI['result']
        dataAddressMatches = dataResult['addressMatches']
        dataCordDict = dataAddressMatches[0]
        dataCord = dataCordDict['coordinates']
      
        weatherAPI(0, str(dataCord['x']), str(dataCord['y']))
        
    
def gameMain(useWeather, userWeather, userTempature):

    rain = False
    snow = False
    sun = False

    if useWeather == 1:
        if userWeather == "rain" or "shower rain":

            rain = True
        elif userWeather == "clear sky":
            sun = True
        elif userWeather == "snow":
            snow = True
        else:
            pass
    else:
        pass
    
    pygame.init()

    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Cave Game')
    font = pygame.font.Font(None, 24)
    FPS = 17
    clock = pygame.time.Clock()

    window = pygame.Surface((384, SCREEN_HEIGHT))


    def draw_clouds(screen, cloud_positions):
        clouds = ["     _~",
                  " _~ )_)",
                  "  )_))_)",
                  "  \\_(  )_)",
                  "   ((_)_(",
                  "    (_)"]

        for cloud_position in cloud_positions:
            x, y = cloud_position

            for line in clouds:
                text_surface = font.render(line, True, (255, 255, 255))
                screen.blit(text_surface, (x, y))
                y += font.size(line)[1]

    cloud_positions = [(800, 100), (600, 150), (400, 200)]

    def draw_clearSky(screen):
        sun = [";;;----",
                ";;'-.",
                "| \\"]
        
        x = 0
        y = -2
        for line in sun:
                text_surface = font.render(line, True, (255, 255, 255))
                screen.blit(text_surface, (x, y))
                y += font.size(line)[1]
                
    def draw_rain(screen, rain_positions):

        for rain_position in rain_positions:
            x, y = rain_position
            text_surface = font.render("|", True, (255, 255, 255))
            screen.blit(text_surface, (x, y))

    def draw_snow(screen, rain_positions):

        for rain_position in rain_positions:
            x, y = rain_position
            text_surface = font.render("*", True, (255, 255, 255))
            screen.blit(text_surface, (x, y))

    class Player(pygame.sprite.Sprite):
        def __init__(self, rows, cols, tilesize):
            super().__init__()
            self.image = pygame.Surface((15, 15))
            self.image.fill((200, 20, 20))
            self.random_position(cols, rows, tilesize)

        def random_position(self, cols, rows, tilesize):
            x = random.randint(0, rows-1) * tilesize + tilesize // 2
            y = random.randint(0, cols-1) * tilesize + tilesize // 2
            self.pos = pygame.Vector2(x, y)
            self.rect = self.image.get_rect(center = self.pos)

        def update(self, events, dt):
            pressed = pygame.key.get_pressed()
            move = pygame.Vector2((0, 0))

            # calculate maximum movement and current cell position  
            testdist = dt // 5 + 3
            cellx = self.rect.centerx // tilesize
            celly = self.rect.centery // tilesize
            minx = (self.rect.left-1) // tilesize
            maxx = (self.rect.right+1) // tilesize
            miny = (self.rect.top-1) // tilesize
            maxy = (self.rect.bottom+1) // tilesize

           # test move up
            if minx == maxx and pressed[pygame.K_w]:
                print("y")
                nexty = (self.rect.top-testdist) // tilesize
                if celly == nexty or (nexty >= 0 and not grid[celly][cellx].walls[0]):
                    move += (0, -1)

            # test move right
            elif miny == maxy and pressed[pygame.K_d]:
                nextx = (self.rect.right+testdist) // tilesize
                if cellx == nextx or (nextx < cols and not grid[celly][cellx].walls[1]):
                    move += (1, 0)
                   
            # test move down
            elif minx == maxx and pressed[pygame.K_s]:
                nexty = (self.rect.bottom+testdist) // tilesize
                if celly == nexty or (nexty < rows and not grid[celly][cellx].walls[2]):
                    move += (0, 1)            

            # test move left
            elif miny == maxy and pressed[pygame.K_a]:
                nextx = (self.rect.left-testdist) // tilesize
                if cellx == nextx or (nextx >= 0 and not grid[celly][cellx].walls[3]):
                    move += (-1, 0)
            
            self.pos = self.pos + move*(dt/5)
            self.rect.center = self.pos        

    class Cell():
        def __init__(self, x, y):
            self.rect = pygame.Rect(x * tilesize, y * tilesize, tilesize, tilesize)
            self.walls = [True, True, True, True] # top , right , bottom , left
            self.visited = False
            self.current = False

        def draw(self):
            if self.current:
                pygame.draw.rect(window, (255, 0, 0), self.rect)

            elif self.visited:
                pygame.draw.rect(window, (255, 255, 255), self.rect)
                if self.walls[0]:
                    pygame.draw.line(window, (0, 0, 0, 0), self.rect.topleft, self.rect.topright, 1)
                if self.walls[1]:
                    pygame.draw.line(window, (0, 0, 0, 0), self.rect.topright, self.rect.bottomright, 1)
                if self.walls[2]:
                    pygame.draw.line(window, (0, 0, 0, 0), self.rect.bottomleft, self.rect.bottomright, 1)
                if self.walls[3]:
                    pygame.draw.line(window, (0, 0, 0, 0), self.rect.topleft, self.rect.bottomleft, 1)

    def checkNeighbors(cell):
        i, j = cell.rect.x // tilesize, cell.rect.y // tilesize
        neighbors = []
        for ni, nj in [(i, j-1), (i+1, j), (i, j+1), (i-1, j)]:
            if 0 <= ni < cols and 0 <= nj < rows and not grid[nj][ni].visited:
                neighbors.append(grid[nj][ni])
        return neighbors[random.randrange(0, len(neighbors))] if neighbors else None

    def removeWalls(current_cell,next_cell):
        x = current_cell.rect.x // tilesize - next_cell.rect.x // tilesize
        y = current_cell.rect.y // tilesize - next_cell.rect.y // tilesize
        if x == -1: # right of current
            current_cell.walls[1] = False
            next_cell.walls[3] = False
        elif x == 1: # left of current
            current_cell.walls[3] = False
            next_cell.walls[1] = False
        elif y == -1: # bottom of current
            current_cell.walls[2] = False
            next_cell.walls[0] = False
        elif y == 1: # top of current
            current_cell.walls[0] = False
            next_cell.walls[2] = False

    def new_grid():
        grid = []
        for y in range(rows):
            grid.append([])
            for x in range(cols):
                grid[y].append(Cell(x,y))
        return grid, grid[0][0]

    tilesize = 48
    cols = int(window.get_width() / tilesize)
    rows = int(window.get_height() / tilesize)
    stack = []
    player = Player(cols, rows, tilesize)
    sprites = pygame.sprite.Group()
    sprites.add(player)

    grid, current_cell = new_grid()


    run = True
    play = False

    while run:

        dt = clock.tick(60)

        keys_pressed = {}

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
            
                keys_pressed[event.key] = True
            elif event.type == pygame.KEYUP:
            
                keys_pressed[event.key] = False

        if play == True:
        
            pygame.draw.rect(window, (255, 164, 164), player.rect)
            sprites.update(None, dt)
            sprites.draw(window)

            if pygame.Rect(0, 0, tilesize, tilesize).colliderect(player.rect):
                grid, current_cell = new_grid()
                player.random_position(cols, rows, tilesize)
                window.fill(0)
                play = False

            else:
                current_cell.visited = True
                current_cell.current = True

                next_cell = checkNeighbors(current_cell)
                if next_cell != None:
                    stack.append(current_cell)
                    removeWalls(current_cell,next_cell)
                    current_cell.current = False
                    current_cell = next_cell
                elif len(stack) > 0:
                    current_cell.current = False
                    current_cell = stack.pop()
                else:
                    play = True

                for y in range(rows):
                    for x in range(cols):
                        grid[y][x].draw()

        rain_positions = []
        for i in range(600):
            rain_positions.append((random.randint(0, 800), random.randint(0, 1200)))

        for i in range(len(cloud_positions)):
            x, y = cloud_positions[i]
            cloud_positions[i] = (x - 1, y)

        for i in range(len(rain_positions)):
            x, y = rain_positions[i]
            rain_positions[i] = (x, y + 1)

        if rain == True:
            draw_rain(screen, rain_positions)
            
        if snow == True:
            draw_snow(screen, rain_positions)  

        if sun == True:
            draw_clearSky(screen)

        screen.blit(window, (128, 0))

        pygame.display.flip()

        screen.fill((0, 0, 0))


        clock.tick(FPS)

    print("\nThanks for playing CaveGame!")
    pygame.quit()
    exit()


def weatherInit():

    userWeatherInput = input("Do you want to use the custom weather feature? (y or n): ")

    if userWeatherInput == "y":

        adress = str(input("Enter address(eg. 1 Hacker Way): "))
        state = str(input("Enter State (eg. California): "))
        zipCode = str(input("Enter ZipCode: "))

        getLoac(adress, state, zipCode)

    elif userWeatherInput  == "n":
        
        tmp  = weatherAPI(1, 0, 0)
        gameMain(1, tmp[0], tmp[1])


    else:
        print("***Incorrect input: use lower case y or n to select***")
        weatherInit()

weatherInit()
    

