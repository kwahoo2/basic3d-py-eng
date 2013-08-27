import pygame

def main():

    xw = 800
    yw = 600
    screen = pygame.display.set_mode((xw, yw))
    
    running = True
    
    while running:
        for event in pygame.event.get(): #przerwanie petli
            if event.type == pygame.QUIT:
                running = False

main()
