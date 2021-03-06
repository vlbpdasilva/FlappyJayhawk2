"""
EECS 448 - "Flappy Jayhawk" -- Project 4
@author Victor Berger, Jesse Yang, Jeromy Tsai, and Cammy Vo
prof: John Gibbons
University of Kansas

Basic controls:
From the menu, press the spacebar to start game. Use the up arrow to control the Jayhawk up.
Hitting one of the moving blocks causes you to lose. Then, the user can press 'c' to restart 
or Escape to close the game.

Sources used:_____________________

Official Pygame documentation: http://www.pygame.org/docs/
Youtube videos available at https://www.youtube.com/playlist?list=PL6gx4Cwl9DGAjkwJocj7vlc_mFU-4wXJq
Pipe image from http://vignette3.wikia.nocookie.net/fantendo/images/0/06/RocketPipes.png/revision/latest?cb=20100430132034
First background obtained from https://peukalo.wordpress.com/tag/super-mario/
Second background image from http://freetems.net/files/2143_t2.png
Third background image from https://kanimate.files.wordpress.com/2015/05/3.jpg
Github repository used for help with Pygame implementations: https://github.com/TimoWilken/flappy-bird-pygame
Pygame clock documentation: http://www.geon.wz.cz/pygame/ref/pygame_time.html
Python documentation regarding classes: https://docs.python.org/2/tutorial/classes.html
Pygame sound effect documentation: http://thepythongamebook.com/en:pygame:step010

"""

#Import
import sys, pygame, time, os
import settings
from random import randint
from Jayhawk import *
from Pipe import *
from Background import *
from database import *

#import powerups
from PowerUpManager import *
from PipeManager import *
  

#Initialization
pygame.init()
settings.init()
database().__init__()

#Initialization of sound tools
#Taken from http://thepythongamebook.com/en:pygame:step010
#All sounds created using http://www.bfxr.net/
pygame.mixer.pre_init(44100, -16, 2, 2048)

#Screen Initializations
pygame.display.set_caption("Flappy Jayhawk")
size = width, height = (600,500)
screen = pygame.display.set_mode(size)

#Color Definitions
black = (0,0,0)
white = (255,255,255)
blue = (0, 0, 255)
red = (255, 0, 0)

#Clock Implementation
clock = pygame.time.Clock()
FPS = 60

#Font Definitions and sizes
smallFont = pygame.font.SysFont("comicsansms", 14)
medFont = pygame.font.SysFont("comicsansms", 25)
largeFont = pygame.font.SysFont("comicsansms", 50)

def load_images():
    """Load all images required by the game and return a dict of them.
    The returned dict has the following keys:
    jayhawk: The image of the Jayhawk bird.
    background: The game's background image.
    pipe: The image of the pipe (a 540px image extending both end-piece and body).
    """

    def load_image(img_file_name):
        """Return the loaded pygame image with the specified file name.
        This function looks for images in the game's images folder
        (./images/).  All images are converted before being returned to
        speed up blitting.
        Arguments:
        img_file_name: The file name (including its extension, e.g.
            '.png') of the required image, without a file path.
        """
        file_name = os.path.join('.', 'images', img_file_name)
        img = pygame.image.load(file_name)
        img.convert()
        return img

    return {'jayhawk': load_image('jayhawk.png'),
            'background': load_image('repeatTest_smw.png'),
            'background2': load_image('background2.png'),
            'background3': load_image('background3.png'),
            'pipe': load_image('pipe.png')
            }

def option_menu(screen, menu, x_pos = 200, y_pos = 250, font = None,
            size = 70, distance = 1.4, fgcolor = (255,255,255),
            cursorcolor = (255,0,0), exitAllowed = True):
    """
    create an option menu with a cursor to allow users to navigate through Options
    """
    pygame.font.init()
    if font == None:
        myfont = pygame.font.Font(None, size)
    else:
        myfont = pygame.font.SysFont(font, size)
    cursorpos = 0
    renderWithChars = False
    for i in menu:
        if renderWithChars == False:
            text =  myfont.render(str(cursorpos + 1)+".  " + i,
                True, fgcolor)
        else:
            text =  myfont.render(chr(char)+".  " + i,
                True, fgcolor)
            char += 1
        textrect = text.get_rect()
        textrect = textrect.move(x_pos, 
                   (size // distance * cursorpos) + y_pos)
        screen.blit(text, textrect)
        pygame.display.update(textrect)
        cursorpos += 1
        if cursorpos == 9:
            renderWithChars = True
            char = 65

    # Draw the ">", the Cursor
    cursorpos = 0
    cursor = myfont.render(">", True, cursorcolor)
    cursorrect = cursor.get_rect()
    cursorrect = cursorrect.move(x_pos - (size // distance),
                 (size // distance * cursorpos) + y_pos)

    # The whole While-loop takes care to show the Cursor, move the
    # Cursor and getting the Keys (1-9 and A-Z) to work...
    ArrowPressed = True
    exitMenu = False
    clock = pygame.time.Clock()
    filler = pygame.Surface.copy(screen)
    fillerrect = filler.get_rect()
    while True:
        clock.tick(30)
        if ArrowPressed == True:
            screen.blit(filler, fillerrect)
            pygame.display.update(cursorrect)
            cursorrect = cursor.get_rect()
            cursorrect = cursorrect.move(x_pos - (size // distance),
                         (size // distance * cursorpos) + y_pos)
            screen.blit(cursor, cursorrect)
            pygame.display.update(cursorrect)
            ArrowPressed = False
        if exitMenu == True:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and exitAllowed == True:
                    if cursorpos == len(menu) - 1:
                        exitMenu = True
                    else:
                        cursorpos = len(menu) - 1; ArrowPressed = True

                if event.key == pygame.K_1:
                    cursorpos = 0; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_2 and len(menu) >= 2:
                    cursorpos = 1; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_3 and len(menu) >= 3:
                    cursorpos = 2; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_4 and len(menu) >= 4:
                    cursorpos = 3; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_5 and len(menu) >= 5:
                    cursorpos = 4; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_6 and len(menu) >= 6:
                    cursorpos = 5; ArrowPressed = True; exitMenu = True
                elif event.key == pygame.K_7 and len(menu) >= 7:
                    cursorpos = 6; ArrowPressed = True; exitMenu = True
                
                elif event.key == pygame.K_UP:
                    ArrowPressed = True
                    if cursorpos == 0:
                        cursorpos = len(menu) - 1
                    else:
                        cursorpos -= 1
                elif event.key == pygame.K_DOWN:
                    ArrowPressed = True
                    if cursorpos == len(menu) - 1:
                        cursorpos = 0
                    else:
                        cursorpos += 1
                elif event.key == pygame.K_KP_ENTER or \
                     event.key == pygame.K_RETURN:
                            exitMenu = True
    
    return cursorpos



def start_menu():
    """Create a start menu that gives the users the title of the game and the creators of the game
    Also gives users the directions to start the game and the directions to play the game.
    Users will stay on the start menu until they press the corresponding key to start the game or press x to exit the game.
    """
    intro = True

    images = load_images();
    #Scrolling background declaration
    back = Background(images['background'], images['background'].get_size(), height)

    screen.fill((255, 231, 181))

    #Draw background
    screen.blit(back.image, back.rect)
    screen.blit(back.image, back.rect2)
    screen.blit(back.image, back.rect3)
    #Make background scroll
    back.scroll()
    
    while intro: 
        # Start menu is being shown
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

        

        message_to_screen("FLAPPY JAYHAWK",
                            blue,
                            -100,
                            "large")
        message_to_screen("By: Jeromy Tsai, Cammy Vo, Jesse Yang, Victor Berger",
                            blue,
                            -20,
                            "small")
        pygame.display.update()
       
        
        choose = option_menu(screen, [
                        'Start Game',
                        'Options',
                        'Instructions',
                        'Show Highscore',
                        'Quit Game'], 200,250,None,32,1.4,red,red)

        if choose == 0:
            print "You choose 'Start Game'."
            gameLoop()
            intro = False
        elif choose == 1:
            print "You choose 'Options'."
            option_screen()
            intro = False
        elif choose == 2:
            print "You choose 'Instructions'."
            instruction()
            intro = False
        elif choose == 3:
            print "You choose 'Show Highscore'."
            high_score()
            intro == False
        elif choose == 4:
            print "You choose 'Quit Game'."
            pygame.quit()

        
        clock.tick(FPS)

def option_screen():
    """
    Gives users ability to turn on/off sound and PowerUps"""
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
    images = load_images();
    #Scrolling background declaration
    back = Background(images['background'], images['background'].get_size(), height)

    screen.fill((255, 231, 181))
    #Draw background
    screen.blit(back.image, back.rect)
    screen.blit(back.image, back.rect2)
    screen.blit(back.image, back.rect3)
    #Make background scroll
    back.scroll()

    message_to_screen("Options",
                        blue,
                        -100,
                        "large")

    pygame.display.update()
    pygame.time.delay(7)

    choose = option_menu(screen, [
                    'Sound',
                    'PowerUps',
                    'Back'], 250, 200, None, 32,1.4,blue,red)
    if choose == 0:
        print "Sound"
        sound_menu()
    elif choose == 1:
        powerup_menu()
    elif choose == 2:
        start_menu()

def sound_menu():
    """Gives users ability to turn on off sound"""
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
    images = load_images();
    #Scrolling background declaration
    back = Background(images['background'], images['background'].get_size(), height)

    screen.fill((255, 231, 181))
    #Draw background
    screen.blit(back.image, back.rect)
    screen.blit(back.image, back.rect2)
    screen.blit(back.image, back.rect3)
    #Make background scroll
    back.scroll()

    message_to_screen("Sound",
                        blue,
                        -100,
                        "large")

    pygame.display.update()
    pygame.time.delay(7)

    choose = option_menu(screen, [
                    'ON',
                    'OFF',
                    'Back'], 250, 200, None, 32,1.4,blue,red)
    if choose == 0:
        settings.sound_toggle = True
        option_screen()
    elif choose == 1:
        settings.sound_toggle = False
        option_screen()
    elif choose == 2:
        option_screen()

def powerup_menu():
    """Turn on/off powerups"""
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
    images = load_images();
    #Scrolling background declaration
    back = Background(images['background'], images['background'].get_size(), height)

    screen.fill((255, 231, 181))
    #Draw background
    screen.blit(back.image, back.rect)
    screen.blit(back.image, back.rect2)
    screen.blit(back.image, back.rect3)
    #Make background scroll
    back.scroll()

    message_to_screen("PowerUps",
                        blue,
                        -100,
                        "large")

    pygame.display.update()
    pygame.time.delay(7)

    choose = option_menu(screen, [
                    'ON',
                    'OFF',
                    'Back'], 250, 200, None, 32,1.4,blue,red)
    if choose == 0:
        settings.powerup_toggle = True
        option_screen()
    elif choose == 1:
        settings.powerup_toggle = False
        option_screen()
    elif choose == 2:
        option_screen()

def instruction():
    """
    Gives users instructions for the game
    """
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
    images = load_images();
    #Scrolling background declaration
    back = Background(images['background'], images['background'].get_size(), height)

    screen.fill((255, 231, 181))
    #Draw background
    screen.blit(back.image, back.rect)
    screen.blit(back.image, back.rect2)
    screen.blit(back.image, back.rect3)
    #Make background scroll
    back.scroll()
    message_to_screen("Press the up arrow key to make the Jayhawk jump upward",
                    blue,
                    -50,
                    "medium")
    message_to_screen("Collect power ups for a better chance of survival",
                    blue,
                    0,
                    "medium")
    message_to_screen("Avoid evil pipes at all costs!!",
                    blue,
                    50,
                    "medium")
    pygame.display.update()
    pygame.time.delay(7)

    choose = option_menu(screen, [
                    'Back'], 250, 400, None, 32,1.4,blue,red)
    if choose == 0:
        print "Back"
        start_menu()

def high_score():
    """
    Show high score
    """
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
    images = load_images();
    #Scrolling background declaration
    back = Background(images['background'], images['background'].get_size(), height)

    screen.fill((255, 231, 181))
    #Draw background
    screen.blit(back.image, back.rect)
    screen.blit(back.image, back.rect2)
    screen.blit(back.image, back.rect3)
    #Make background scroll
    back.scroll()

    message_to_screen("High Score",
                        blue,
                        -100,
                        "large")

    rows = database().printTable()
    for index,row in enumerate(rows):    
        message_to_screen(str(row[0]),
                            blue,
                            -50 + index * 20,
                            "medium")
        if(index > 7):
            break

    pygame.display.update()
    clock.tick(FPS)

    choose = option_menu(screen, [
                    'Back'], 250, 400, None, 32,1.4,blue,red)
    if choose == 0:
        print "Back"
        start_menu()

def game_over():
    """
    Creates the game over screen that users will see when they jayhawk touches a pipe, causing the player to lose.
    """

    while 1:
        message_to_screen("Game Over",
                            blue,
                            0,
                            "large")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
                quit()


def text_objects(text, color, size):
    """
    Creates text objects with corresponding sizes. 
    Can expand to a greater range of font size by adding more to this list.
    """
    if size == "small":
        textSurface = smallFont.render(text, True, color)
    elif size == "medium":
        textSurface = medFont.render(text, True, color)
    elif size == "large":
        textSurface = largeFont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace=0, size="small"):
    """
    Creates the message that is displayed on the screen to users. 
    Will be centered and msg, color, size can be changed
    """
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((width/2),(height/2)+y_displace)
    screen.blit(textSurf,textRect)

def difficulty_change(difficulty):
    if(difficulty == 1):
        Jayhawk.gravity_accel = 1
        settings.gravity_accel = 1
        Pipe.GAP = 200
    elif(difficulty == 2):
        Jayhawk.gravity_accel = 2
        settings.gravity_accel = 2
        Pipe.GAP = 150
    elif(difficulty == 3):
        Jayhawk.gravity_accel = 3
        settings.gravity_accel = 3
        Pipe.GAP = 125
        
def gameLoop():
    """
    Runs the game loop until users lose by allowing the jayhawk to collide with the pipes.
    When game over the game will show the game over screen and give the users the option to play again.
    """
    gameOver = False
    gameExit = False
    
    images = load_images();
    
    #Initial difficulty setting
    difficulty_change(1)

    #Scrolling background declaration
    back = Background(images['background'], images['background'].get_size(), height)

    #pipeManager = PipeManager(images['pipe'])
    settings.pipeManager = PipeManager(images['pipe'])
    pipeManager = settings.pipeManager
    #Definition of the jayhawk object and its corresponding rect
    settings.jayhawk = Jayhawk(80,200,(60,60),images['jayhawk'])
    jayhawk = settings.jayhawk

    #Rect declaration of screen
    screenrect = screen.get_rect()

    #Initial difficulty setting
    difficulty = 1;    

    #Screen fill color variable
    fill = (255, 231, 181);

    #initialize score
    score = 0

    powerupManager = PowerUpManager()

    #Load game sounds
    try:
        jump = pygame.mixer.Sound(os.path.join('Sounds','Jump.ogg'))  #load sound
        fail = pygame.mixer.Sound(os.path.join('Sounds','Fail.ogg'))  #load sound
    except:
        raise UserWarning, "could not load or play soundfiles in 'Sounds' folder"
    
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                pygame.quit()
                quit()
                sys.exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:   
                    # listens for ESCAPE key to close the game
                    gameExit = True
                    pygame.quit()
                    sys.exit
                if ((event.key == pygame.K_UP) or (event.key == pygame.K_w) or (event.key == pygame.K_SPACE)):
                    jayhawk.jump()
                    if(settings.sound_toggle):
                        jump.play();
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:# listens for both "1" keys on keyboard
                    if(Jayhawk.gravity_accel != 1):
                        difficulty_change(1)
                        back = Background(images['background'], images['background'].get_size(), height);
                        fill = (255, 231, 181);
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    if(Jayhawk.gravity_accel != 2):
                        difficulty_change(2)
                        ### background image from http://freetems.net/files/2143_t2.png
                        back = Background(images['background2'], images['background2'].get_size(), height);
                        fill = (17, 131, 255);
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    if(Jayhawk.gravity_accel != 3):
                        difficulty_change(3)
                        ### background image from https://kanimate.files.wordpress.com/2015/05/3.jpg
                        back = Background(images['background3'], images['background3'].get_size(), height);           

        jayhawk.updatePosition()
        
        #Keeps the Jayhawk in screen for testing
        jayhawk.clamp()        

        screen.fill(fill)

        #Draw background
        screen.blit(back.image, back.rect)
        screen.blit(back.image, back.rect2)
        screen.blit(back.image, back.rect3)
 
        if(settings.powerup_toggle):
            powerupManager.draw_powerups()
            powerupManager.spawn_management()
            powerupManager.obtained_management()
        
        #Make background scroll
        back.scroll()

        pipeManager.draw_pipes(1)
        pipeManager.spawn_management()
        if(pipeManager.score(jayhawk.rect)):
            score = score + settings.gravity_accel
            
        message_to_screen(str(score),
			blue,
			-200,
			"large")
            
        if(pipeManager.collision(jayhawk.rect)):
            gameOver = True
            if(settings.sound_toggle):
                fail.play()
        
        #Draw Jayhawk
        screen.blit(jayhawk.image, jayhawk.rect)

        if(jayhawk.grounded()):
            gameOver = True
            if(settings.sound_toggle):
                fail.play()


        scoreAdded = False 
        while gameOver == True:
                       
            screen.fill(fill)
            #Draw background	
            screen.blit(back.image, back.rect)
            screen.blit(back.image, back.rect2)
            screen.blit(back.image, back.rect3)		           	

            #Draw final pipe location
            pipeManager.draw_pipes(0)
		
            #Draw Jayhawk
            jayhawk.updatePosition()
            jayhawk.clamp()
            screen.blit(jayhawk.image, jayhawk.rect)
            
            
            #Draw message
            message_to_screen(str(score),
                            blue,
                            -200,
                            "large")
            if(not scoreAdded):
                database().addScore(score)		
                scoreAdded = True
            message_to_screen("Game Over",
                            blue,
                            -50,
                            "large")		     
            message_to_screen("Press c to go to start screen",	
                            blue,		                            
                            50,		                             
                            "small")	
            message_to_screen("Press space to play again",  
                            blue,                                   
                            80,                                  
                            "small")    
                          
            pygame.display.update()
            clock.tick(FPS)
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            gameOver = False
                            gameExit = True
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_c:
                                    start_menu()
                            if event.key == pygame.K_SPACE:
                                    gameLoop()
                            if event.key == pygame.K_ESCAPE:
                                    gameExit = True
                                    pygame.quit()
                                    sys.exit
                                        
                        
        
        #Updates screen and implements delay
        pygame.display.update()
        pygame.display.flip()
        clock.tick(settings.FPS)

def main():
    """
    The application's entry point. Calls "start_menu" and "gameLoop" functions
    """
    gameExit = False
    start_menu()
    #gameLoop()
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
    pygame.quit()
    quit()
    sys.exit
    
    
"""
Starts application by calling main function
"""
if __name__ == '__main__':
    main()
