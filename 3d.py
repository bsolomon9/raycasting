import pygame, math

pygame.init()
win = pygame.display.set_mode([500,500])

clock = pygame.time.Clock()

def line_line(point_1,point_2,point_3,point_4):
    denominator = ((point_4[1]-point_3[1])*(point_2[0]-point_1[0]) - (point_4[0]-point_3[0])*(point_2[1]-point_1[1]))
    if denominator == 0:
        return None

    uA = ((point_4[0]-point_3[0])*(point_1[1]-point_3[1]) - (point_4[1]-point_3[1])*(point_1[0]-point_3[0]))/denominator
    uB = ((point_2[0]-point_1[0])*(point_1[1]-point_3[1]) - (point_2[1]-point_1[1])*(point_1[0]-point_3[0]))/denominator

    if uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1:
        intersectionX = point_1[0] + (uA * (point_2[0]-point_1[0]))
        intersectionY = point_1[1] + (uA * (point_2[1]-point_1[1]))
        return (intersectionX, intersectionY)
    return


def draw(win,p1,user_lines):
    win.fill((0,0,0))

    #background
    pygame.draw.rect(win, (100, 100, 100), (0, SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))
    pygame.draw.rect(win, (200, 200, 200), (0, -SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))

        
    start_angle = player_angle - HALF_FOV
    for ray in range(CASTED_RAYS):
        target_x = p1[0] - math.sin(start_angle) * 700
        target_y = p1[1] + math.cos(start_angle) * 700

        closest = 100000

        for line in user_lines:
            pygame.draw.line(win, (255,255,255), line[0],line[1])

            intersect_point = line_line( p1, (target_x,target_y),line[0],line[1])
            if intersect_point is not None:
                #pygame.draw.circle(win, (255,255,255), intersect_point, 2)

                # Get distance between ray source and intersect point
                ray_dx = p1[0] - intersect_point[0]
                ray_dy = p1[1] - intersect_point[1]
                
                # If the intersect point is closer than the previous closest intersect point, it becomes the closest intersect point
                distance = math.sqrt(ray_dx**2 + ray_dy**2)
                if (distance < closest):
                    closest = distance

                #color = 255 / (1 + depth * depth * 0.0001)
                color = (1 + closest * closest * 0.0005)
                if color > 255: color = 255
                if color < 0: color = 0
                wall_height = 21000 / closest
                pygame.draw.rect(win, (255, color, color), (
                                    ray * SCALE,
                                    (SCREEN_HEIGHT / 2) - wall_height / 2,
                                     SCALE+1, wall_height))
                

        start_angle += STEP_ANGLE

    for line in user_lines: pygame.draw.line(win, (255,255,255), line[0],line[1])

    #fov lines    
    pygame.draw.line(win, (0, 0, 0), (p1[0], p1[1]),
                        (p1[0] - math.sin(player_angle - HALF_FOV) * 50,
                        p1[1] + math.cos(player_angle - HALF_FOV) * 50), 3)
    
    pygame.draw.line(win, (0, 0, 0), (p1[0], p1[1]),
                        (p1[0] - math.sin(player_angle + HALF_FOV) * 50,
                        p1[1] + math.cos(player_angle + HALF_FOV) * 50), 3)

    pygame.display.flip()


p1 = [20,20]
player_angle = math.pi

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS
SCALE = (SCREEN_WIDTH) / CASTED_RAYS

lines = [
    ( (1,1), (0,499) ),
    ( (1,1), (499,0) ),
    ( (499,499), (0,499) ),
    ( (499,499), (499,0) )
]

run = True
while run:
    clock.tick(60)
    show_walls = False

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONUP:
            lines.append( (pos, pygame.mouse.get_pos()) )
  
        if event.type == pygame.QUIT: 
            run = False
        


    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]: player_angle -= 0.05
    if keys[pygame.K_RIGHT]: player_angle += 0.05
    if keys[pygame.K_UP]:
        forward = True
        p1[0] += -math.sin(player_angle) * 3
        p1[1] += math.cos(player_angle) * 3
    if keys[pygame.K_DOWN]:
        forward = False
        p1[0] -= -math.sin(player_angle) * 3
        p1[1] -= math.cos(player_angle) * 3

    draw(win,p1,lines)