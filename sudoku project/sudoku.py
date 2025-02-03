import pygame
import os
from grid import Grid

#setting the window position relative to the screen upper left corner
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (200,70)

#create the window surface and set the window caption
surface = pygame.display.set_mode((1200,700)) #width,height for disaply
pygame.display.set_caption('Sudoku')

pygame.font.init()
game_font = pygame.font.SysFont('Comnic Sans MS', 50)
game_font2 = pygame.font.SysFont("Comic Sans MS",25) 


#creating instances for grid class
grid = Grid(pygame, game_font)
running = True

#he game loop
while running:
    
    #check for input events(    #it will happen only when i click  )
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.win:
            if pygame.mouse.get_pressed()[0]: # ONLY CHECK FOR LEFT MOUSE BUTTON
                pos = pygame.mouse.get_pos() # here it will give the pixel values of the sub-grid pixel values
                #print(pos)
                grid.get_mouse_click(pos[0],pos[1]) 
                
        if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_SPACE and grid.win:
                grid.restart()
           elif event.key == pygame.K_SPACE and (event.mod & pygame.KMOD_CTRL):  # Check for Ctrl + Space
                grid.fill_all(surface)
      
                                                     
                
    #clear the window surface to blank
    surface.fill((0,0,0))  
    
    #draw the grid here
    grid.draw_all(pygame,surface)
    
    if grid.win:
        won_surface = game_font.render("you won",False,(0,255,0))
        surface.blit(won_surface,(950,550))
        
        press_space_surf = game_font2.render("press space to restart!",False,(0,255,200))
        
        surface.blit(press_space_surf,(850,600))
    #update the window surface
    pygame.display.flip()  # Any content drawn on this surface becomes visible when pygame.display.flip() is called.

            