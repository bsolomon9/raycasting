import pygame, math

pygame.init()
win = pygame.display.set_mode([500,500])

clock = pygame.time.Clock()

def normal_to_map(num):
    return round( (round(num, -1)+1)/10 )-1

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
    return None

def draw(win,p1,user_lines,walls):
    win.fill((0,0,0))

    pygame.draw.circle(win, (255,0,255), p1, 5)
        
    start_angle = player_angle - FOV
    for i in range(CASTED_RAYS):
        target_x = p1[0] - math.sin(start_angle) * 700
        target_y = p1[1] + math.cos(start_angle) * 700

        closest = 100000
        closest_point = [target_x, target_y]
        for line in user_lines:
            if walls:
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
                    closest_point = intersect_point
        if not walls:
            pygame.draw.circle(win, (255,255,255), closest_point, 2)
        pygame.draw.line(win, (55,55,55), p1, (closest_point[0],closest_point[1]) )
        #pygame.draw.line(win, (55,55,55), p1, (target_x,target_y)
        start_angle += STEP_ANGLE

    pygame.display.flip()


p1 = [20,20]
lines = []
player_angle = math.pi

FOV = math.pi * 2 #/ 3
CASTED_RAYS = 100
STEP_ANGLE = FOV / CASTED_RAYS


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

    if keys[pygame.K_d]: p1[0] += 2
    if keys[pygame.K_a]: p1[0] -= 2
    if keys[pygame.K_w]: p1[1] -= 2
    if keys[pygame.K_s]: p1[1] += 2

    if keys[pygame.K_SPACE]: show_walls = True

    draw(win,p1,lines,show_walls)