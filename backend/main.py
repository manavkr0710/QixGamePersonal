import pygame
 
pygame.init()
 
import pygame
 
pygame.init()

screen = pygame.display.set_mode((700, 700), pygame.RESIZABLE)
running = True
clock = pygame.time.Clock()
##player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

push_enabled = False
width = 20
height = 20
screen_width = screen.get_width() 
screen_height = screen.get_height() 
xpos = screen_width/2
ypos = screen_height - height -50
speed = 5
push_enabled = False
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                push_enabled = not push_enabled

    screen.fill("white")
    border_thickness = 20
    pygame.draw.rect(screen, "black", (50, 20, screen_width - 100, screen_height - 70), border_thickness)

    
    rectangle = pygame.draw.rect(screen, "red", (xpos, ypos, width, height))
    

        ##erase_width = width
        ##erase_height = height
        
        ##key movement

    keys = pygame.key.get_pressed()
    if push_enabled:  # Unrestricted movement
        if keys[pygame.K_LEFT]:
            xpos -= speed
            if xpos < 50:
                xpos = 50
        if keys[pygame.K_RIGHT]:
            xpos += speed
            if xpos > screen_width - width - 50:
                    xpos = screen_width - width - 50
        if keys[pygame.K_UP]:
            ypos -= speed
            if ypos < 20:
                    ypos = 20
        if keys[pygame.K_DOWN]:
            ypos += speed
            if ypos > screen_height - height - 50:
                    ypos = screen_height - height - 50
    else:

        if keys[pygame.K_LEFT]:
            if ypos == 20:
                xpos -= speed
                if xpos < 50:
                    xpos = 50
            elif ypos == screen_height - height - 50:
                xpos -= speed
                if xpos < 50: 
                    xpos = 50
        if keys[pygame.K_RIGHT]:
            if ypos == 20:
                xpos += speed
                if xpos > screen_width - width - 50:
                    xpos = screen_width - width - 50
            elif ypos == screen_height - height - 50:  # Bottom border
                xpos += speed
                if xpos > screen_width - width - 50:
                    xpos = screen_width - width - 50
            
        if keys[pygame.K_UP]:
            if xpos == 50:  # Left border
                ypos -= speed
                if ypos < 20:
                    ypos = 20
            elif xpos == screen_width - width - 50:  # Right border
                ypos -= speed
                if ypos < 20:
                    ypos = 20
        if keys[pygame.K_DOWN]:
            if xpos == 50:  # Left border
                ypos += speed
                if ypos > screen_height - height - 50:
                    ypos = screen_height - height - 50
            elif xpos == screen_width - width - 50:  # Right border
                ypos += speed
                if ypos > screen_height - height - 50:
                    ypos = screen_height - height - 50
        
            
        
    

    
    pygame.display.flip()

    dt = clock.tick(60) / 1000
            
pygame.quit()