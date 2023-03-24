from math import atan2

# check if pygame is installed and if not, we will install it automatically
try:
    import pygame
except ImportError:
    print("Pygame is not installed: Installing it now...")
    import os
    try:
        os.system("python -m pip install pygame")
    except Exception as e:
        print("Failed to install pygame! Please install it manually with 'python -m pip install pygame'")
        print("Error: " + str(e))
        quit()
    try:
        import pygame
    except ImportError:
        print("Failed to install pygame! Please install it manually with 'python -m pip install pygame'")
        quit()
    print("Pygame installed successfully!")


import pygame

# This value determines the refresh rate of the program. 60 fps should be fine for most cases and is recommended.
TICKRATE = 60

pygame.init()

# screen
WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Controller Test")
clock = pygame.time.Clock()

try:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
except:
    print("No controller found!")
    joystick = None

joystickConnected = True
joystickLastButtonPressed = None

# rumble controller
def rumble(left: float=1, right: float=1, duration: int=100):
    joystick.rumble(left, right, duration)
    #print("Rumble!")

def getAngleOfJoystick(ax1=1, ax2=0):
    rad = atan2(joystick.get_axis(ax1), joystick.get_axis(ax2))
    deg = rad * (180 / 3.14159265358979323846)
    return round(deg, 1) * -1 # invert

while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.JOYBUTTONDOWN:
            rumble()
            joystickLastButtonPressed = event.button
        if event.type == pygame.JOYHATMOTION:
            if event.value == (0, 1) or event.value == (-1, 0):
                rumble(0, 1, 200)
            elif event.value == (0, -1) or event.value == (1, 0):
                rumble(1, 0, 200)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                rumble(1, 1, 5000)

        # check if the window is focused
        if event.type == pygame.ACTIVEEVENT:
            if event.state == 2:
                if event.gain == 0:
                    isWindowFocused = False
                else:
                    isWindowFocused = True
    
    # check for joysticks
    try:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        joystickConnected = True
        #print(joystick.get_name())
        pygame.display.set_caption("Controller Test - Connected")
    except:
        joystickConnected = False
        pygame.display.set_caption("Controller Test - Waiting for controller...")

    if joystickConnected:
        # axis for xbox controller (default axis mapping)
        leftAxis_X = 0
        leftAxis_Y = 1
        rightAxis_X = 2
        rightAxis_Y = 3
        # check for PS3 or PS4 controller and change the right joystick mapping ("Wireless Controller" is bluetooth and the others are USB)
        if joystick.get_name() == "Wireless Controller" or joystick.get_name() == "Sony Interactive Entertainment Wireless Controller" or joystick.get_name() == "Sony Computer Entertainment Wireless Controller" or joystick.get_name() == "Sony PLAYSTATION(R)3 Controller" or joystick.get_name() == "ShanWan PLAYSTATION(R)3 Controller":
            rightAxis_X = 3
            rightAxis_Y = 4
        elif joystick.get_name() == "Xbox One Wired Controller" or joystick.get_name() == "Xbox One Controller":
            rightAxis_X = 3
            rightAxis_Y = 4
        rightJoystickAngle = getAngleOfJoystick(rightAxis_X, rightAxis_Y)
        leftJoystickAngle = getAngleOfJoystick(leftAxis_X, leftAxis_Y)
        if round(joystick.get_axis(leftAxis_X), 1) < 0.2 and round(joystick.get_axis(leftAxis_X), 1) > -0.2 and round(joystick.get_axis(leftAxis_Y), 1) < 0.2 and round(joystick.get_axis(leftAxis_Y), 1) > -0.2:
            leftJoystickAngle = 0
        if round(joystick.get_axis(rightAxis_X), 1) < 0.2 and round(joystick.get_axis(rightAxis_X), 1) > -0.2 and round(joystick.get_axis(rightAxis_Y), 1) < 0.2 and round(joystick.get_axis(rightAxis_Y), 1) > -0.2:
            rightJoystickAngle = 0
    else:
        # if no joystick is connected, set the joystick angles to 0
        rightJoystickAngle = 0
        leftJoystickAngle = 0
    
    screen.fill((0, 0, 0))
    textFont = pygame.font.SysFont("Arial", 18)
    bigWarningFont = pygame.font.SysFont("Arial", 36) # font for reminding user to focus the window

    if joystickConnected:
        screen.blit(textFont.render("Press any button to activate the rumble", True, (255, 255, 255)), (0, 0))

        screen.blit(textFont.render("Joystick Name: " + joystick.get_name(), True, (255, 255, 255)), (0, 25))

        screen.blit(textFont.render("Button Event: " + str(joystickLastButtonPressed), True, (255, 255, 255)), (0, 50))

        # draw both joysticks

        pygame.draw.circle(screen, (255, 255, 255), (WIDTH/2 - 200, HEIGHT/2), 100, 1)
        pygame.draw.circle(screen, (255, 255, 255), (WIDTH/2 - 200, HEIGHT/2), 10, 1)
        pygame.draw.circle(screen, (255, 0, 0),     (WIDTH/2 - 200 + int(joystick.get_axis(leftAxis_X) * 100), HEIGHT/2 + int(joystick.get_axis(leftAxis_Y) * 100)), 10, 1)
        screen.blit(textFont.render(str(leftJoystickAngle), True, (255, 255, 255)), (WIDTH/2 - 220, HEIGHT/2 +110))

        pygame.draw.circle(screen, (255, 255, 255), (WIDTH/2 + 200, HEIGHT/2), 100, 1)
        pygame.draw.circle(screen, (255, 255, 255), (WIDTH/2 + 200, HEIGHT/2), 10, 1)
        pygame.draw.circle(screen, (255, 0, 0),     (WIDTH/2 + 200 + int(joystick.get_axis(rightAxis_X) * 100), HEIGHT/2 + int(joystick.get_axis(rightAxis_Y) * 100)), 10, 1)
        screen.blit(textFont.render(str(rightJoystickAngle), True, (255, 255, 255)), (WIDTH/2 + 180, HEIGHT/2 +110))

        # check that the window is focused
        if not isWindowFocused:
            screen.blit(bigWarningFont.render("Please focus this window!", True, (255, 50, 10)), (WIDTH/2 - 200, HEIGHT/2 - 140))
            screen.blit(textFont.render("(click on it)", True, (255, 50, 10)), (WIDTH/2 - 50, HEIGHT/2 - 100))

    else:
        screen.blit(textFont.render("No controller connected", True, (255, 255, 255)), (0, 0))
        
        # draw both joysticks at default position

        pygame.draw.circle(screen, (255, 255, 255), (WIDTH/2 - 200, HEIGHT/2), 100, 1)
        pygame.draw.circle(screen, (255, 255, 255), (WIDTH/2 - 200, HEIGHT/2), 10, 1)
        pygame.draw.circle(screen, (255, 0, 0),     (WIDTH/2 - 200, HEIGHT/2), 10, 1)
        screen.blit(textFont.render(str(leftJoystickAngle), True, (255, 255, 255)), (WIDTH/2 - 220, HEIGHT/2 +110))

        pygame.draw.circle(screen, (255, 255, 255), (WIDTH/2 + 200, HEIGHT/2), 100, 1)
        pygame.draw.circle(screen, (255, 255, 255), (WIDTH/2 + 200, HEIGHT/2), 10, 1)
        pygame.draw.circle(screen, (255, 0, 0),     (WIDTH/2 + 200, HEIGHT/2), 10, 1)
        screen.blit(textFont.render(str(rightJoystickAngle), True, (255, 255, 255)), (WIDTH/2 + 180, HEIGHT/2 +110))

    pygame.display.update()

    clock.tick(TICKRATE)
        
