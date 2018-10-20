import os
def getPath(path):
    WORKING_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(WORKING_DIRECTORY, path)

def run(width, height, fps, scene):
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("QWERTY")
    clock = pygame.time.Clock()
    activeScene = scene
    FULLSCREEN = False
    while activeScene != None:
        pressedKeys = pygame.key.get_pressed()
        #Event filtering - Detects if user wants to close the game, otherwise sends inputs to be handled by scene
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            #Checks if window is being closed or if alt-f4 is pressed (pygame doesn't close on alt-f4 by default)
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressedKeys[pygame.K_LALT] or pressedKeys[pygame.K_RALT]
                if event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True
                if (event.key == pygame.K_RETURN and alt_pressed) or event.key == pygame.K_F11:
                    FULLSCREEN = not FULLSCREEN
                    if FULLSCREEN:
                        pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                    else:
                        pygame.display.set_mode((width, height))
                    activeScene.renderedBack = False
            if quit_attempt:
                activeScene.Terminate()
            else:
                filtered_events.append(event)

        #Call the methods in the active scene
        activeScene.ProcessInput(filtered_events, pressedKeys)
        activeScene.Update()
        activeScene.Render(screen)

        #Check if scene needs to be changed
        activeScene = activeScene.next
        #Update the buffer and tick to the next frame
        pygame.display.flip()
        clock.tick(fps)
        #print ("fps:", clock.get_fps())

#Screen Size
WIDTH = 1280 #704
HEIGHT = 736 #448

LEVELCOUNT = 0
if __name__ == "__main__":
    import pygame
    import Scenes as Scene
    #Change the directory so the terminal is looking at where the file is being run from
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    pygame.init()
    pygame.mouse.set_visible(False)
    #DEBUG: Change start scene here
    title = Scene.TitleScene(WIDTH, HEIGHT)
    run(WIDTH, HEIGHT, 60, title)